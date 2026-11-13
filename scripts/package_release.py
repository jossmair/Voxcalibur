"""Create the two complete downloadable archives, sources and SHA-256 checksums."""
import hashlib
import zipfile
from pathlib import Path
from app import __version__
from scripts.package_sources import main as package_sources


def main():
    root = Path(__file__).resolve().parents[1]
    dist = root / "dist"
    installation = dist / f"Installation-Voxcalibur-{__version__}"
    required = ("Installer-Voxcalibur.exe", "payload.zip", "payload.json", "uninstaller.exe")
    for name in required:
        if not (installation / name).is_file():
            raise RuntimeError(f"Installation incomplète : {name}")
    archive_path = dist / f"Voxcalibur-{__version__}-Installation.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_STORED, allowZip64=True) as archive:
        for name in required:
            archive.write(installation / name, f"{installation.name}/{name}")
    package_sources()
    archives = [dist / f"Voxcalibur-{__version__}-{kind}.zip" for kind in ("Portable", "Installation", "Sources")]
    lines = []
    for path in archives:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                digest.update(chunk)
        lines.append(f"{digest.hexdigest()}  {path.name}")
        print(f"Ready: {path.name} ({path.stat().st_size} bytes)", flush=True)
    (dist / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
