#!/usr/bin/env python3
"""SLIDESHOW RECIPE v2 builder: cover (real frame + black band title) + item slides (item frame top, map below) + end slide.
Usage: python3 tools/slides_v2_build.py media/configs/<cfg>.json   (frames are grabbed from cfg["src"] with ffmpeg)"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
cfg = json.load(open(sys.argv[1])); out = cfg["out_dir"]; os.makedirs(out, exist_ok=True)
F = "brand/fonts/TikTokSans-800.ttf"; f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1350; TMP = "/tmp/slides_v2"; os.makedirs(TMP, exist_ok=True)

def grab(t, gamma=1.0):
    p = f"{TMP}/{t}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", cfg["src"], "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB")
    return ImageEnhance.Brightness(im).enhance(gamma) if gamma != 1.0 else im

def fill(im, w, h, cx=0.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1))
    x = int((im.width - w) * cx); y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))

def text(d, y, s, size, fill=(255, 255, 255), maxw=940):
    fo = f(size)
    while d.textlength(s, font=fo) > maxw: size -= 2; fo = f(size)
    d.text((W // 2, y), s, font=fo, fill=fill, anchor="mt", stroke_width=max(4, size // 12), stroke_fill=(0, 0, 0))
    return y + int(size * 1.12)

def grad_text(im, y, s, size):
    d = ImageDraw.Draw(im); fo = f(size)
    while d.textlength(s, font=fo) > 960: size -= 2; fo = f(size)
    w = int(d.textlength(s, font=fo)); h = int(size * 1.2)
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).text((0, 0), s, font=fo, fill=255)
    g = Image.new("RGB", (w, h))
    for x in range(w):
        a = x / max(1, w - 1); ImageDraw.Draw(g).line([(x, 0), (x, h)], fill=(int(150 + 105 * a), int(70 - 20 * a), int(255 - 60 * a)))
    im.paste(g, ((W - w) // 2, y), mask); return y + int(size * 1.12)

def credit(d):
    d.text((W // 2, 1262), cfg["credit"], font=f(28), fill=(255, 255, 255), anchor="mt", stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((W // 2, 1298), "Fan page. Not affiliated with Rockstar Games.", font=f(22), fill=(210, 210, 210), anchor="mt", stroke_width=3, stroke_fill=(0, 0, 0))

n = 0
def save(im):
    global n; n += 1; p = f"{out}/{n:02d}.jpg"; im.save(p, quality=92); print(p)

c = cfg["cover"]; im = Image.new("RGB", (W, H)); im.paste(fill(grab(c["t"], c.get("gamma", 1.0)), W, 900, c.get("cx", 0.5)), (0, 0))
d = ImageDraw.Draw(im); d.rectangle((0, 900, W, H), fill=(0, 0, 0))
y = 912
for ln in c["title"]:
    y = grad_text(im, y, ln[1:], 92) if ln.startswith("*") else text(d, y, ln, 92)
d = ImageDraw.Draw(im); text(d, y + 8, c["sub"], 36, (200, 200, 200)); credit(d); save(im)

for i, it in enumerate(cfg["items"], 1):
    im = Image.new("RGB", (W, H))
    im.paste(fill(grab(it["car"], it.get("gamma", 1.0)), W, 680, it.get("cx", 0.5)), (0, 0))
    im.paste(fill(grab(it["map"]), W, 670, it.get("mcx", 0.5)), (0, 680))
    d = ImageDraw.Draw(im); d.rectangle((0, 676, W, 684), fill=(0, 0, 0))
    y = text(d, 548, f"{i}. {it['name']}", 58)
    text(d, y, it["info"], 38, (255, 214, 0))
    y = text(d, 1100, "HEAD HERE", 54); text(d, y, it["where"], 38, (255, 214, 0))
    credit(d); save(im)

e = cfg["end"]; im = fill(grab(e["t"], e.get("gamma", 1.0)), W, H).filter(ImageFilter.GaussianBlur(6))
im = Image.blend(im, Image.new("RGB", (W, H)), 0.45); d = ImageDraw.Draw(im); y = 420
for ln in e["lines"]: y = text(d, y, ln, 74)
y = text(d, y + 40, e["sub"], 40, (255, 214, 0)); credit(d); save(im)
