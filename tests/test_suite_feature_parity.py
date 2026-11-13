"""Regression scenarios for the current suite features in the independent edition."""
from app.core.controller import Controller
from app.core.device_detector import Hardware
from app.core.settings import Settings, bundle_root
from app.core.text import TextLedger
from app.services.engine_manager import EngineManager


def test_english_dictation_keeps_its_numbers_and_units():
    settings = Settings(language="en", number_style="words", abbreviate_units=True)
    controller = Controller(settings, Hardware("fixture", 4, 16 * 2**30, 8 * 2**30))
    controller.ledger = TextLedger()
    original = "I paid 25 euros for 3 meters."
    controller.ledger.confirm("first", original)
    controller._finalize_text()
    assert controller.ledger.pending == [original]


def test_switching_language_invalidates_the_prepared_engine():
    settings = Settings(language="fr-FR", acceleration="cpu")
    manager = EngineManager(None)
    manager.active = type("Prepared", (), {"ready": True})()
    manager.signature = manager.settings_signature(settings)
    assert manager.is_prepared(settings)
    settings.language = "de"
    assert not manager.is_prepared(settings)


def test_language_and_cpu_choice_survive_automatic_and_turnkey_setup(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path / "profile"))
    monkeypatch.setenv("VOXCALIBUR_BUNDLE", str(tmp_path / "bundle"))
    bundle_root().mkdir()
    (bundle_root() / "bundle.json").write_text("{}")
    settings = Settings(language="es", acceleration="cpu")
    settings.configure_turnkey()
    settings.configure_automatic()
    loaded = Settings.load()
    assert loaded.language == "es" and loaded.acceleration == "cpu"
