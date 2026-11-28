#!/usr/bin/env python3
"""NEON slideshow builder (owner 2026-11-28: 'mach es in den Farben und Stil hiervon' = x.com/mtshojib420 'PERMANENT stat
upgrades', 528K views / 14.7K bookmarks). Vice City synthwave look: blurred purple/pink background frame, big cream
Barlow Condensed titles with shadow, slanted colour stripe, ONE accent colour per item, dark translucent info cards with a
coloured icon + label, bottom nav row of all items (current one highlighted). Our brand pill + counter stay on every slide.

Usage: python3 tools/slides_neon_build.py media/configs/<name>.json
config: {"out_dir", "tag", "credit", "bg": [video, t] | image path,
         "cover": {"h1": [..2 lines], "sub", "swipe"},
         "items": [{"img": [path, x0, y0, x1, y1], "color": "#hex", "kicker", "title", "cards": [[label, text, icon], ..]}],
         "end": {"h1": [..], "sub"}}
icon = pin | dot | check | eye | warn
"""
from brandmark import video_mark, slide_mark, mark_png   # channel watermark (owner 2026-11-28)
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

C = json.load(open(sys.argv[1])); out = C["out_dir"]; os.makedirs(out, exist_ok=True)
W, H = 1080, 1350
FX, FB, FS = ("brand/fonts/BarlowCondensed-ExtraBold.ttf", "brand/fonts/BarlowCondensed-Bold.ttf",
              "brand/fonts/BarlowCondensed-SemiBold.ttf")
fx = lambda s: ImageFont.truetype(FX, s); fb = lambda s: ImageFont.truetype(FB, s); fs = lambda s: ImageFont.truetype(FS, s)
CREAM = (250, 240, 225); CARD = (28, 22, 52, 215); NAVY = (24, 18, 46)
hexc = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
items = C["items"]; N = len(items) + 2


