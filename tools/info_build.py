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
f.append("[a]scale=-2:2400,crop=1080:1920,boxblur=22:2,eq=brightness=-0.06:saturation=1.35[bg]")
f.append("[b]scale=1080:608:force_original_aspect_ratio=increase,crop=1080:608[fg]")
f.append("[bg][fg]overlay=0:656[v0]")

dr = []
t1, t2 = (C.get("title") or [None, None]) + [None] * (2 - len(C.get("title") or []))
if t1:
    dr.append(f"drawtext=fontfile={F}:text='{esc(t1)}':fontsize=120:fontcolor=white:borderw=8:bordercolor={PINK}:"
              f"shadowcolor=black@0.6:shadowx=4:shadowy=4:x=(w-tw)/2:y=170")
if t2:
    dr.append(f"drawtext=fontfile={F}:text='{esc(t2)}':fontsize={C.get('title2_size',58)}:fontcolor={CYAN}:borderw=6:bordercolor=black:"
              f"x=(w-tw)/2:y=320")
W = C["words"]; red = set(C.get("red_words", []))
for i, (w, st, en) in enumerate(W):
    nxt = W[i + 1][1] if i + 1 < len(W) else dur
    end = min(nxt, en + 0.6)
    c = w.strip(".,!?").upper()
    col = RED if c in red else YEL
    dr.append(f"drawtext=fontfile={F}:text='{esc(c)}':fontsize=100:fontcolor={col}:borderw=9:bordercolor=black:"
              f"x=(w-tw)/2:y=960-th/2:enable='gte(t,{st})*lt(t,{end:.3f})'")
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
              f"x=(w-tw)/2:y=1180:enable='gte(t,{t0})'")
for k, line in enumerate([C.get("credit", ""), "Fan page. Not affiliated with Rockstar Games."]):
    if line:
        dr.append(f"drawtext=fontfile={F}:text='{esc(line)}':fontsize=28:fontcolor=white:borderw=3:bordercolor=black:"
                  f"x=(w-tw)/2:y=h-{130 - k*42}")
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
f.append(f"[2:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur:.2f},asplit[vo1][vo2]")
if C.get("music"):
    inputs += ["-stream_loop", "-1", "-i", C["music"]]
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
