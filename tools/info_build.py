#!/usr/bin/env python3
"""ne0nleonida standard video builder (owner's style — use for EVERY video).

  python3 tools/info_build.py config.json

Layout (always): full 9:16 screen filled with a zoomed, blurred, colourful copy of the footage
(no black bars, no solid bands) + sharp 16:9 footage band in the middle + one-word yellow captions
synced to the voice (ElevenLabs Scribe word timings) + credit/disclaimer. Optional: title lines,
checklist steps with red arrow pop-ins, end text, background music (ducked under the voice).

config.json:
{
  "footage": "media/official/trailer2_landscape_clean.mp4",   # landscape source
  "precrop": "null",                # ffmpeg crop for the source, "null" if already clean
  "shots": [7.5, 15, 30],           # start seconds of each cut (equal lengths over the VO)
  "vo": "media/raw/vo.mp3",
  "words": [["Want",0.14,0.28], ...],   # from Scribe; numbers spelled as digits
  "red_words": ["ONE","TWO"],       # words shown in red instead of yellow
  "title": ["GTA 6", "PLAY THE SECOND IT UNLOCKS"],
  "steps": [["1. PRELOAD NOW","PS5 or Xbox",4.16], ...],   # optional
  "end_text": ["FOLLOW FOR MORE GTA 6 TIPS", 16.28],         # optional
  "music": "media/music/synthwave_trap_01.mp3",              # optional
  "caption_y": 1380,                # caption centre; default BELOW the band (owner: never over the face)
  "credit": "Footage: Rockstar Games (Trailer 2)",
  "out": "media/edits/x.mp4"
}
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw

C = json.load(open(sys.argv[1]))
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PINK, CYAN, YEL, RED = "0xFF2BD6", "0x22E6FF", "0xFFE600", "0xFF2A2A"
vo = C["vo"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vo]).decode()) + C.get("tail", 0.4)

def esc(t):
    return (t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
             .replace(",", "\\,").replace("%", "\\%"))

arrow = "/tmp/ne0n_arrow.png"
im = Image.new("RGBA", (260, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.polygon([(20, 60), (150, 60), (150, 20), (240, 130), (150, 240), (150, 200), (20, 200)],
          fill=(235, 20, 30, 255), outline=(255, 255, 255, 255), width=10)
im.rotate(165, resample=Image.BICUBIC, expand=True).save(arrow)

shots = C["shots"]; n = len(shots); seg = dur / n
f = [f"[0:v]trim=start={s}:duration={seg:.3f},setpts=PTS-STARTPTS[s{i}]" for i, s in enumerate(shots)]
f.append("".join(f"[s{i}]" for i in range(n)) +
         f"concat=n={n}:v=1:a=0,fps=30,{C.get('precrop','null')},split[a][b]")
# full-screen fill: zoom in hard so there is never black, blur, keep colour
SPLIT = "facecam" in C          # owner 2026-11-19: stacked layout = facecam on top, gameplay below
SY = C.get("split_y", 700)      # seam between facecam (top) and gameplay (bottom)
if SPLIT:
    fx, fy, fw, fh = C["facecam"]                       # facecam rect in source pixels
    f.append(f"[a]crop={fw}:{fh}:{fx}:{fy},scale=1080:{SY}:force_original_aspect_ratio=increase,"
             f"crop=1080:{SY}[top]")
    gc = C.get("game_crop")                             # optional [x,y,w,h]; default whole frame
    gcf = f"crop={gc[2]}:{gc[3]}:{gc[0]}:{gc[1]}," if gc else ""
    f.append(f"[b]{gcf}scale=1080:{1920-SY}:force_original_aspect_ratio=increase,crop=1080:{1920-SY}[bot]")
    f.append("[top][bot]vstack=inputs=2[v0]")
else:
    f.append("[a]scale=-2:2400,crop=1080:1920,boxblur=22:2,eq=brightness=-0.06:saturation=1.35[bg]")
    f.append("[b]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608[fg]")
    f.append("[bg][fg]overlay=0:656[v0]")

dr = []
t1, t2 = (C.get("title") or [None, None]) + [None] * (2 - len(C.get("title") or []))
# Title block (owner 2026-11-19): sits LOWER (TikTok search bar covers y<~280) and auto-shrinks so
# each line fits inside ~880 px with side margins, never touching the screen edges.
from PIL import ImageFont
def fit(txt, size, border, maxw=880):
    while size > 30 and ImageFont.truetype(F, size).getlength(txt) + 2 * border > maxw:
        size -= 2
    return size
TY = C.get("title_y", 330)
s1 = fit(t1, C.get("title1_size", 84), 8) if t1 else 0
TT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "brand", "fonts", "TikTokSans-700.ttf")
title_png = None
if SPLIT and t1:
    # TikTok-style title (owner ref IMG_0817): black bold TikTok Sans on white rounded boxes, one box per
    # line, centred ON the seam between facecam and gameplay, visible the whole video.
    lines = [l for l in (t1, t2) if l]
    size = C.get("title_size", 84)
    while size > 40 and max(ImageFont.truetype(TT, size).getlength(l) for l in lines) + 56 > 1010:
        size -= 2
    ft = ImageFont.truetype(TT, size); padx, lh = 28, int(size * 1.22)
    ws = [ft.getlength(l) for l in lines]; Wb = int(max(ws) + 2 * padx + 8); Hb = lh * len(lines) + 16
    im = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (l, wl) in enumerate(zip(lines, ws)):
        x0 = (Wb - wl) / 2 - padx; y0 = 8 + k * lh
        d.rounded_rectangle([x0, y0, x0 + wl + 2 * padx, y0 + lh], radius=int(size * 0.22), fill=(255, 255, 255, 255))
    for k, (l, wl) in enumerate(zip(lines, ws)):
        d.text(((Wb - wl) / 2, 8 + k * lh + lh / 2), l, font=ft, fill=(0, 0, 0, 255), anchor="lm")
    title_png = "/tmp/ne0n_title.png"; im.save(title_png)
    title_xy = ((1080 - Wb) // 2, SY - Hb // 2)
elif t1:
    dr.append(f"drawtext=fontfile={F}:text='{esc(t1)}':fontsize={s1}:fontcolor=white:borderw=8:bordercolor={PINK}:"
              f"shadowcolor=black@0.6:shadowx=4:shadowy=4:x=(w-tw)/2:y={TY}")
if t2 and not SPLIT:
    s2 = fit(t2, C.get("title2_size", 52), 6)
    dr.append(f"drawtext=fontfile={F}:text='{esc(t2)}':fontsize={s2}:fontcolor={CYAN}:borderw=6:bordercolor=black:"
              f"x=(w-tw)/2:y={TY + s1 + 34}")
W = C["words"]; red = set(C.get("red_words", []))
for i, (w, st, en) in enumerate(W):
    nxt = W[i + 1][1] if i + 1 < len(W) else dur
    end = min(nxt, en + 0.6)
    c = w.strip(".,!?").upper()
    col = RED if c in red else YEL
    dr.append(f"drawtext=fontfile={TT if SPLIT else F}:text='{esc(c)}':fontsize=100:fontcolor={col}:borderw=9:bordercolor=black:"
              f"x=(w-tw)/2:y={C.get('caption_y', 1330 if SPLIT else 1380)}-th/2:enable='gte(t,{st})*lt(t,{end:.3f})'")
steps = C.get("steps", [])
for k, (a, b, t0) in enumerate(steps):
    y = 1310 + k * 150
    dr.append(f"drawtext=fontfile={F}:text='{esc(a)}':fontsize=60:fontcolor=white:x=90:y={y}:box=1:"
              f"boxcolor=0x0A0014@0.8:boxborderw=14:enable='gte(t,{t0})'")
    dr.append(f"drawtext=fontfile={F}:text='{esc(b)}':fontsize=40:fontcolor={CYAN}:borderw=3:bordercolor=black:"
              f"x=104:y={y+82}:enable='gte(t,{t0})'")
for txt, t0, *rest in C.get("pop_texts", []):   # [text, start, end, y]
    t_end, y = (rest + [dur, 1360])[:2]
    dr.append(f"drawtext=fontfile={F}:text='{esc(txt)}':fontsize=64:fontcolor=white:borderw=7:bordercolor={PINK}:"
              f"x=(w-tw)/2:y={y}:enable='between(t,{t0},{t_end})'")
if C.get("end_text"):
    txt, t0 = C["end_text"]
    dr.append(f"drawtext=fontfile={F}:text='{esc(txt)}':fontsize=58:fontcolor=white:borderw=6:bordercolor={PINK}:"
              f"x=(w-tw)/2:y={C.get('end_text_y',960)}:enable='gte(t,{t0})'")
for k, line in enumerate([C.get("credit", ""), "Fan page. Not affiliated with Rockstar Games."]):
    if line:
        dr.append(f"drawtext=fontfile={F}:text='{esc(line)}':fontsize=28:fontcolor=white:borderw=3:bordercolor=black:"
                  f"x=(w-tw)/2:y={C.get('credit_y',1480) + k*42}")
f.append("[v0]" + ",".join(dr) + "[v1]")
cur = "v1"
if steps:
    f.append(f"[1:v]format=rgba,scale=200:-1,split={len(steps)}" + "".join(f"[ar{k}]" for k in range(len(steps))))
    for k, (_, _, t0) in enumerate(steps):
        y = 1310 + k * 150 - 40; nx = f"v{k+2}"
        f.append(f"[{cur}][ar{k}]overlay=x='if(lt(t,{t0}+0.25),1080-220*(t-{t0})/0.25,860)':y={y}:"
                 f"enable='between(t,{t0},{t0}+2.8)'[{nx}]")
        cur = nx

inputs = ["-i", C["footage"], "-loop", "1", "-i", arrow, "-i", vo]
if C.get("music"):
    inputs += ["-stream_loop", "-1", "-i", C["music"]]
if title_png:
    ti = 4 if C.get("music") else 3
    inputs += ["-loop", "1", "-i", title_png]
    f.append(f"[{cur}][{ti}:v]overlay={title_xy[0]}:{title_xy[1]}:shortest=0[vt]"); cur = "vt"
f.append(f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur:.2f},asplit[vo1][vo2]")
if C.get("music"):
    f.append(f"[3:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.09,"
             f"afade=t=out:st={dur-0.8:.2f}:d=0.8[mu]")
    f.append("[mu][vo1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=300[duck]")
    f.append("[vo2][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[aout]")
else:
    f.append("[vo1]anullsink;[vo2]loudnorm=I=-14:TP=-1.5:LRA=7[aout]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", f"[{cur}]",
       "-map", "[aout]", "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
       "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", C["out"]]
subprocess.run(cmd, check=True)
print("ok", C["out"], f"{dur:.2f}s")
