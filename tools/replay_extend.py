#!/usr/bin/env python3
"""Append a slow-motion replay of the payoff to a creator clip (owner 2026-11-19: TikTok flagged a
12 s re-cut as 'unoriginal, low-quality'; no AI voice wanted -> transform with replay + label + length).

Usage: python3 tools/replay_extend.py <config_in.json> <config_out.json> <start> <end> [speed=0.5]
Writes <footage>_rp.mp4 and <vo>_rp.mp3, copies the replayed words (stretched) and adds a
"NOCHMAL IN ZEITLUPE" / "SLOW-MO REPLAY" label. Then build: info_build.py <config_out.json>.
"""
import json, subprocess, sys

cin, cout, a, b = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
sp = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
C = json.load(open(cin))
foot, vo = C["footage"], C["vo"]
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", vo]).decode())
nf, na = foot.replace(".mp4", "_rp.mp4"), vo.replace(".mp3", "_rp.mp3")
k = 1 / sp
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", foot, "-filter_complex",
    f"[0:v]trim=0:{dur:.3f},setpts=PTS-STARTPTS,fps=30[v0];"
    f"[0:v]trim={a}:{b},setpts=(PTS-STARTPTS)*{k},fps=30[v1];"
    f"[0:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS[a0];"
    f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={sp}[a1];"
    "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]",
    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-c:a", "aac", nf],
    check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", nf, "-vn", "-c:a", "libmp3lame", "-b:a", "192k", na],
               check=True)
rep = [[w[0], round(dur + (w[1] - a) * k, 2), round(dur + (w[2] - a) * k, 2)]
       for w in C["words"] if w[1] >= a and w[2] <= b]
C["footage"], C["vo"] = nf, na
C["words"] = C["words"] + rep
de = any(x in (C.get("credit", "") + " ".join(C.get("title", []))) for x in
         ("montanablack", "papaplatte", "giggand", "Ä", "Ü", "Ö"))
lbl = "NOCHMAL IN ZEITLUPE" if de else "SLOW-MO REPLAY"
total = dur + (b - a) * k
C["pop_texts"] = C.get("pop_texts", []) + [[lbl, round(dur, 2), round(total, 2), 1160]]
if C.get("end_text"):
    C["end_text"] = [C["end_text"][0], round(max(dur, total - 4.0), 2)]
C["out"] = C["out"].replace(".mp4", "_rp.mp4").replace("_v2_rp", "_rp")
json.dump(C, open(cout, "w"), ensure_ascii=False)
print("ok", cout, f"{total:.2f}s")
