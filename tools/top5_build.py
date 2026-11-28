#!/usr/bin/env python3
"""TOP-5 ranking compilation (owner refs media/references/top5/, 2026-11-20).

Layout 1080x1920 (TikTok-SAFE since 2026-11-20 23:51): facecam full-width top (y 0-760), coloured title words in
rounded black boxes on the seam (+ green teaser), gameplay below (760-1920). Everything important inside x 120-860. Ranking list 1.-5. on the left
(coloured numbers, labels appear as the countdown 5 -> 1 reaches them). One-word yellow captions,
per-clip credit (tiny, bottom-left), music bed under the original audio, loudnorm -14 LUFS.

Config: {"title": [[["RANKING THE ","white"],["FUNNIEST","green"]], [["GTA 6 ","pink"],["FAILS","blue"]]],
  "teaser": "(#1 IS PURE EVIL)", "music": "...", "out": "...",
  "items": [ {"rank":5, "label":"Seaplane", "footage":"...cut.mp4", "start":0, "end":12.5,
              "facecam":[x,y,w,h], "game_crop":[x,y,w,h] or null, "words":[[w,s,e],...] (times in the cut),
              "red_words":[...], "credit":"Clip: @x on Twitch"}, ... ]}   # items in play order (5 first)
Usage: python3 tools/top5_build.py media/configs/<name>.json   (run with /tmp/venv/bin/python if PIL is broken)
"""
from brandmark import video_mark, slide_mark, mark_png   # channel watermark (owner 2026-11-28)
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

C = json.load(open(sys.argv[1]))
FB = "brand/fonts/TikTokSans-800.ttf"
COL = {"white": (255, 255, 255), "green": (60, 230, 60), "pink": (255, 40, 170), "blue": (40, 150, 255),
       "yellow": (255, 220, 0), "red": (230, 30, 30), "orange": (255, 140, 20), "grey": (150, 150, 150)}
NUMCOL = {1: "red", 2: "yellow", 3: "orange", 4: "grey", 5: "white"}
W, H = 1080, 1920
# TikTok SAFE LAYOUT (owner 2026-11-20 23:51: title + list were cut off). Phones (19.5:9) crop ~100 px off EACH
# side of a 1080x1920 video; the search bar covers y~140-230, the caption/username y>~1560, the buttons x>~860.
# -> no black header any more: facecam full-width top (0-SEAM), title in rounded black boxes ON the seam,
#    gameplay below, list at x>=130 / y 990-1350, captions y 1440, credit y 1490 - all inside x 120-860.
HEAD, SEAM = 0, 760
SAFE_L, SAFE_R = 120, 860
tmp = tempfile.mkdtemp(prefix="top5_")


def font(sz):
    return ImageFont.truetype(FB, sz)


def line_img(d, parts, y, sz, maxw=SAFE_R - SAFE_L - 40, box=True):
    f = font(sz)
    while sum(d.textlength(t, font=f) for t, _ in parts) > maxw and sz > 30:
        sz -= 2; f = font(sz)
    tw = sum(d.textlength(t, font=f) for t, _ in parts)
    x = (SAFE_L + SAFE_R - tw) / 2          # centre of the SAFE zone (= frame centre)
    if box:
        d.rounded_rectangle((x - 22, y - 8, x + tw + 22, y + sz + 14), radius=18, fill=(0, 0, 0, 235))
    for t, c in parts:
        d.text((x, y), t, font=f, fill=COL[c], stroke_width=2, stroke_fill=(0, 0, 0))
        x += d.textlength(t, font=f)
    return sz


# title overlay on the facecam/gameplay seam (full-frame transparent PNG)
hd = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hd)
t = C["title"]
line_img(d, t[0], SEAM - 112, 72)
line_img(d, t[1], SEAM - 18, 72)
if C.get("teaser"):
    line_img(d, [[C["teaser"], "green"]], SEAM + 76, 44)
hd.save(f"{tmp}/head.png")

items = C["items"]
labels = {it["rank"]: it["label"] for it in items}


