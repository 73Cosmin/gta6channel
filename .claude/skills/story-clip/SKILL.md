---
name: story-clip
description: >-
  Turn the owner's own 16:9 GTA 6 gameplay capture into a full-screen 9:16 "story clip" like @toastergta's SWAT-stash
  video (2.0M views on X): the in-game dialogue tells the story with one-word subtitles, punch-in zooms with cinematic
  bars, a red arrow, an understated hook line, original game audio, payoff at the end. Use when the owner sends own
  clips/captures and says "bau sowas nach", "story clip", "wie toaster", or sends a long own gameplay scene with NPC dialogue.
---

# story-clip

> **STATUS 2026-11-27 ~22:40: first build REJECTED by the owner** ("gefällt mir gar nicht ... komischer Pfeil ... allgemein
> schlecht gemacht, verwirf es"). Built from the night 1080p SWAT capture (media/configs/2026-11-27_story_swat.json).
> No red arrow any more (owner disliked it). Don't build another story clip unless the owner asks again; then ask first
> what should look different and show a short preview (10-15 s) before a full render.

## Why this format (analysis 2026-11-27)
Reference: x.com/toastergta/status/2126279048179707967 - "All that SWAT backup just for it to end like this 💀",
115 s, **2.02M views / 25.3K likes / 7.8K bookmarks / 744 reposts** in <10 h (account: 20K followers).
It is almost the SAME scene as our own `2026-11-26_own_swat_yoink_short` (29 s) = **1.1K views**. What they did differently:

| Theirs (2M) | Ours (1.1K) |
|---|---|
| FULL-SCREEN 9:16 crop of the 16:9 capture, camera close behind the car, 4K60 | small 16:9 band in the middle + blurred bars = looks like a repost |
| DAYLIGHT, bright | night, dark |
| The whole raid is the story: police radio subtitled word by word ("Perimeter secure... SWAT's in position... Suspect's gone... We didn't find any cash... If the suspect comes back, I want this asshole in cuffs or a body bag") -> THEN he walks up and takes the bag out of their car | cut to 29 s, the setup (raid, "no cash found", the threat) was missing - payoff without tension |
| Hook = understated curiosity joke "It's free money at this point 😭" (doesn't spoil the payoff) | hook spoiled it: "BRO YOINKED FROM SWAT 💀" |
| Original game audio only (sirens, radio) - immersive | music bed |
| Red arrow at 12 s ("watch THIS balcony"), punch-in zooms with black cinematic bars on the SWAT team | static band |
| Caption = ironic tease of the ending ("...just for it to end like this 💀") | |
Length is NOT the problem: 115 s worked because every few seconds a new dialogue line raises the stakes.

## What the owner must send
- Own capture, 16:9, ideally 4K/1440p 60 fps (1080p works), **daylight**, camera close/low behind the character or car,
  one continuous scene with NPC/police dialogue (raid, arrest, chase, robbery, someone talking right before the stupid/genius move).
- The whole scene incl. the build-up (don't pre-cut it) + 5-10 s after the payoff.
- Upload: files into the chat -> they land in /root/.claude/uploads/...; copy to `media/raw/clips/` (gitignored, never commit raw).

## Workflow
1. **Read the scene**: contact sheet every 2 s + Scribe transcript of the raw capture:
   ```bash
   ffmpeg -i in.mp4 -vf "fps=1/2,scale=300:-1,tile=8x8" sheet.jpg
   ffmpeg -i in.mp4 -vn -ac 1 -b:a 96k a.mp3 && python3 tools/eleven.py scribe a.mp3 words.json
   ```
2. **Story plan** (write it down before cutting): SETUP (what's going on, 3-8 s) -> TENSION (the dialogue lines that raise
   the stakes; keep them ALL, cut only dead air/walking with no talk) -> PAYOFF (the move) -> end 1-3 s after the payoff
   (no outro, ends hard so it loops). Target 30-120 s; longer only if a new line/beat comes every ~3-5 s.
3. **Segments** (`tools/story_build.py` config): one segment per continuous part, `x` = horizontal centre of the
   9:16 crop (keep the subject in it - check frames!), close-ups = `"zoom": 1.5-2.0, "bars": true` (+ `"y"`),
   slow pan with `x_end`. Dark capture -> `"gamma": 1.2-1.4`. No jump cuts inside one take (cut only where time really skips).
4. **Hook** (`hook.lines`, 2 short lines, sentence case, 1 emoji, 4-6 s): understated joke / curiosity that does NOT
   spoil the payoff ("It's free money at this point 😭", "They really thought this was over 💀"). Dark translucent box (builder default).
5. **No arrows** (owner 2026-11-27: 'komischer Pfeil'). The `arrows` option stays in the builder but is not used.
6. **Words**: `"words": "auto"` (Scribe on the cut audio); drop non-dialogue tags (builder skips `[...]`).
   Check the words json for mishearings and fix before the final build.
7. **Build + check**: `python3 tools/story_build.py media/configs/<date>_story_<slug>.json`; look at frames at 0.5 s,
   the arrow, each zoom, the payoff, the last frame (subject inside the crop, nothing cut off in the phone safe zone, bright start).
8. **Caption**: ironic tease of the ending + question, e.g. "All that SWAT backup just for it to end like this 💀
   Would you have risked it? 👇" + max 5 hashtags. Own capture -> no credit line needed.
9. **Publish**: TikTok automatic (it is a video, our sound = game audio) in the next slot (CONTENT PLAN v4),
   YouTube Shorts at the same time (own-made = YT rule; Shorts allow up to 3 min), IG Reel if it is the day's strongest.
   X: the reference went viral ON X - suggest posting this format on X too (ask the owner first; X stories are off).
   Log in log.md + scoreboard.csv (format 'Story clip', test_name story_clip).

## Exceptions to the CLAUDE.md VIDEO CHECKLIST (owner asked for this exact style)
- No black-on-white title box (#7): the hook is the dark translucent TikTok-classic box from the reference.
- No music bed (#4): original game audio only - the dialogue IS the content.
- Word captions are white one-word subtitles of the game dialogue (not yellow/red).
- Faint `ne0nleonida` watermark (anti-repost + recognition, like the reference's `toaster.gta`); `"watermark": ""` turns it off.
- Still applies: bright start, phone safe zone, no 'fan page / not affiliated' line, look at 3+ frames.

Tool: tools/story_build.py (docstring = full config reference). Test render: built on a 16:9 YouTube section, 17.5 s, ~45 s build.
