import os
from PIL import Image

src = f"main_/assets/menu/buttons"
dst = "assets_clean"
os.makedirs(dst, exist_ok=True)

for fname in os.listdir(src):
    if fname.lower().endswith(".png"):
        path = os.path.join(src, fname)
        img = Image.open(path)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA")
        img.save(os.path.join(dst, fname), optimize=True)
