import zipfile
from pathlib import Path
from app import __version__


def source_files(root):
    items = [root / name for name in ("app", "assets", "docs", "tests", "scripts", "installer", "benchmarks", ".github")]
    # Disposable profiles may contain local preferences. Never distribute them.
    files = [f for folder in items for f in folder.rglob("*")
             if f.is_file() and "__pycache__" not in f.parts
             and not f.is_relative_to(root / "docs/test-settings")]
    files += [root / name for name in (
        "README.md",
        "Lancer Voxcalibur.cmd",
        "LICENSE",
        "pyproject.toml",
        "requirements-lock.txt",
        "requirements-benchmark.txt",
        "Voxcalibur.spec",
        ".gitignore",
        ".gitattributes",
    )]
    return sorted(files)


def main():
    root = Path(__file__).resolve().parent.parent
    destination = root / "dist" / f"Voxcalibur-{__version__}-Sources.zip"
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in source_files(root):
            archive.write(file, Path("Voxcalibur") / file.relative_to(root))
    print(destination)


if __name__ == "__main__":
    main()
