import hashlib
import json

import numpy as np
import pytest

from scripts.evaluate_corpus import condition_audio, load_manifest


def test_added_noise_is_seeded_and_has_the_declared_snr():
    original = (0.02 * np.sin(np.arange(16000) * 0.2)).astype(np.float32)
    result = condition_audio(original, "white20", 42, "recording")
    noise = result - original
    snr = 10 * np.log10(np.mean(original**2) / np.mean(noise**2))
    assert abs(snr - 20) < 0.01
    assert np.array_equal(result, condition_audio(original, "white20", 42, "recording"))
    assert not np.array_equal(result, condition_audio(original, "white20", 43, "recording"))
    assert np.array_equal(original, condition_audio(original, "clean", 42, "recording"))


def test_peak_protection_keeps_noisy_audio_finite_and_bounded():
    original = np.ones(16000, dtype=np.float32)
    result = condition_audio(original, "white10", 42, "recording")
    assert np.isfinite(result).all() and np.max(np.abs(result)) <= 1


def test_changed_corpus_and_path_escape_are_rejected(tmp_path):
    audio = tmp_path / "sample.wav"
    audio.write_bytes(b"fixture")
    case = {
        "id": "one",
        "audio": "sample.wav",
        "text": "Bonjour",
        "sha256": hashlib.sha256(b"fixture").hexdigest(),
    }
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"schema_version": 1, "provenance": {}, "cases": [case]}))
    assert load_manifest(manifest)["cases"][0]["id"] == "one"
    audio.write_bytes(b"changed")
    with pytest.raises(ValueError, match="changed"):
        load_manifest(manifest)
    case["audio"] = "../outside.wav"
    manifest.write_text(json.dumps({"schema_version": 1, "cases": [case]}))
    with pytest.raises(ValueError, match="inside"):
        load_manifest(manifest)


def test_empty_manifest_is_not_a_successful_evaluation(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"schema_version": 1, "cases": []}')
    with pytest.raises(ValueError, match="nonempty"):
        load_manifest(manifest)
