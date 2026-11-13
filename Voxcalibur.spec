from PyInstaller.utils.hooks import collect_submodules
import os
from pathlib import Path
import PySide6
from app import __version__

# Exclude unrelated DLL directories inherited from development tools.
os.environ['PATH'] = os.pathsep.join([str(Path('.venv/Scripts').resolve()),
    str(Path(os.environ.get('SystemRoot', 'C:/Windows')) / 'System32'),
    os.environ.get('SystemRoot', 'C:/Windows')])

a = Analysis(['scripts/run_voxcalibur.py'], pathex=['.'], binaries=[],
    datas=[('assets/voxcalibur-logo.png', 'assets'), ('assets/voxcalibur.svg', 'assets'), ('assets/voxcalibur.ico', 'assets'),
           ('assets/hud-orange/core-main-v1.png', 'assets/hud-orange'), ('assets/hud-orange/core-hub-v1.png', 'assets/hud-orange'),
           ('assets/hud-orange/orbit-overlay-v1.png', 'assets/hud-orange'), ('assets/hud-orange/halo-v1.png', 'assets/hud-orange'),
           ('assets/hud-orange/surface-main-v1.png', 'assets/hud-orange'), ('assets/hud-orange/surface-hub-v1.png', 'assets/hud-orange'),
           ('assets/hud-orange/frames', 'assets/hud-orange/frames'),
           ('docs/third-party', 'third-party-licenses'),
           ('assets/licenses/NVIDIA-CUDA-EULA.txt', 'assets/licenses'),
           (str(Path(PySide6.__file__).parent / 'translations' / 'qtbase_fr.qm'), 'assets')],
    hiddenimports=collect_submodules('comtypes.gen'),
    excludes=['PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets', 'PySide6.QtPdf',
              'PySide6.QtPdfWidgets', 'tkinter', 'matplotlib', 'torch', 'pytest'],
    noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='Voxcalibur', debug=False,
          bootloader_ignore_signals=False, strip=False, upx=False, console=False,
          icon='assets/voxcalibur.ico')
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name=f'Voxcalibur-{__version__}')
