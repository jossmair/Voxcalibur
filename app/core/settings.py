from __future__ import annotations

import json
import math
import os
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, fields, field
from pathlib import Path


def data_root() -> Path:
    return Path(
        os.environ.get(
            "VOXCALIBUR_DATA", str(Path(os.environ.get("LOCALAPPDATA", Path.home())) / "Voxcalibur")
        )
    )


def directory(name: str) -> Path:
    result = data_root() / name
    result.mkdir(parents=True, exist_ok=True)
    return result


def bundle_root() -> Path:
    override = os.environ.get("VOXCALIBUR_BUNDLE")
    if override:
        return Path(override)
    return (
        Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[2]
    )


@dataclass
class Settings:
    engine: str = "parakeet"
    acceleration: str = "auto"
    microphone: int | None = None
    language: str = "fr-FR"
    hotkey: str = "single"
    trigger_key: str = "shift_left"
    hub_visible: bool = True
    hub_auto: bool = True
    hub_compact: bool = False
    hub_position: tuple[int, int] | None = None
    start_minimized: bool = True
    autostart: bool = False
    notifications: bool = False
    punctuation: bool = True
    capitals: bool = False
    typography: bool = False
    voice_commands: bool = False
    progressive: bool = False
    insertion_strategy: str = "auto"
    vad_threshold: float = 0.5
    silence_ms: int = 360
    segment_seconds: int = 30
    setup_done: bool = False
    turnkey_configured: bool = False
    experience_revision: int = 0
    vocabulary: list = field(default_factory=list)
    number_style: str = "original"
    abbreviate_units: bool = False
    short_dictation_unpunctuated: bool = True
    text_options_revision: int = 1

    def configure_automatic(self) -> bool:
        """The consumer application has one supported, fully automatic path."""
        first_launch = not self.setup_done or self.experience_revision < 7
        self.engine = "parakeet"
        if self.acceleration != "cpu":
            self.acceleration = "auto"
        self.microphone, self.hotkey, self.insertion_strategy = None, "single", "auto"
        self.progressive, self.punctuation = False, True
        self.notifications = False
        self.capitals, self.typography, self.voice_commands = False, False, False
        self.hub_visible, self.hub_auto, self.hub_compact = True, True, False
        self.hub_position = None
        self.vad_threshold, self.silence_ms, self.segment_seconds = 0.5, 360, 30
        self.setup_done, self.experience_revision = True, 7
        self.turnkey_configured = (bundle_root() / "bundle.json").is_file()
        try:
            self.save()
        except OSError:
            pass  # Read-only preferences must not prevent dictation from starting.
        return first_launch

    def configure_turnkey(self) -> bool:
        if self.turnkey_configured or not (bundle_root() / "bundle.json").is_file():
            return False
        self.engine = "parakeet"
        if self.acceleration != "cpu":
            self.acceleration = "auto"
        self.microphone, self.hotkey, self.insertion_strategy = None, "single", "auto"
        self.progressive = True
        self.experience_revision = 3
        self.setup_done, self.turnkey_configured = True, True
        self.save()
        return True

    @classmethod
    def load(cls) -> Settings:
        path = data_root() / "preferences/settings.json"
        backup = path.with_name("settings.backup.json")
        value = read_preferences(path)
        previous = read_preferences(backup)
        if value is None:
            value = previous or {}
        result = cls()
        # Validate each field independently: one bad value cannot discard the dictionary.
        for item in fields(cls):
            default = getattr(result, item.name)
            candidate = value.get(item.name, default)
            if isinstance(default, bool):
                candidate = candidate if isinstance(candidate, bool) else default
            elif isinstance(default, str):
                candidate = candidate if isinstance(candidate, str) else default
            elif item.name in (
                "experience_revision",
                "silence_ms",
                "segment_seconds",
                "vad_threshold",
                "text_options_revision",
            ):
                try:
                    if isinstance(candidate, bool) or not math.isfinite(float(candidate)):
                        raise ValueError
                    candidate = float(candidate) if item.name == "vad_threshold" else int(candidate)
                except (ValueError, TypeError, OverflowError):
                    candidate = default
            elif item.name == "vocabulary":
                if not isinstance(candidate, list):
                    candidate = (previous or {}).get("vocabulary", [])
            elif item.name == "microphone":
                candidate = candidate if type(candidate) is int and candidate >= 0 else None
            elif item.name == "hub_position":
                candidate = (
                    tuple(candidate)
                    if isinstance(candidate, (list, tuple))
                    and len(candidate) == 2
                    and all(type(n) is int for n in candidate)
                    else None
                )
            setattr(result, item.name, candidate)
        result.engine = "parakeet"
        from app.core.languages import LANGUAGE_CODES

        if result.language not in LANGUAGE_CODES:
            result.language = "fr-FR"
        if result.acceleration not in {"auto", "cpu", "gpu"}:
            result.acceleration = "auto"
        from app.core.text_options import normalize_vocabulary

        result.vocabulary = normalize_vocabulary(result.vocabulary)
        if result.number_style not in {"original", "digits", "words"}:
            result.number_style = "original"
        from app.core.hotkeys import trigger_spec

        result.trigger_key = trigger_spec(result.trigger_key)[0]
        if result.experience_revision < 3:
            result.progressive = True
            result.experience_revision = 3
            result.silence_ms, result.segment_seconds = 360, 30
        if result.insertion_strategy not in {"auto", "unicode", "native", "clipboard"}:
            result.insertion_strategy = "auto"
        # Replace the previous automatic formatting defaults once; preserve custom modes.
        if "text_options_revision" not in value:
            if value.get("number_style") == "digits" and value.get("abbreviate_units") is True:
                result.number_style, result.abbreviate_units = "original", False
            result.text_options_revision = 1
        result.silence_ms = max(200, min(2000, result.silence_ms))
        result.segment_seconds = max(3, min(30, result.segment_seconds))
        result.vad_threshold = max(0.1, min(0.95, result.vad_threshold))
        return result

    def save(self) -> None:
        path = directory("preferences") / "settings.json"
        contents = json.dumps(asdict(self), ensure_ascii=False, indent=2).encode("utf-8")
        try:
            original = path.read_bytes()
        except FileNotFoundError:
            original = None
        if original is not None:
            try:
                valid = isinstance(json.loads(original.decode("utf-8")), dict)
            except (ValueError, UnicodeError):
                valid = False
            if not valid:
                # Preserve the original before replacing it with recovered preferences.
                atomic_write(path.with_name(f"settings.corrupt-{time.time_ns()}.json"), original)
        atomic_write(path, contents)
        try:
            atomic_write(path.with_name("settings.backup.json"), contents)
        except OSError:
            pass  # The primary save has succeeded; keep any previous usable backup.


def read_preferences(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, ValueError, UnicodeError):
        return None


def atomic_write(path, contents):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
