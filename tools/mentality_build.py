#!/usr/bin/env python3
"""'<Streamer> GTA 6 Mentality' edit (owner reference 2026-11-20, eliasn97clips style).

Structure: INTRO black card "<NAME> GTA 6 Mentality" + hit at 0.0 s (owner 2026-11-20) -> streamer setup beat (original audio only) -> black card "<NAME> GTA 6 Mentality" + boom ->
action beats with phonk bed under the original audio, a card between beats. Layout: facecam full-width
top (0-800), gameplay below (800-1920), punchy colour grade, one-word captions, credit + disclaimer.

Usage: python3 tools/mentality_build.py media/configs/<name>.json
Config: {"card": "Monte GTA 6 Mentality", "hook": ["LINE 1", "LINE 2"], "music": "media/music/x.mp3",
 "sting": "media/music/sting_whoosh_boom.wav", "credit": "Clip: @x on Twitch", "out": "media/edits/x.mp4",
 "card_dur": 0.7, "music_vol": 0.32,
 "beats": [{"footage": "...cut.mp4", "start": 0, "end": 6, "facecam": [x,y,w,h], "game_crop": [x,y,w,h],
            "words": [[w,s,e],...] (cut time), "red_words": [...], "card_before": false}, ...]}
"""
import json, os, subprocess, sys, tempfile

W, H, SEAM = 1080, 1920, 800
FB = "brand/fonts/TikTokSans-700.ttf"
GRADE = "eq=contrast=1.13:saturation=1.35:brightness=0.015,unsharp=5:5:0.7"


def esc(t):
    return t.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%")


def run(cmd):
    subprocess.run(cmd, check=True)


C = json.load(open(sys.argv[1]))
tmp = tempfile.mkdtemp()
cd = C.get("card_dur", 0.7)
parts, timeline, t = [], [], 0.0   # timeline: (kind, start, end)
disc = "Fan page. Not affiliated with Rockstar Games."
for i, b in enumerate(C["beats"]):
    # owner 2026-11-20 23:55: ALWAYS open with the black "<Name> GTA 6 Mentality" card + hit at 0.0 s, so a
    # swiping viewer instantly knows the format (otherwise it looks like a random clip). "intro_card": false disables.
    if b.get("card_before") or (i == 0 and C.get("intro_card", True)):
        cp = f"{tmp}/card{i}.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r=30:d={cd}",
             "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo", "-t", f"{cd}",
             "-vf", f"drawtext=fontfile={FB}:text='{esc(C['card'])}':fontsize=64:fontcolor=white:"
                    f"x=(w-tw)/2:y=(h-th)/2", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-shortest", cp])
        parts.append(cp); timeline.append(("card", t, t + cd)); t += cd
    s0, s1 = b["start"], b["end"]; dur = s1 - s0
    fx, fy, fw, fh = b["facecam"]; gc = b.get("game_crop")
    gcf = f"crop={gc[2]}:{gc[3]}:{gc[0]}:{gc[1]}," if gc else ""
    red = {w.upper() for w in b.get("red_words", [])}
    dr = []
    for w, a, e in b.get("words", []):
        if e < s0 or a > s1:
            continue
        txt = w.upper().strip(".,!?…\"")
        col = "0xFF2A2A" if txt in red else "0xFFE600"
        dr.append(f"drawtext=fontfile={FB}:text='{esc(txt)}':fontsize=92:fontcolor={col}:borderw=8:"
                  f"bordercolor=black:x=(w-tw)/2:y=1480-th/2:enable='between(t,{max(0, a - s0):.2f},{e - s0:.2f})'")
    if i == 0 and C.get("hook"):
        for k, line in enumerate(C["hook"]):
            y = SEAM - 66 + k * 78
            dr.append(f"drawtext=fontfile={FB}:text='{esc(line)}':fontsize=56:fontcolor=black:box=1:"
                      f"boxcolor=white:boxborderw=14:x=(w-tw)/2:y={y}")
    dr.append(f"drawtext=fontfile={FB}:text='{esc(C['credit'])}':fontsize=30:fontcolor=white:borderw=3:"
              f"bordercolor=black:x=(w-tw)/2:y=1640")
    dr.append(f"drawtext=fontfile={FB}:text='{esc(disc)}':fontsize=26:fontcolor=white:borderw=3:"
              f"bordercolor=black:x=(w-tw)/2:y=1682")
    fc = (f"[0:v]trim={s0}:{s1},setpts=PTS-STARTPTS,fps=30,split[a][b];"
          f"[a]crop={fw}:{fh}:{fx}:{fy},scale={W}:{SEAM}:force_original_aspect_ratio=increase,crop={W}:{SEAM}[top];"
          f"[b]{gcf}scale={W}:{H - SEAM}:force_original_aspect_ratio=increase,crop={W}:{H - SEAM}[bot];"
          f"[top][bot]vstack,{GRADE},format=yuv420p,{','.join(dr)}[v];"
          f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo[a]")
    sp = f"{tmp}/beat{i}.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", b["footage"], "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", "-ar", "48000", sp])
    parts.append(sp); timeline.append(("beat", t, t + dur)); t += dur

