#!/usr/bin/env python3
"""Sum up 23 November 2026 world news in one 1024x1024 image.
Deterministic, no network, no randomness, no timestamps.
Writes /output/entry.png (creates /output if needed).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"

def font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for p in (f"/usr/share/fonts/truetype/dejavu/{name}",
              f"/usr/share/fonts/TTF/{name}"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def panel(draw, x, y, w, h, color, num, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill="white",
                   outline=(210, 210, 210), width=2)
    draw.rectangle([x, y, x + w, y + 10], fill=color)
    draw.text((x + 28, y + 28), num, font=font(28, True), fill=color)
    draw.text((x + 78, y + 36), kicker, font=font(22, True), fill=(90, 90, 90))
    # headline, wrapped
    lines = wrap(draw, headline, font(44, True), w - 56)
    yy = y + 78
    for ln in lines:
        draw.text((x + 28, yy), ln, font=font(44, True), fill=(20, 20, 20))
        yy += 52
    yy += 8
    for ln in wrap(draw, body, font(26), w - 56):
        draw.text((x + 28, yy), ln, font=font(26), fill=(60, 60, 60))
        yy += 36

def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    # header
    d.rectangle([0, 0, W, 118], fill=(12, 32, 64))
    d.text((32, 18), "WORLD NEWS", font=font(52, True), fill="white")
    d.text((32, 76), "MONDAY  23  NOVEMBER  2026", font=font(26, True),
           fill=(170, 200, 235))
    d.text((700, 30), "IN ONE", font=font(30, True), fill=(255, 210, 90))
    d.text((700, 66), "IMAGE", font=font(30, True), fill=(255, 210, 90))
    panels = [
        ((16, 134, 488, 410), (0, 130, 120), "01", "CLIMATE",
         "COP31 COLLAPSES",
         "Climate talks in Antalya end with no deal. The EU rejects a text with no fossil-fuel phase-out."),
        ((520, 134, 488, 410), (160, 40, 40), "02", "UKRAINE",
         "KYIV UNDER FIRE",
         "Russian strikes kill at least 15 in the Kyiv region. 23 November is a day of mourning."),
        ((16, 560, 488, 410), (20, 80, 160), "03", "USA",
         "DEMOCRATS WIN BIG",
         "Democrats clinch the biggest US House majority in decades, at least 258 seats."),
        ((520, 560, 488, 410), (180, 90, 0), "04", "IRAN",
         "IRAN ON EDGE",
         "Trump says he is inclined to resume strikes after the New Year if no deal is reached."),
    ]
    for (x, y, w, h), color, num, kicker, head, body in panels:
        panel(d, x, y, w, h, color, num, kicker, head, body)
    d.rectangle([0, 986, W, H], fill=(12, 32, 64))
    d.text((32, 992), "COP31  •  KYIV  •  WASHINGTON  •  TEHRAN",
           font=font(20, True), fill="white")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, "PNG", optimize=True)

if __name__ == "__main__":
    main()
