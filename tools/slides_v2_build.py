#!/usr/bin/env python3
"""SLIDESHOW RECIPE v2 builder: cover (real frame + black band title) + item slides (item frame top, map below) + end slide.
Usage: python3 tools/slides_v2_build.py media/configs/<cfg>.json   (frames are grabbed from cfg["src"] with ffmpeg)"""
from brandmark import slide_mark   # channel watermark (owner 2026-11-28)
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

def from_img(spec):
    # spec = [path, top, bottom] (rows of the source image) - e.g. a car or map half of a reference post image
    path, top, bottom = spec
    im = Image.open(path).convert("RGB")
    k = cfg.get("img_scale", 1)   # e.g. 4 when the crops were measured on the original and path is the x4 upscale
    return im.crop((0, top * k, im.width, bottom * k))

def sharp(im):   # off for AI-upscaled sources ("sharpen": false) - they are already sharp
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2)) if cfg.get("sharpen", True) else im

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

def credit(d):   # tiny bottom-left, no disclaimer (owner 2026-11-26)
    d.text((22, H - 22), cfg["credit"], font=f(18), fill=(190, 190, 190), anchor="ls", stroke_width=1, stroke_fill=(0, 0, 0))

# BRAND (owner 2026-11-26 ~23:40: "man muss merken dass es von meinem account ist"): same pill tag + "NN / TT" counter
# as the card-style cover (tools/slides_card_build.py) on every slide, teal divider between item and map.
TEAL, PILL, WHITE = (94, 230, 200), (18, 15, 24), (250, 246, 238)
B = cfg.get("brand")
TOTAL = len(cfg["items"]) + 2
def brand(d, i):
    if not B:
        return
    ft = f(30); L, R = 64, 1016; w = d.textlength(B["tag"], font=ft)
    d.rounded_rectangle((L, 56, L + w + 56, 112), 28, fill=PILL); d.rectangle((L + 20, 70, L + 26, 98), fill=TEAL)
    d.text((L + 40, 84), B["tag"], font=ft, fill=WHITE, anchor="lm")
    ct = f"{i:02d} / {TOTAL:02d}"; cw = d.textlength(ct, font=ft)
    d.rounded_rectangle((R - cw - 40, 56, R + 8, 112), 28, fill=PILL); d.text((R - 16, 84), ct, font=ft, fill=TEAL, anchor="rm")

n = 0
def save(im):
    slide_mark(im, W // 2, H - 52)   # @ne0nleonida watermark (owner 2026-11-28)
    global n; n += 1; p = f"{out}/{n:02d}.jpg"; im.save(p, quality=97, subsampling=0); print(p)

c = cfg["cover"]; im = Image.new("RGB", (W, H)); im.paste(fill(from_img(c["img"]) if c.get("img") else grab(c["t"], c.get("gamma", 1.0)), W, 900, c.get("cx", 0.5)), (0, 0))
d = ImageDraw.Draw(im); d.rectangle((0, 900, W, H), fill=(0, 0, 0))
y = 912
for ln in c["title"]:
    y = grad_text(im, y, ln[1:], 92) if ln.startswith("*") else text(d, y, ln, 92)
d = ImageDraw.Draw(im); text(d, y + 8, c["sub"], 36, (200, 200, 200)); credit(d); save(im)

for i, it in enumerate(cfg["items"], 1):
    im = Image.new("RGB", (W, H))
    car = from_img(it["car_img"]) if it.get("car_img") else grab(it["car"], it.get("gamma", 1.0))
    mp = from_img(it["map_img"]) if it.get("map_img") else grab(it["map"])
    im.paste(sharp(fill(car, W, 680, it.get("cx", 0.5))), (0, 0))
    im.paste(sharp(fill(mp, W, 670, it.get("mcx", 0.5))), (0, 680))
    d = ImageDraw.Draw(im); d.rectangle((0, 676, W, 684), fill=TEAL if B else (0, 0, 0)); brand(d, i + 1)
    y = text(d, 548 if it.get("info") else 590, f"{i}. {it['name']}", 58)
    if it.get("info"):
        text(d, y, it["info"], 38, (255, 214, 0))
    y = text(d, 1100, "HEAD HERE", 54); text(d, y, it["where"], 38, (255, 214, 0))
    credit(d); save(im)

e = cfg["end"]; im = fill(from_img(e["img"]) if e.get("img") else grab(e["t"], e.get("gamma", 1.0)), W, H).filter(ImageFilter.GaussianBlur(6))
im = Image.blend(im, Image.new("RGB", (W, H)), 0.45); d = ImageDraw.Draw(im); y = 420
for ln in e["lines"]: y = text(d, y, ln, 74)
y = text(d, y + 40, e["sub"], 40, (255, 214, 0)); brand(d, TOTAL); credit(d); save(im)
