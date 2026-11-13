import io
import struct
import wave

import numpy as np
import pytest

from scripts.prepare_fleurs import canonical_wav


def test_public_float_wave_is_converted_without_changing_rate_or_length():
    samples = np.array([0.0, 0.5, -1.0, 1.0], dtype="<f4").tobytes()
    fmt = struct.pack("<HHIIHH", 3, 1, 16000, 64000, 4, 32)
    body = (
        b"WAVEfmt " + struct.pack("<I", len(fmt)) + fmt + b"data" + struct.pack("<I", len(samples)) + samples
    )
    original = b"RIFF" + struct.pack("<I", len(body)) + body
    converted = canonical_wav(original)
    with wave.open(io.BytesIO(converted), "rb") as recording:
        assert recording.getframerate() == 16000 and recording.getnframes() == 4
        assert recording.getsampwidth() == 2
        assert np.frombuffer(recording.readframes(4), dtype="<i2").tolist() == [0, 16384, -32767, 32767]


def test_malformed_recording_is_rejected_before_scoring():
    with pytest.raises(ValueError, match="RIFF"):
        canonical_wav(b"not an audio recording")
