from PySide6.QtWidgets import QApplication
from app.core.settings import Settings
from app.core.device_detector import Hardware
from app.core.controller import Controller
from app.ui.main_window import MainWindow
from app.core.languages import LANGUAGES


def test_choices_survive_startup(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    Settings(language="es", acceleration="cpu").save()
    settings = Settings.load()
    settings.configure_automatic()
    assert Settings.load().language == "es"
    assert Settings.load().acceleration == "cpu"
    assert [name for _, name in LANGUAGES[:6]] == ["Français", "Auto détection", "Anglais", "Espagnol", "Allemand", "Italien"]


def test_no_gpu_is_disabled_and_language_reconfigures(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    app = QApplication.instance() or QApplication([])
    c = Controller(Settings(), Hardware("fixture", 4, 16*2**30, 8*2**30))
    w = MainWindow(c)
    assert not w.gpu.isEnabled() and not w.gpu.isChecked()
    w.language.setCurrentIndex(w.language.findData("de"))
    kind, settings = c.commands.get_nowait()
    assert kind == "configure" and settings.language == "de"
    assert Settings.load().language == "de"
    w.deleteLater()
    app.processEvents()


def test_compatible_gpu_defaults_on_and_can_disable(tmp_path, monkeypatch):
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    monkeypatch.setattr("app.services.engine_manager.choose_backend", lambda *a, **kw: "cuda")
    app = QApplication.instance() or QApplication([])
    c = Controller(Settings(), Hardware("fixture", 4, 16*2**30, 8*2**30, gpus=[{"name":"GPU"}]))
    w = MainWindow(c)
    assert w.gpu.isEnabled() and w.gpu.isChecked()
    w.gpu.setChecked(False)
    assert c.commands.get_nowait()[1].acceleration == "cpu"
    assert Settings.load().acceleration == "cpu"
    w.deleteLater()
    app.processEvents()


def test_language_popup_search_keyboard_and_cancel(tmp_path, monkeypatch):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    monkeypatch.setenv("VOXCALIBUR_DATA", str(tmp_path))
    app = QApplication.instance() or QApplication([])
    c = Controller(Settings(), Hardware("fixture", 4, 16*2**30, 8*2**30))
    w = MainWindow(c)
    w.show()
    w.language.showPopup()
    app.processEvents()
    popup = w.language.popup
    assert popup.height() < 400 and popup.list.count() == len(LANGUAGES)
    popup.search.setText("espag")
    assert popup.list.count() == 1
    QTest.keyClick(popup.search, Qt.Key_Return)
    assert w.language.currentData() == "es" and not popup.isVisible()
    assert c.commands.get_nowait()[0] == "configure"
    w.language.showPopup()
    QTest.keyClick(popup.search, Qt.Key_Escape)
    assert w.language.currentData() == "es" and c.commands.empty()
    w.hide()
    w.deleteLater()
    app.processEvents()
