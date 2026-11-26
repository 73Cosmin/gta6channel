#!/usr/bin/env python3
"""QUOTE CUT (owner ref 2026-11-20, media/references/quote_cut_eli.mp4): low-effort viral format.
Stacked: facecam top (0-620), gameplay below. ONE caption only: the streamer's own (ironic) line in
German quotes + emoji, white text with soft shadow, at the top of the gameplay. The video ends HARD on
the dumb moment (no replay, no end card). Credit + disclaimer small at the bottom.

Usage: /tmp/venv/bin/python tools/quote_cut.py media/configs/<name>.json
Config: {"footage": "...mp4", "start": 0, "end": 6.6, "facecam": [x,y,w,h], "game_crop": [x,y,w,h],
         "quote": "Guck, wie krass das aussieht", "emoji": "😍", "credit": "Clip: @x on Twitch",
         "out": "media/edits/x.mp4"}
"""
import json, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, SEAM = 1080, 1920, 620
FONT = "brand/fonts/TikTokSans-700.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
C = json.load(open(sys.argv[1]))
tmp = tempfile.mkdtemp()


def overlay():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines = f"„{C['quote']}“".split("\n")  # "\n" in the quote = 2 lines (long quotes)
    size = 66
    f = ImageFont.truetype(FONT, size)
    ew = 1.25 * len(C.get("emoji") or "")   # emoji ~1.25 x font size wide each, sits after the last line
    while max(f.getlength(t) + (ew * size + 12 if i == len(lines) - 1 and ew else 0)
              for i, t in enumerate(lines)) > 620 and size > 34:
        size -= 2; f = ImageFont.truetype(FONT, size)
    em = None
    if C.get("emoji"):
        ef = ImageFont.truetype(EMOJI, 109, layout_engine=ImageFont.Layout.BASIC)
        e = Image.new("RGBA", (160 * len(C["emoji"]), 140), (0, 0, 0, 0))
        ImageDraw.Draw(e).text((0, 0), C["emoji"], font=ef, embedded_color=True)
        e = e.crop(e.getbbox()); k = size * 1.05 / e.height
        em = e.resize((int(e.width * k), int(e.height * k)), Image.LANCZOS)
    for i, txt in enumerate(lines):
        last = i == len(lines) - 1
        tw = f.getlength(txt)
        total = tw + (em.width + 12 if em and last else 0)
        x0, y0 = int((W - total) / 2), SEAM + 250 + int(i * size * 1.25)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x0 + 3, y0 + 4), txt, font=f, fill=(0, 0, 0, 200))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(4)))
        d = ImageDraw.Draw(img)
        d.text((x0, y0), txt, font=f, fill="white", stroke_width=2, stroke_fill=(0, 0, 0, 160))
        if em and last:
            img.alpha_composite(em, (int(x0 + tw + 12), y0 + int(size * 0.08)))
    if C.get("credit"):   # tiny bottom-left (owner 2026-11-26: no disclaimer line)
        d.text((24, H - 44), C["credit"], font=ImageFont.truetype(FONT, 20), fill=(255, 255, 255, 150),
               stroke_width=1, stroke_fill=(0, 0, 0, 150))
    p = f"{tmp}/ov.png"; img.save(p); return p


ov = overlay()
s0, s1 = C["start"], C["end"]
fx, fy, fw, fh = C["facecam"]; gc = C.get("game_crop")
gcf = f"crop={gc[2]}:{gc[3]}:{gc[0]}:{gc[1]}," if gc else ""
fc = (f"[0:v]trim={s0}:{s1},setpts=PTS-STARTPTS,fps=30,split[a][b];"
      f"[a]crop={fw}:{fh}:{fx}:{fy},scale={W}:{SEAM}:force_original_aspect_ratio=increase,crop={W}:{SEAM}[top];"
      f"[b]{gcf}scale={W}:{H - SEAM}:force_original_aspect_ratio=increase,crop={W}:{H - SEAM}[bot];"
      f"[top][bot]vstack,format=rgba[st];[st][1:v]overlay=0:0,format=yuv420p[v];"
      f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,aresample=48000,loudnorm=I=-14:TP=-1.5[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", C["footage"], "-i", ov, "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", C["out"]], check=True)
print("ok", C["out"], f"{s1 - s0:.2f}s")
