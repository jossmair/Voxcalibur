from pathlib import Path
from PIL import Image
root = Path(__file__).resolve().parents[1]
source = Image.open(root / "assets/voxcalibur-logo.png").convert("RGBA")
source.thumbnail((256, 256), Image.Resampling.LANCZOS)
icon = Image.new("RGBA", (256, 256))
icon.alpha_composite(source, ((256-source.width)//2, (256-source.height)//2))
icon.save(root / "assets/voxcalibur.png")
icon.save(root / "assets/voxcalibur.ico", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
