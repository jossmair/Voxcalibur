import json

import pytest
from PySide6.QtWidgets import QApplication

from app.core.controller import Controller
from app.core.device_detector import Hardware
from app.core.settings import Settings
from app.core.text_options import TextPostprocessor
from app.ui.main_window import MainWindow


def processor(settings):
    return TextPostprocessor(
        settings.vocabulary,
        settings.number_style,
        settings.abbreviate_units,
        settings.short_dictation_unpunctuated,
    )


def test_new_defaults_preserve_recognized_numbers_and_units():
    settings = Settings()
    assert settings.number_style == "original" and not settings.abbreviate_units
    text = "Les dix-sept personnes transportent vingt kilogrammes demain."
    assert processor(settings).apply(text) == text
    settings.abbreviate_units = True
    assert processor(settings).apply("vingt kilogrammes") == "vingt kg"


@pytest.mark.parametrize(
    "text,enabled,expected",
    [
        ("Bonjour !", True, "Bonjour"),
        ("Bonjour !", False, "Bonjour !"),
        ("un deux trois quatre.", True, "un deux trois quatre"),
        ("un deux trois quatre cinq.", True, "un deux trois quatre cinq."),
        ("Prix : 12,5 € !", True, "Prix 12,5 €"),
        ("https://exemple.fr/bonjour.", True, "https://exemple.fr/bonjour"),
    ],
)
def test_short_dictation_switch_and_exact_five_word_boundary(text, enabled, expected):
    settings = Settings(short_dictation_unpunctuated=enabled)
    assert processor(settings).apply(text) == expected


def test_explicit_dictionary_still_works_in_original_number_mode():
    settings = Settings(vocabulary=[{"name": "Josselin", "aliases": ["Jocelyn"]}])
    assert (
        processor(settings).apply("Jocelyn écrit dix-sept mots aujourd’hui.")
        == "Josselin écrit dix-sept mots aujourd’hui."
    )


def test_legacy_default_migrates_once_and_keeps_custom_preferences(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    path = tmp_path / "preferences/settings.json"
    path.parent.mkdir()
    path.write_text(
        json.dumps(
            {
                "number_style": "digits",
                "abbreviate_units": True,
                "trigger_key": "f8",
                "language": "es",
                "vocabulary": ["Josselin"],
            }
        )
    )
    loaded = Settings.load()
    assert loaded.number_style == "original" and not loaded.abbreviate_units
    assert (
        loaded.trigger_key == "f8" and loaded.language == "es" and loaded.vocabulary[0]["name"] == "Josselin"
    )
    loaded.number_style, loaded.abbreviate_units = "digits", True
    loaded.short_dictation_unpunctuated = False
    loaded.save()
    loaded = Settings.load()
    loaded.configure_automatic()
    restored = Settings.load()
    assert restored.number_style == "digits" and restored.abbreviate_units
    assert not restored.short_dictation_unpunctuated


def test_legacy_custom_letters_are_not_reset(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    path = tmp_path / "preferences/settings.json"
    path.parent.mkdir()
    path.write_text('{"number_style":"words","abbreviate_units":true}')
    loaded = Settings.load()
    assert loaded.number_style == "words" and loaded.abbreviate_units


async def test_option_updates_running_processor_without_model_reload():
    controller = Controller(Settings(), Hardware("fixture", 4, 16 * 2**30, 8 * 2**30))

    async def vocabulary_update():
        pass

    controller._update_recognition_vocabulary = vocabulary_update
    controller.commands.put(
        (
            "text_options",
            {"number_style": "original", "abbreviate_units": False, "short_dictation_unpunctuated": False},
        )
    )
    controller.commands.put(("quit", None))
    await controller._process_commands()
    assert controller.text_processor.apply("Bonjour demain.") == "Bonjour demain."
    assert not controller.settings.short_dictation_unpunctuated


def test_short_punctuation_checkbox_saves_immediately(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    app = QApplication.instance() or QApplication([])
    controller = Controller(Settings(), Hardware("fixture", 4, 16 * 2**30, 8 * 2**30))
    window = MainWindow(controller)
    assert window.short_punctuation.isChecked()
    window.short_punctuation.setChecked(False)
    kind, value = controller.commands.get_nowait()
    assert kind == "text_options" and value["short_dictation_unpunctuated"] is False
    assert not Settings.load().short_dictation_unpunctuated
    window.deleteLater()
    app.processEvents()
