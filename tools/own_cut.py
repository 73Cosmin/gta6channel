#!/usr/bin/env python3
"""Generic own-gameplay cutter (generalised from own_cut_fake_robbery.py).
Usage: python3 tools/own_cut.py <plan.json>
plan = {"src": "...mp4", "words": "...json ([[text,start,end],...] from eleven.py scribe),
        "segments": [[start, end, speed, "optional extra -vf"], ...],
        "sting_at_seg": index (sting_whoosh_boom.wav at the START of that segment) or null,
        "vf_all": "eq=..." (applied to every segment), "cut": "media/raw/clips/<name>_cut.mp4",
        "audio": "media/raw/clips/<name>_audio.mp3", "config": "media/configs/<name>.json",
        "end_text": "QUESTION?" (shown the last end_secs seconds), "end_secs": 4.5}
Writes the cut + audio, and puts the remapped word timings + end_text into the info_build config."""
import json, subprocess, sys, tempfile, os
P = json.load(open(sys.argv[1]))
tmp = tempfile.mkdtemp()
lst = open(f"{tmp}/list.txt", "w")
for i, (a, b, sp, *ex) in enumerate(P["segments"]):
    vf = ",".join(x for x in [f"setpts=PTS/{sp}" if sp != 1 else "", "fps=30", P.get("vf_all", ""), ex[0] if ex else ""] if x)
    af = (f"atempo={sp}," if sp != 1 else "") + "aresample=48000"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(round(b - a, 3)), "-i", P["src"], "-vf", vf, "-af", af,
                    "-ac", "2", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-c:a", "aac", "-b:a", "192k", f"{tmp}/s{i}.mp4"], check=True)
    lst.write(f"file '{tmp}/s{i}.mp4'\n")
lst.close()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c", "copy", f"{tmp}/cat.mp4"], check=True)
si = P.get("sting_at_seg")
if si is not None:
    t = sum((b - a) / sp for a, b, sp, *_ in P["segments"][:si])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmp}/cat.mp4", "-i", "media/music/sting_whoosh_boom.wav", "-filter_complex",
                    f"[1:a]aresample=48000,adelay={int(t*1000)}|{int(t*1000)},volume=0.8[st];[0:a][st]amix=inputs=2:duration=first:normalize=0[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", P["cut"]], check=True)
else:
    os.replace(f"{tmp}/cat.mp4", P["cut"])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", P["cut"], "-vn", "-c:a", "libmp3lame", "-b:a", "192k", P["audio"]], check=True)
w = json.load(open(P["words"]))
out, off = [], 0
for a, b, sp, *_ in P["segments"]:
    for t_, x, y in w:
        if t_.startswith("["):
            continue
        if x >= a - 0.02 and y <= b + 0.05:
            out.append([t_, round(off + max(0, x - a) / sp, 2), round(off + (min(y, b) - a) / sp, 2)])
    off += (b - a) / sp
print("dur", round(off, 2)); print(" ".join(x[0] for x in out))
C = json.load(open(P["config"]))
C["words"] = out
if P.get("end_text"):
    C["end_text"] = [P["end_text"], round(off - P.get("end_secs", 4.5), 2)]
json.dump(C, open(P["config"], "w"), ensure_ascii=False)