def background():
    b = C["bg"]
    if isinstance(b, list):
        p = "/tmp/_neon_bg.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(b[1]), "-i", b[0], "-frames:v", "1", p], check=True)
        src = Image.open(p).convert("RGB")
    else:
        src = Image.open(b).convert("RGB")
    s = max(W / src.width, H / src.height); src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    x = (src.width - W) // 2; src = src.crop((x, 0, x + W, H)).filter(ImageFilter.GaussianBlur(9))
    src = ImageEnhance.Color(src).enhance(1.3)
    # synthwave tint: violet top -> magenta mid -> deep blue bottom
    grad = Image.new("RGB", (W, H)); g = ImageDraw.Draw(grad)
    stops = [(0, (70, 52, 140)), (0.45, (120, 60, 140)), (1, (30, 30, 90))]
    for y in range(H):
        t = y / H
        for (a, ca), (b2, cb) in zip(stops, stops[1:]):
            if a <= t <= b2:
                k = (t - a) / (b2 - a); g.line((0, y, W, y), fill=tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
    return Image.blend(src, grad, 0.55)


BG = background()


def shadow_text(im, xy, txt, font, fill, anchor="mt", off=6):
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.text((xy[0] + off * 0.5, xy[1] + off), txt, font=font, fill=(10, 6, 30, 190), anchor=anchor)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(im).text(xy, txt, font=font, fill=fill, anchor=anchor)


def stripe(im, y, col, w=760, h=26):
    d = ImageDraw.Draw(im); x0 = (W - w) // 2
    d.polygon([(x0 + 24, y), (x0 + w, y), (x0 + w - 24, y + h), (x0, y + h)], fill=col)


def brand(im, i):
    d = ImageDraw.Draw(im); ft = fb(30); tag = C["tag"]; w = d.textlength(tag, font=ft)
    d.rounded_rectangle((40, 30, 40 + w + 52, 78), 24, fill=(18, 12, 38, 230), outline=(255, 110, 190), width=2)
    d.rectangle((58, 42, 63, 66), fill=(255, 110, 190)); d.text((76, 54), tag, font=ft, fill=CREAM, anchor="lm")
    ct = f"{i:02d} / {N:02d}"; cw = d.textlength(ct, font=fb(30))
    d.rounded_rectangle((W - 40 - cw - 40, 30, W - 40, 78), 24, fill=(18, 12, 38, 230)); d.text((W - 60, 54), ct, font=fb(30), fill=(255, 210, 90), anchor="rm")
    slide_mark(im, W // 2, 54, size=26)   # @ne0nleonida watermark (owner 2026-11-28)
    d.text((22, H - 12), C["credit"], font=fs(19), fill=(220, 210, 235, 150), anchor="ls")


def crop_img(spec):
    p, x0, y0, x1, y1 = spec
    return Image.open(p).convert("RGB").crop((x0, y0, x1, y1))


def fit(img, w, h):
    s = max(w / img.width, h / img.height); img = img.resize((int(img.width * s) + 1, int(img.height * s) + 1), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2; return img.crop((x, y, x + w, y + h))


def circle(img, r, col, ring=7, glow=False):
    size = 2 * r + 2 * ring; c = Image.new("RGBA", (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse((0, 0, size - 1, size - 1), fill=col); m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    c.paste(fit(img, 2 * r, 2 * r), (ring, ring), m)
    return c


def icon(d, kind, cx, cy, col):
    if kind == "pin":
        d.ellipse((cx - 16, cy - 26, cx + 16, cy + 6), fill=col); d.polygon([(cx - 13, cy - 2), (cx + 13, cy - 2), (cx, cy + 24)], fill=col)
        d.ellipse((cx - 6, cy - 16, cx + 6, cy - 4), fill=NAVY)
    elif kind == "check":
        d.line([(cx - 18, cy), (cx - 5, cy + 14), (cx + 20, cy - 16)], fill=CREAM, width=8, joint="curve")
    elif kind == "eye":
        d.ellipse((cx - 24, cy - 13, cx + 24, cy + 13), outline=col, width=5); d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=col)
    elif kind == "warn":
        d.polygon([(cx, cy - 22), (cx + 22, cy + 18), (cx - 22, cy + 18)], fill=col); d.rectangle((cx - 2, cy - 8, cx + 2, cy + 6), fill=NAVY)
        d.ellipse((cx - 3, cy + 9, cx + 3, cy + 14), fill=NAVY)
    else:
        d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=col)


def wrap(d, s, font, maxw):
    lines, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]


def nav(im, cur):
    n = len(items); sz = 88; gap = 22; x = (W - (n * sz + (n - 1) * gap)) // 2; y = 1214
    d = ImageDraw.Draw(im)
    for k, it in enumerate(items):
        col = hexc(it["color"]); on = k == cur
        d.rounded_rectangle((x, y, x + sz, y + sz), 18, fill=(22, 16, 44, 235), outline=col if on else None, width=5 if on else 0)
        th = circle(crop_img(it["img"]), 28, col + (255,), ring=4)
        if not on: th = Image.blend(Image.new("RGBA", th.size, (0, 0, 0, 0)), th, 0.6)
        im.alpha_composite(th, (x + (sz - th.width) // 2, y + (sz - th.height) // 2)); x += sz + gap


def save(im, i):
    im.convert("RGB").save(f"{out}/{i:02d}.jpg", quality=97, subsampling=0); print(i)


def circles_row(im, y0, r=98, dy=270):
    pos = [(W * 0.22, y0), (W * 0.5, y0), (W * 0.78, y0), (W * 0.22, y0 + dy), (W * 0.5, y0 + dy), (W * 0.78, y0 + dy)]
    d = ImageDraw.Draw(im)
    for k, (it, (cx, cy)) in enumerate(zip(items, pos)):
        c = circle(crop_img(it["img"]), r, hexc(it["color"]) + (255,))
        im.alpha_composite(c, (int(cx - c.width / 2), int(cy - c.height / 2)))
        shadow_text(im, (cx, cy + c.height / 2 + 6), f"{k + 1:02d}", fx(46), CREAM, off=4)


# 1) cover. OWNER 2026-11-28: covers with OFFICIAL GTA VI ARTWORK perform best (Platinum 278K with Lucia artwork,
#    Hurricane 37K with Jason) -> "art": "brand/artwork/<name>.jpg" (+ "art_y" 0..1 vertical crop) = full-bleed artwork,
#    title on a dark top fade, one row of item circles on a dark bottom fade.
cv = C["cover"]
if cv.get("art"):
    a = Image.open(cv["art"]).convert("RGB"); s_ = W / a.width; a = a.resize((W, int(a.height * s_)), Image.LANCZOS)
    y0 = int((a.height - H) * cv.get("art_y", 0.35)); im = a.crop((0, y0, W, y0 + H)).convert("RGBA")
    fade = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fade)
    for yy in range(H):
        al = max(0, 1 - yy / 470) * 215 if yy < 470 else max(0, (yy - 960) / 390) * 235
        fd.line((0, yy, W, yy), fill=(20, 12, 44, int(al)))
    im.alpha_composite(fade); brand(im, 1)
    y = 112
    for ln in cv["h1"]:
        f = fx(140)
        while ImageDraw.Draw(im).textlength(ln, font=f) > W - 110: f = fx(f.size - 4)
        shadow_text(im, (W / 2, y), ln, f, CREAM, off=8); y += int(f.size * 0.92)
    stripe(im, y + 14, (255, 95, 175)); y += 62
    shadow_text(im, (W / 2, y), cv["sub"], fb(46), (255, 210, 90), off=3)
    n_ = len(items); r_ = 58; sp = (W - 120) / n_
    for k, it in enumerate(items):
        c = circle(crop_img(it["img"]), r_, hexc(it["color"]) + (255,), ring=6); cx = 60 + sp * (k + 0.5)
        im.alpha_composite(c, (int(cx - c.width / 2), 1068)); shadow_text(im, (cx, 1068 + c.width + 2), f"{k + 1:02d}", fx(36), CREAM, off=3)
    sy = 1250
else:
    im = BG.convert("RGBA"); brand(im, 1)
    y = 120
    for ln in cv["h1"]:
        f = fx(150)
        while ImageDraw.Draw(im).textlength(ln, font=f) > W - 120: f = fx(f.size - 4)
        shadow_text(im, (W / 2, y), ln, f, CREAM, off=8); y += int(f.size * 0.92)
    stripe(im, y + 18, (255, 95, 175)); y += 70
    shadow_text(im, (W / 2, y), cv["sub"], fb(46), (255, 210, 90), off=3)
    circles_row(im, y + 200); sy = 1225
shadow_text(im, (W / 2 - 40, sy), cv["swipe"], fx(64), CREAM, off=5)
d = ImageDraw.Draw(im); ax = W / 2 - 40 + ImageDraw.Draw(im).textlength(cv["swipe"], font=fx(64)) / 2 + 24
d.line((ax, sy + 37, ax + 70, sy + 37), fill=CREAM, width=9); d.polygon([(ax + 92, sy + 37), (ax + 64, sy + 17), (ax + 64, sy + 57)], fill=CREAM)
save(im, 1)

# 2) items
for k, it in enumerate(items):
    col = hexc(it["color"]); im = BG.convert("RGBA"); brand(im, k + 2); d = ImageDraw.Draw(im)
    pic = fit(crop_img(it["img"]), 940, 410); x0, y0 = (W - 940) // 2, 100
    d.rounded_rectangle((x0 - 7, y0 - 7, x0 + 947, y0 + 417), 32, fill=col)
    m = Image.new("L", pic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 939, 409), 26, fill=255); im.paste(pic, (x0, y0), m)
    y = 532
    shadow_text(im, (W / 2, y), f"{k + 1:02d} · {it['kicker']}", fb(40), col, off=3); y += 50
    f = fx(118)
    while d.textlength(it["title"], font=f) > W - 110: f = fx(f.size - 4)
    shadow_text(im, (W / 2, y), it["title"], f, CREAM, off=7); y += int(f.size * 0.95)
    stripe(im, y, col, w=700, h=22); y += 46
    cf = fs(35); lf = fb(30)
    for lab, txt, ic in it["cards"]:
        lines = wrap(d, txt.upper(), cf, 940 - 150)
        ch = 20 + 34 + len(lines) * 38 + 16
        card = Image.new("RGBA", (940, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 939, ch - 1), 22, fill=CARD); im.alpha_composite(card, (x0, y))
        d = ImageDraw.Draw(im); icon(d, ic, x0 + 52, y + ch // 2, col); d.line((x0 + 100, y + 22, x0 + 100, y + ch - 22), fill=CREAM, width=3)
        d.text((x0 + 124, y + 18), lab.upper(), font=lf, fill=col)
        yy = y + 54
        for ln in lines: d.text((x0 + 124, yy), ln, font=cf, fill=CREAM); yy += 38
        y += ch + 14
    nav(im, k); save(im, k + 2)

# 3) end
e = C["end"]; im = BG.convert("RGBA"); brand(im, N)
y = 140
for ln in e["h1"]:
    f = fx(130)
    while ImageDraw.Draw(im).textlength(ln, font=f) > W - 110: f = fx(f.size - 4)
    shadow_text(im, (W / 2, y), ln, f, CREAM, off=8); y += int(f.size * 0.93)
stripe(im, y + 16, (255, 95, 175)); y += 66
d = ImageDraw.Draw(im)
for ln in wrap(d, e["sub"].upper(), fb(44), W - 160):
    shadow_text(im, (W / 2, y), ln, fb(44), (255, 210, 90), off=3); y += 52
circles_row(im, y + 150, r=82, dy=235)
shadow_text(im, (W / 2, 1225), e.get("cta", "SAVE THIS FOR LATER"), fx(64), CREAM, off=5)
save(im, N)