def list_png(revealed, cur, path):
    im = Image.new("RGBA", (W, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    fn = font(60)
    for k, r in enumerate(C.get("slots", [1, 2, 3, 4, 5])):  # "slots": ["A","B"] = versus mode
        y = k * 72
        d.text((SAFE_L + 10, y), f"{r}.", font=fn, fill=COL[C.get("slot_colors", {}).get(str(r), NUMCOL.get(r, "yellow"))],
               stroke_width=5, stroke_fill=(0, 0, 0))
        if r in revealed:
            fill = COL["yellow"] if r == cur else COL["white"]
            sz = 48; fl = font(sz)
            while d.textlength(labels[r], font=fl) > SAFE_R - (SAFE_L + 95) and sz > 28:
                sz -= 2; fl = font(sz)
            d.text((SAFE_L + 95, y + 8 + (48 - sz) // 2), labels[r], font=fl, fill=fill, stroke_width=5, stroke_fill=(0, 0, 0))
    im.save(path)


def esc(s):
    return (s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace(",", "\\,").replace("%", "\\%"))


segs, revealed = [], []
for i, it in enumerate(items):
    revealed.append(it["rank"])
    lp = f"{tmp}/list{i}.png"; list_png(revealed, it["rank"], lp)
    cr = Image.new("RGBA", (W, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(cr)
    # tiny bottom-left credit, no disclaimer (owner 2026-11-26); the strip is placed as before, text sits left/bottom
    d.text((24, 50), it["credit"], font=font(20), fill=(255, 255, 255, 150), stroke_width=1, stroke_fill=(0, 0, 0, 150))
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
        cs = 88
        while cs > 48 and font(cs).getlength(txt) + 16 > 620:   # stay clear of TikTok's right-hand buttons
            cs -= 4
        dr.append(f"drawtext=fontfile={FB}:text='{esc(txt)}':fontsize={cs}:fontcolor={c}:borderw=8:bordercolor=black:"
                  f"x=(w-tw)/2:y=1420-th/2:enable='between(t,{max(0,a-s0):.2f},{b-s0:.2f})'")
    dr.append(video_mark())   # @ne0nleonida watermark (owner 2026-11-28)
    cap = ("," + ",".join(dr)) if dr else ""
    fc = (f"[0:v]trim={s0}:{s1},setpts=PTS-STARTPTS,fps=30,split[a][b];"
          f"[a]crop={fw}:{fh}:{fx}:{fy},scale={W}:{SEAM}:force_original_aspect_ratio=increase,crop={W}:{SEAM}[top];"
          f"[b]{gcf}scale={W}:{H-SEAM}:force_original_aspect_ratio=increase,crop={W}:{H-SEAM}[bot];"
          f"color=black:s={W}x{H}:r=30:d={dur:.3f}[bg];"
          f"[bg][top]overlay=0:0[v1];[v1][bot]overlay=0:{SEAM}[v2];"
          f"[v2][2:v]overlay=0:990[v3];[v3][3:v]overlay=0:1830{cap}[v4];[v4][1:v]overlay=0:0[v];"
          f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a]")
    out = f"{tmp}/seg{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", it["footage"], "-i", f"{tmp}/head.png", "-i", lp, "-i", cp,
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", str(C.get("crf", 16)), "-profile:v", "high", "-maxrate", "16M", "-bufsize", "32M",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)
    segs.append(out)

lst = f"{tmp}/list.txt"
open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
joined = f"{tmp}/joined.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                       joined]).decode())
# audio: original clip audio; optional music bed (owner 2026-11-20: bed felt distracting -> default off);
# optional "sting" (whoosh + boom) at every rank change
starts, acc = [], 0.0
for sp in segs:
    starts.append(acc)
    acc += float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", sp]).decode())
ins, fl, mix = ["-i", joined], [], ["[0:a]"]
k = 1
if C.get("music"):
    ins += ["-stream_loop", "-1", "-i", C["music"]]
    fl.append(f"[{k}:a]volume={C.get('music_vol', 0.16)},atrim=0:{total:.3f}[m]"); mix.append("[m]"); k += 1
if C.get("sting"):
    for j, st in enumerate(starts):
        ins += ["-i", C["sting"]]
        ms = int(max(0, st - 0.35) * 1000)
        fl.append(f"[{k}:a]volume={C.get('sting_vol', 0.7)},adelay={ms}|{ms}[s{j}]"); mix.append(f"[s{j}]"); k += 1
fl.append("".join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(fl),
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart", C["out"]], check=True)
print("ok", C["out"], f"{total:.2f}s")
