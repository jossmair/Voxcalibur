"""Reproducible real-audio evaluation; deliberately separate from normal dictation."""

import argparse
import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time
import wave

import numpy as np
import soxr

from scripts.benchmark_metrics import NORMALIZATION, aggregate, bootstrap_wer, score, tokens


CONDITIONS = {"clean": None, "white20": 20, "white10": 10}


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def load_manifest(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if value.get("schema_version") != 1 or not value.get("cases"):
        raise ValueError("A nonempty schema_version=1 manifest is required")
    seen = set()
    for case in value["cases"]:
        if not isinstance(case.get("id"), str) or case["id"] in seen:
            raise ValueError("Recording IDs must be unique strings")
        seen.add(case["id"])
        if not tokens(case["text"]) or len(case.get("sha256", "")) != 64:
            raise ValueError("Every recording needs a reference and an audio SHA-256")
        audio = (Path(path).parent / case["audio"]).resolve()
        if not audio.is_relative_to(Path(path).parent.resolve()):
            raise ValueError("Audio must remain inside the manifest directory")
        if not audio.is_file() or digest(audio) != case["sha256"]:
            raise ValueError(f"Missing or changed audio: {case['id']}")
    return value


def read_audio(path):
    with wave.open(str(path), "rb") as stream:
        if stream.getsampwidth() != 2 or stream.getcomptype() != "NONE":
            raise ValueError("PCM16 WAV required")
        audio = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").astype(np.float32)
        audio = audio.reshape(-1, stream.getnchannels()).mean(axis=1) / 32768
        result = soxr.resample(audio, stream.getframerate(), 16000).astype(np.float32)
    if not len(result) or not np.isfinite(result).all():
        raise ValueError("Empty or nonfinite recording")
    return result


def condition_audio(audio, condition, seed, recording_id):
    """Added Gaussian noise is a simulation, never presented as a real room."""
    snr = CONDITIONS[condition]
    if snr is None:
        return audio.copy()
    seed += int.from_bytes(hashlib.sha256(recording_id.encode()).digest()[:8], "little")
    noise = np.random.default_rng(seed).standard_normal(len(audio))
    speech_rms = np.sqrt(np.mean(audio.astype(np.float64) ** 2))
    noise *= speech_rms / (10 ** (snr / 20) * np.sqrt(np.mean(noise**2)))
    result = audio.astype(np.float64) + noise
    result *= min(1.0, 0.999 / max(0.999, float(np.max(np.abs(result)))))
    return result.astype(np.float32)


def summaries(cases, seed):
    output = {}
    for condition in sorted({case["condition"] for case in cases}):
        selected = [case for case in cases if case["condition"] == condition]
        values = [dict(case["metrics"], speaker_id=case.get("speaker_id")) for case in selected]
        raw = [case["raw_metrics"] for case in selected]
        seconds = sum(case["audio_seconds"] for case in selected)
        output[condition] = {
            **aggregate(values),
            "raw_asr": aggregate(raw),
            "wer_95ci": bootstrap_wer(values, seed=seed),
            "audio_seconds": seconds,
            "real_time_factor": sum(case["inference_seconds"] for case in selected) / seconds,
            "empty_hypotheses": sum(not case["hypothesis"].strip() for case in selected),
            "gender_labels": dict(Counter(case.get("gender_label", "unknown") for case in selected)),
        }
    return output


async def evaluate(args):
    from app import __version__
    from app.core.device_detector import detect
    from app.core.settings import Settings
    from app.core.text import TextFormatter
    from app.core.text_options import TextPostprocessor
    from app.services.engine_manager import EngineManager

    manifest = load_manifest(args.manifest)
    root = Path(__file__).resolve().parents[1]
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    settings = Settings(acceleration=args.acceleration, language="fr-FR", vocabulary=[])
    hardware = detect()
    manager = EngineManager(hardware)
    selected = manifest["cases"][: args.limit] if args.limit else manifest["cases"]
    report = {
        "schema_version": 1,
        "application_version": __version__,
        "source_commit": revision,
        "benchmark_script_sha256": digest(Path(__file__)),
        "metrics_script_sha256": digest(root / "scripts/benchmark_metrics.py"),
        "manifest_sha256": digest(args.manifest),
        "provenance": manifest["provenance"],
        "normalization": NORMALIZATION,
        "cer_normalization": "word tokens joined with single spaces",
        "settings": {
            "language": "fr-FR",
            "vocabulary": [],
            "number_style": settings.number_style,
            "abbreviate_units": settings.abbreviate_units,
            "progressive": settings.progressive,
        },
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "soxr": soxr.__version__,
            "cpu": hardware.cpu,
            "cores": hardware.cores,
            "ram_gib": round(hardware.ram_total / 2**30, 2),
            "gpus": hardware.gpus,
        },
        "requested_acceleration": args.acceleration,
        "seed": args.seed,
        "conditions": {
            name: {
                "snr_db": CONDITIONS[name],
                "kind": "original_recording" if name == "clean" else "simulated_gaussian_noise",
            }
            for name in args.conditions
        },
        "available_recordings": len(manifest["cases"]),
        "selected_recordings": len(selected),
        "is_full_split": len(selected) == len(manifest["cases"]),
        "expected_evaluations": len(selected) * len(args.conditions),
        "run_completed": False,
        "cases": [],
        "limits": [
            "Speaker identities, microphone models and original noise conditions are unknown for FLEURS.",
            "Added noise is simulated; this is not a real-microphone or real-room campaign.",
            "Recording-bootstrap intervals do not estimate generalization to unseen speakers.",
            "Possible overlap with model training data is not established.",
        ],
    }

    def save():
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(".tmp")
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(args.output)

    started = time.monotonic()
    try:
        engine = await manager.prepare(settings)
        report.update(
            backend=engine.backend,
            load_seconds=time.monotonic() - started,
            model_sha256=digest(engine.model),
            runtime_sha256=digest(engine.dll),
            runtime_filename=Path(engine.dll).name,
            vocabulary_status=engine.vocabulary_status,
        )
        postprocessor = TextPostprocessor([], settings.number_style, settings.abbreviate_units)
        for index, case in enumerate(selected):
            original = read_audio(args.manifest.parent / case["audio"])
            for condition in args.conditions:
                audio = condition_audio(original, condition, args.seed, case["id"])
                events = []
                inference_started = time.monotonic()
                await engine.begin(events.append)
                for offset in range(0, len(audio), 512):
                    await engine.feed(audio[offset : offset + 512])
                stop = time.monotonic()
                await engine.finish()
                end = time.monotonic()
                raw = " ".join(event.text for event in events if event.final)
                formatter = TextFormatter(settings)
                text = "".join(formatter.format(event.text) for event in events if event.final)
                text = postprocessor.apply(text)
                report["cases"].append(
                    {
                        "id": case["id"],
                        "condition": condition,
                        "reference": case["text"],
                        "hypothesis": text,
                        "raw_hypothesis": raw,
                        "speaker_id": case.get("speaker_id"),
                        "gender_label": case.get("gender_label", "unknown"),
                        "microphone": case.get("microphone", "unknown"),
                        "environment": case.get("environment", "unknown"),
                        "source_sentence_id": case.get("source_sentence_id"),
                        "audio_sha256": case["sha256"],
                        "processed_audio_sha256": hashlib.sha256(audio.tobytes()).hexdigest(),
                        "audio_seconds": len(audio) / 16000,
                        "inference_seconds": end - inference_started,
                        "flush_seconds": end - stop,
                        "metrics": score(case["text"], text),
                        "raw_metrics": score(case["text"], raw),
                    }
                )
            if (index + 1) % 25 == 0:
                save()
                print(
                    f"Evaluated {index + 1}/{len(selected)} recordings, {len(report['cases'])} conditions",
                    flush=True,
                )
        report["summary"] = summaries(report["cases"], args.seed)
        report["run_completed"] = len(report["cases"]) == report["expected_evaluations"]
    except BaseException as error:
        report["error_type"] = type(error).__name__
        raise
    finally:
        try:
            await manager.close()
        finally:
            report["total_seconds"] = time.monotonic() - started
            save()
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--acceleration", choices=("cpu", "auto", "gpu"), default="cpu")
    parser.add_argument("--conditions", nargs="+", choices=tuple(CONDITIONS), default=list(CONDITIONS))
    parser.add_argument("--seed", type=int, default=20261113)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if len(args.conditions) != len(set(args.conditions)):
        parser.error("Conditions must be unique")
    asyncio.run(evaluate(args))