lst = f"{tmp}/list.txt"
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
cat = f"{tmp}/cat.mp4"
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18",
     "-preset", "fast", "-c:a", "aac", "-ar", "48000", cat])

# optional end card (louder end hit)
if C.get("end_card"):
    ep = f"{tmp}/cardend.mp4"; ed = C.get("end_card_dur", 1.0)
    run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=black:s={W}x{H}:r=30:d={ed}",
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ed}",
         "-vf", f"drawtext=fontfile={FB}:text='{esc(C['card'])}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=(h-th)/2",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", ep])
    open(f"{tmp}/list.txt", "a").write(f"file '{ep}'\n")
    timeline.append(("end", t, t + ed)); t += ed
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c:v", "libx264",
         "-crf", "18", "-preset", "fast", "-c:a", "aac", "-ar", "48000", cat])

cards = [(a, e) for k, a, e in timeline if k == "card"]
ends = [(a, e) for k, a, e in timeline if k == "end"]
if not C.get("music"):
    # reference style (owner 2026-11-20): NO music bed, same hit sound on every card, louder hit on end card
    inputs = ["-i", cat]; fa = ""; mix = ["[0:a]"]; j = 1
    for a, e in cards + ends:
        snd = C["end_sound"] if (a, e) in ends else C["card_sound"]
        inputs += ["-i", snd]; d = max(0, a - C.get("hit_lead", 0.1))
        fa += f"[{j}:a]adelay={int(d * 1000)}|{int(d * 1000)},volume={C.get('hit_vol', 1.0)}[h{j}];"
        mix.append(f"[h{j}]"); j += 1
    fa += f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.0[aout]"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fa, "-map", "0:v", "-map", "[aout]",
         "-c:v", "libx264", "-crf", str(C.get("crf", 22)), "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", C["out"]])
    print("ok", C["out"], f"{t:.2f}s"); sys.exit(0)
# music bed: starts at the first card, full volume on cards, ducked under beats
m0 = cards[0][0] if cards else 0.0
mv = C.get("music_vol", 0.32)
loud = "+".join(f"between(t,{a + m0 * 0:.2f},{e:.2f})" for a, e in cards) or "0"
inputs = ["-i", cat, "-i", C["music"]]
fa = (f"[1:a]adelay={int(m0 * 1000)}|{int(m0 * 1000)},atrim=0:{t:.3f},"
      f"volume='if({loud},1.0,{mv})':eval=frame,afade=t=out:st={t - 1.2:.2f}:d=1.2[m];")
mix = ["[0:a]", "[m]"]
if C.get("sting"):
    for j, (a, e) in enumerate(cards):
        inputs += ["-i", C["sting"]]
        fa += f"[{j + 2}:a]adelay={int(a * 1000)}|{int(a * 1000)},volume=0.9[s{j}];"
        mix.append(f"[s{j}]")
fa += f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,loudnorm=I=-14:TP=-1.5[aout]"
os.makedirs(os.path.dirname(C["out"]), exist_ok=True)
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fa, "-map", "0:v", "-map", "[aout]",
     "-c:v", "libx264", "-crf", str(C.get("crf", 22)), "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
     "-movflags", "+faststart", C["out"]])
print("ok", C["out"], f"{t:.2f}s")
