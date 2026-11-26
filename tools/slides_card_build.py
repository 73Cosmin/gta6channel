#!/usr/bin/env python3
"""Card-style 4:5 TikTok slideshow (owner ref: the 3.5K '10 hidden controls' slideshow). Bright image on top that
fades into dark navy, pill tag, giant headline, teal-accent cards / checklist rows, credit + 'save' footer.
Usage: python3 tools/slides_card_build.py media/configs/<name>.json"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
C = json.load(open(sys.argv[1])); out = C["out_dir"]; os.makedirs(out, exist_ok=True)
F8, F7 = "brand/fonts/TikTokSans-800.ttf", "brand/fonts/TikTokSans-700.ttf"
f8 = lambda s: ImageFont.truetype(F8, s); f7 = lambda s: ImageFont.truetype(F7, s)
W, H = 1080, 1350; BG = (20, 17, 28); CARD = (34, 29, 46); TEAL = (94, 230, 200); WHITE = (250, 246, 238); GREY = (190, 186, 200)
L, R = 64, 1016
N = C.get("total", len(C["slides"]))   # "total"/"start": build a single cover for a longer slideshow
def grab(t):
    p = f"/tmp/_card_{t}.png"
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(t), "-i", C["video"], "-frames:v", "1", p], check=True)
    return Image.open(p).convert("RGB")
def top_image(src, h, cx=None):
    s = max(W / src.width, h / src.height); im = src.resize((int(src.width * s) + 1, int(src.height * s) + 1))
    x = (im.width - W) // 2 if cx is None else int((im.width - W) * cx); y = (im.height - h) // 2; return im.crop((x, y, x + W, y + h))
def fade(base, y0, y1):
    ov = Image.new("RGB", (W, H), BG); m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    for y in range(y0, H): d.line((0, y, W, y), fill=min(255, int(255 * (y - y0) / max(1, y1 - y0))))
    return Image.composite(ov, base, m)
def wrap(d, s, font, maxw):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def pill(d, i):
    ft = f8(30); w = d.textlength(C["tag"], font=ft)
    d.rounded_rectangle((L, 56, L + w + 56, 112), 28, fill=(18, 15, 24)); d.rectangle((L + 20, 70, L + 26, 98), fill=TEAL)
    d.text((L + 40, 84), C["tag"], font=ft, fill=WHITE, anchor="lm")
    ct = f"{i:02d} / {N:02d}"; cw = d.textlength(ct, font=f8(30))
    d.rounded_rectangle((R - cw - 40, 56, R + 8, 112), 28, fill=(18, 15, 24))  # dark pill so the counter reads on bright images
    d.text((R - 16, 84), ct, font=f8(30), fill=TEAL, anchor="rm")
def footer(d):
    d.line((L, 1262, R, 1262), fill=(70, 64, 86), width=2)
    d.text((22, H - 22), C["credit"], font=f7(18), fill=GREY, anchor="ls")   # tiny source, bottom-left (owner 2026-11-26)
    d.text((R, 1296), C["save"], font=f8(28), fill=TEAL, anchor="rm")
for i, sl in enumerate(C["slides"], C.get("start", 1)):
    src = Image.open(sl["img"]).convert("RGB") if sl.get("img") else grab(sl["t"])
    if sl.get("cover") or sl.get("end"):
        im = Image.new("RGB", (W, H), BG); im.paste(top_image(src, 820, sl.get('crop_x')), (0, 0)); im = fade(im, 560, 860); d = ImageDraw.Draw(im); pill(d, i)
        y = 830; d.text((L, y), sl["h1"], font=f8(116), fill=WHITE, anchor="lt"); y += 132
        fh = f8(116)
        while d.textlength(sl["h2"], font=fh) > R - L: fh = f8(fh.size - 4)
        d.text((L, y), sl["h2"], font=fh, fill=TEAL, anchor="lt"); y += fh.size + 40
        for ln in wrap(d, sl["sub"], f7(40), R - L): d.text((L, y), ln, font=f7(40), fill=WHITE, anchor="lt"); y += 52
        if sl.get("swipe"): d.text((L, y + 30), sl["swipe"], font=f8(32), fill=TEAL, anchor="lt")
        footer(d); im.save(f"{out}/{i:02d}.jpg", quality=93); print(i); continue
    if sl.get("full"):  # whole screenshot/map on a card (owner 2026-11-23: map slideshow), fit into y 132-1240
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); pill(d, i)
        bh = 1240 - 132; s = min((R - L) / src.width, bh / src.height); w, h = int(src.width * s), int(src.height * s)
        x, y = (W - w) // 2, 132 + (bh - h) // 2
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 22, fill=255)
        d.rounded_rectangle((x - 4, y - 4, x + w + 3, y + h + 3), 26, fill=TEAL); im.paste(src.resize((w, h)), (x, y), m)
        footer(ImageDraw.Draw(im)); im.save(f"{out}/{i:02d}.jpg", quality=93); print(i); continue
    if sl.get("step"):  # owner 2026-11-25: image = top half, big instruction text = bottom half (no empty space)
        ih = 640; im = Image.new("RGB", (W, H), BG); im.paste(top_image(src, ih), (0, 0)); im = fade(im, ih - 160, ih + 10)
        d = ImageDraw.Draw(im); pill(d, i)
        hf = f8(84)
        while d.textlength(sl["head"], font=hf) > R - L: hf = f8(hf.size - 4)
        bs = 56
        while bs > 34 and (len(wrap(d, sl["body"], f7(bs), R - L)) * int(bs * 1.32) > 1236 - (ih + 140 + hf.size)): bs -= 2
        blk = 64 + hf.size + 70 + len(wrap(d, sl["body"], f7(bs), R - L)) * int(bs * 1.32)
        y = ih + 6 + max(0, (1236 - ih - 6 - blk) // 2)  # centre the text block in the lower half
        d.text((L, y), sl["step"], font=f8(44), fill=TEAL, anchor="lt"); y += 64
        d.text((L, y), sl["head"], font=hf, fill=WHITE, anchor="lt"); y += hf.size + 30
        d.rectangle((L, y, L + 120, y + 6), fill=TEAL); y += 34
        for ln in wrap(d, sl["body"], f7(bs), R - L): d.text((L, y), ln, font=f7(bs), fill=WHITE, anchor="lt"); y += int(bs * 1.32)
        footer(d); im.save(f"{out}/{i:02d}.jpg", quality=93); print(i); continue
    lst = sl.get("list"); n = len(lst) if lst else 0
    ih = 660 if not lst else (600 if n <= 4 else 380 if n <= 8 else 250)
    im = Image.new("RGB", (W, H), BG); im.paste(top_image(src, ih), (0, 0)); im = fade(im, ih - 220, ih); d = ImageDraw.Draw(im); pill(d, i)
    bf = f8(110 if lst and n > 8 else 128)
    while d.textlength(sl["big"], font=bf) > R - L: bf = f8(bf.size - 6)
    y = ih - bf.size - 10; d.text((L, y), sl["big"], font=bf, fill=WHITE, anchor="lt", stroke_width=3, stroke_fill=BG)
    y = ih + 22; d.rectangle((L, y, R, y + 5), fill=TEAL); y += 36
    if lst:
        rh = 60 if n <= 4 else 54 if n <= 8 else 52
        kf = f8(36 if n > 8 else 40); lf = f7(32 if n > 8 else 36)
        kw = max(d.textlength(k, font=kf) for k, _ in lst) + 30
        box_h = n * rh + 40 if n > 4 else sum(rh * len(wrap(d, v, lf, R - L - 60 - kw)) + 26 for _, v in lst) + 20
        d.rounded_rectangle((L, y, R, y + box_h), 22, fill=CARD); d.rectangle((L, y, L + 7, y + box_h), fill=TEAL)
        yy = y + 22
        for k, v in lst:
            d.text((L + 34, yy + 4), k, font=kf, fill=TEAL, anchor="lt")
            lines = wrap(d, v, lf, R - L - 60 - kw)
            if n > 4: lines = [lines[0] if len(lines) == 1 else v]
            for ln in lines: d.text((L + 34 + kw, yy + 8), ln, font=lf, fill=WHITE, anchor="lt"); yy += rh
            if n <= 4: yy += 26
    else:
        for k, head, body in sl["items"]:
            kf = f8(64); hf = f8(42); bfnt = f7(36); kw = d.textlength(k, font=kf) + 30
            lines = wrap(d, body, bfnt, R - L - 70 - kw); hh = 60 + len(lines) * 48 + 50
            d.rounded_rectangle((L, y, R, y + hh), 22, fill=CARD); d.rectangle((L, y, L + 7, y + hh), fill=TEAL)
            d.text((L + 34, y + 30), k, font=kf, fill=TEAL, anchor="lt")
            d.text((L + 34 + kw, y + 32), head, font=hf, fill=WHITE, anchor="lt")
            yy = y + 92
            for ln in lines: d.text((L + 34 + kw, yy), ln, font=bfnt, fill=GREY, anchor="lt"); yy += 48
            y += hh + 26
    footer(d); im.save(f"{out}/{i:02d}.jpg", quality=93); print(i)
