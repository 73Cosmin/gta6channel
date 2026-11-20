#!/usr/bin/env python3
"""TOP-5 ranking compilation (owner refs media/references/top5/, 2026-11-20).

Layout 1080x1920: black header (y 0-300) with coloured title words + teaser line, below it the
clips in stacked layout (facecam y 300-1000, gameplay y 1000-1920). Ranking list 1.-5. on the left
(coloured numbers, labels appear as the countdown 5 -> 1 reaches them). One-word yellow captions,
per-clip credit + fan-page disclaimer, music bed under the original audio, loudnorm -14 LUFS.

Config: {"title": [[["RANKING THE ","white"],["FUNNIEST","green"]], [["GTA 6 ","pink"],["FAILS","blue"]]],
  "teaser": "(#1 IS PURE EVIL)", "music": "...", "out": "...",
  "items": [ {"rank":5, "label":"Seaplane", "footage":"...cut.mp4", "start":0, "end":12.5,
              "facecam":[x,y,w,h], "game_crop":[x,y,w,h] or null, "words":[[w,s,e],...] (times in the cut),
              "red_words":[...], "credit":"Clip: @x on Twitch"}, ... ]}   # items in play order (5 first)
Usage: python3 tools/top5_build.py media/configs/<name>.json   (run with /tmp/venv/bin/python if PIL is broken)
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

C = json.load(open(sys.argv[1]))
FB = "brand/fonts/TikTokSans-800.ttf"
COL = {"white": (255, 255, 255), "green": (60, 230, 60), "pink": (255, 40, 170), "blue": (40, 150, 255),
       "yellow": (255, 220, 0), "red": (230, 30, 30), "orange": (255, 140, 20), "grey": (150, 150, 150)}
NUMCOL = {1: "red", 2: "yellow", 3: "orange", 4: "grey", 5: "white"}
W, H, HEAD, SEAM = 1080, 1920, 300, 1000
tmp = tempfile.mkdtemp(prefix="top5_")


def font(sz):
    return ImageFont.truetype(FB, sz)


def line_img(d, parts, y, sz, maxw=1020):
    f = font(sz)
    while sum(d.textlength(t, font=f) for t, _ in parts) > maxw and sz > 30:
        sz -= 2; f = font(sz)
    x = (W - sum(d.textlength(t, font=f) for t, _ in parts)) / 2
    for t, c in parts:
        d.text((x, y), t, font=f, fill=COL[c], stroke_width=3, stroke_fill=(0, 0, 0))
        x += d.textlength(t, font=f)


# header
hd = Image.new("RGBA", (W, HEAD), (0, 0, 0, 255)); d = ImageDraw.Draw(hd)
t = C["title"]
line_img(d, t[0], 22, 92)
line_img(d, t[1], 122, 92)
line_img(d, [[C.get("teaser", ""), "green"]], 232, 46)
hd.save(f"{tmp}/head.png")

items = C["items"]
labels = {it["rank"]: it["label"] for it in items}


def list_png(revealed, cur, path):
    im = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn, fl = font(70), font(56)
    for k, r in enumerate([1, 2, 3, 4, 5]):
        y = k * 82
        d.text((36, y), f"{r}.", font=fn, fill=COL[NUMCOL[r]], stroke_width=5, stroke_fill=(0, 0, 0))
        if r in revealed:
            fill = COL["yellow"] if r == cur else COL["white"]
            d.text((130, y + 10), labels[r], font=fl, fill=fill, stroke_width=5, stroke_fill=(0, 0, 0))
    im.save(path)


def esc(s):
    return (s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%"))


segs, revealed = [], []
for i, it in enumerate(items):
    revealed.append(it["rank"])
    lp = f"{tmp}/list{i}.png"; list_png(revealed, it["rank"], lp)
    cr = Image.new("RGBA", (W, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(cr)
    for k, s in enumerate([it["credit"], "Fan page. Not affiliated with Rockstar Games."]):
        f = font(34 if k == 0 else 28)
        d.text(((W - d.textlength(s, font=f)) / 2, k * 46), s, font=f, fill=(255, 255, 255),
               stroke_width=3, stroke_fill=(0, 0, 0))
    cp = f"{tmp}/cred{i}.png"; cr.save(cp)
    s0, s1 = it["start"], it["end"]; dur = s1 - s0
    fx, fy, fw, fh = it["facecam"]
    gc = it.get("game_crop")
    gcf = f"crop={gc[2]}:{gc[3]}:{gc[0]}:{gc[1]}," if gc else ""
    red = {w.upper() for w in it.get("red_words", [])}
    dr = []
    for w, a, b in it["words"]:
        if b < s0 or a > s1:
            continue
        txt = w.upper().strip(".,!?…\"")
        c = "0xFF2A2A" if txt in red else "0xFFE600"
        dr.append(f"drawtext=fontfile={FB}:text='{esc(txt)}':fontsize=96:fontcolor={c}:borderw=8:bordercolor=black:"
                  f"x=(w-tw)/2:y=1520-th/2:enable='between(t,{max(0,a-s0):.2f},{b-s0:.2f})'")
    cap = ("," + ",".join(dr)) if dr else ""
    fc = (f"[0:v]trim={s0}:{s1},setpts=PTS-STARTPTS,fps=30,split[a][b];"
          f"[a]crop={fw}:{fh}:{fx}:{fy},scale={W}:{SEAM-HEAD}:force_original_aspect_ratio=increase,crop={W}:{SEAM-HEAD}[top];"
          f"[b]{gcf}scale={W}:{H-SEAM}:force_original_aspect_ratio=increase,crop={W}:{H-SEAM}[bot];"
          f"color=black:s={W}x{H}:r=30:d={dur:.3f}[bg];"
          f"[bg][top]overlay=0:{HEAD}[v1];[v1][bot]overlay=0:{SEAM}[v2];"
          f"[v2][1:v]overlay=0:0[v3];[v3][2:v]overlay=0:1030[v4];[v4][3:v]overlay=0:1690{cap}[v];"
          f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a]")
    out = f"{tmp}/seg{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", it["footage"], "-i", f"{tmp}/head.png", "-i", lp, "-i", cp,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "19",
                    "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)
    segs.append(out)

lst = f"{tmp}/list.txt"
open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
joined = f"{tmp}/joined.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                       joined]).decode())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-stream_loop", "-1", "-i", C["music"], "-filter_complex",
                f"[1:a]volume=0.16,atrim=0:{total:.3f}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,"
                "loudnorm=I=-14:TP=-1.5:LRA=11[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", C["out"]], check=True)
print("ok", C["out"], f"{total:.2f}s")
