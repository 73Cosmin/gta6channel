#!/usr/bin/env python3
"""TikTok photo-mode slideshow: 1080x1920 slides, official trailer frame on top, bold text in the safe zone.
Usage: python3 tools/slides_build.py media/configs/<name>.json"""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
cfg = json.load(open(sys.argv[1])); out = cfg["out_dir"]; os.makedirs(out, exist_ok=True)
F = "brand/fonts/TikTokSans-800.ttf"; f = lambda s: ImageFont.truetype(F, s)
W, H = 1080, 1920; YEL, RED, WHITE = (255, 214, 0), (255, 59, 48), (255, 255, 255)

def frame(t):
    p = f"/tmp/_sl_{t}.png"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", cfg["video"], "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB")

def bg(t):
    im = frame(t); bw = im.resize((int(im.width * H / im.height), H)).filter(ImageFilter.GaussianBlur(30))
    x = (bw.width - W) // 2; base = bw.crop((x, 0, x + W, H))
    base = Image.blend(base, Image.new("RGB", (W, H), (0, 0, 0)), 0.55)
    bh = 860; band = im.resize((int(im.width * bh / im.height), bh)); x = (band.width - W) // 2
    base.paste(band.crop((x, 0, x + W, bh)), (0, 0)); return base, bh

def ctext(d, y, s, font, fill, maxw=620):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    for ln in lines:
        d.text((W // 2, y), ln, font=font, fill=fill, anchor="mt", stroke_width=6, stroke_fill=(0, 0, 0))
        y += int(font.size * 1.12)
    return y

def box(d, y, s, font, fg=(0, 0, 0), bgc=WHITE):
    w = d.textlength(s, font=font); pad = 24
    d.rounded_rectangle((W/2 - w/2 - pad, y, W/2 + w/2 + pad, y + font.size + 30), 22, fill=bgc)
    d.text((W // 2, y + 15), s, font=font, fill=fg, anchor="mt"); return y + font.size + 44

for i, sl in enumerate(cfg["slides"], 1):
    im, ybot = bg(sl["t"]); d = ImageDraw.Draw(im); y = ybot + 50
    if sl.get("cover"):
        for ln in sl["title"]: y = box(d, y, ln, f(78))
        y = ctext(d, y + 30, sl["sub"], f(54), YEL)
    else:
        for tip in sl["tips"]:
            y = ctext(d, y, tip["num"] + " " + tip["head"], f(64), YEL)
            y = ctext(d, y + 8, tip["how"], f(46), WHITE) + 50
        if sl.get("cta"): ctext(d, max(y, 1330), sl["cta"], f(50), RED)
    d.text((22, H - 22), cfg["credit"], font=f(18), fill=(190, 190, 190), anchor="ls", stroke_width=1, stroke_fill=(0, 0, 0))  # tiny, no disclaimer (owner 2026-11-26)
    p = f"{out}/{i:02d}.jpg"; im.save(p, quality=92); print(p)
