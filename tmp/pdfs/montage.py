from PIL import Image, ImageDraw
from pathlib import Path

fs = sorted(Path("tmp/pdfs").glob("redline-page-*.png"))
thumbs = []
for f in fs:
    im = Image.open(f).convert("RGB")
    im.thumbnail((240, 320))
    tile = Image.new("RGB", (250, 345), "#dddddd")
    tile.paste(im, ((250 - im.width) // 2, 8))
    ImageDraw.Draw(tile).text((8, 328), f.stem, fill="black")
    thumbs.append(tile)
out = Image.new("RGB", (1250, 345 * ((len(thumbs) + 4) // 5)), "white")
for i, im in enumerate(thumbs):
    out.paste(im, ((i % 5) * 250, (i // 5) * 345))
out.save("tmp/pdfs/contact.png")
