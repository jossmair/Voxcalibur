"""Explicit download/extraction of the pinned, licensed French FLEURS test split."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import struct
import urllib.request
import wave

import numpy as np


def canonical_wav(data):
    """Convert the published float32 RIFF recordings to reproducible PCM16 WAV."""
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        raise ValueError("Expected RIFF/WAVE audio")
    chunks = {}
    offset = 12
    while offset + 8 <= len(data):
        name, size = struct.unpack_from("<4sI", data, offset)
        start = offset + 8
        if start + size > len(data):
            raise ValueError("Truncated WAV chunk")
        chunks[name] = data[start : start + size]
        offset = start + size + (size % 2)
    encoding, channels, rate, _, alignment, bits = struct.unpack_from("<HHIIHH", chunks[b"fmt "])
    payload = chunks[b"data"]
    if channels < 1 or rate < 8000 or len(payload) % alignment:
        raise ValueError("Invalid WAV layout")
    if encoding == 3 and bits == 32:
        samples = np.frombuffer(payload, dtype="<f4")
        if not np.isfinite(samples).all():
            raise ValueError("Nonfinite audio")
        pcm = np.rint(np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes()
    elif encoding == 1 and bits == 16:
        pcm = payload
    else:
        raise ValueError(f"Unsupported WAV encoding: {encoding}/{bits}")
    output = io.BytesIO()
    with wave.open(output, "wb") as target:
        target.setnchannels(channels)
        target.setsampwidth(2)
        target.setframerate(rate)
        target.writeframes(pcm)
    return output.getvalue()


def digest(path):
    result = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def prepare(destination, allow_download=False):
    import pyarrow.parquet as pq

    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "benchmarks/corpora/fleurs-fr-test.json").read_text(encoding="utf-8"))
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    parquet = destination / "0000.parquet"
    if not parquet.is_file():
        if not allow_download:
            raise RuntimeError("Corpus absent : fournir --allow-download pour le téléchargement explicite.")
        url = f"https://huggingface.co/datasets/google/fleurs/resolve/{catalog['revision']}/{catalog['file']}"
        temporary = parquet.with_suffix(".part")
        with urllib.request.urlopen(url, timeout=60) as source, temporary.open("wb") as output:
            shutil.copyfileobj(source, output, length=4 * 1024 * 1024)
        temporary.replace(parquet)
    if parquet.stat().st_size != catalog["bytes"] or digest(parquet) != catalog["sha256"]:
        raise RuntimeError("Corpus différent de la révision publique épinglée.")
    audio_dir = destination / "wav"
    audio_dir.mkdir(exist_ok=True)
    cases = []
    for batch in pq.ParquetFile(parquet).iter_batches(batch_size=16):
        for row in batch.to_pylist():
            identity = f"fleurs-fr-test-{len(cases):05d}"
            original = row["audio"]["bytes"]
            data = canonical_wav(original)
            with wave.open(io.BytesIO(data), "rb") as recording:
                if recording.getsampwidth() != 2 or recording.getcomptype() != "NONE":
                    raise RuntimeError("Le corpus épinglé doit contenir des WAV PCM16.")
                duration = recording.getnframes() / recording.getframerate()
            path = audio_dir / (identity + ".wav")
            path.write_bytes(data)
            cases.append(
                {
                    "id": identity,
                    "audio": path.relative_to(destination).as_posix(),
                    "text": row["raw_transcription"],
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "original_audio_sha256": hashlib.sha256(original).hexdigest(),
                    "duration_seconds": duration,
                    "source_sentence_id": str(row["id"]),
                    "speaker_id": None,
                    "microphone": "unknown",
                    "environment": "unknown",
                    "gender_label": {0: "male", 1: "female"}.get(row["gender"], "unknown"),
                }
            )
    manifest = {
        "schema_version": 1,
        "provenance": {**catalog, "audio_conversion": "IEEE float32 to PCM16: round(clip(x,-1,1)*32767)"},
        "cases": cases,
    }
    path = destination / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Prepared {len(cases)} human recordings ({sum(c['duration_seconds'] for c in cases) / 60:.1f} minutes)"
    )
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("vendor/fleurs-fr-test"))
    parser.add_argument("--allow-download", action="store_true")
    options = parser.parse_args()
    prepare(options.output, options.allow_download)
