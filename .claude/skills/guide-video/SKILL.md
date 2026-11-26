---
name: guide-video
description: >-
  Build a 1deflay-style GTA 6 secret/how-to guide video (Short, 30-45 s) from a YouTube video section:
  "HOW TO GET X" hook, step-by-step gameplay synced to an AI voiceover, title box, one-word captions.
  Use when the owner sends a YouTube link + timestamp/number and says "mach ein Video wie deflay",
  "guide video", "how to get", "secret location", "free car", or similar.
---

# guide-video

Proven format (owner 2026-11-26, refs @1deflay; first two: serial killer quest, free Rolls Royce).
Every sentence of the voiceover gets its own gameplay cut that SHOWS exactly that step.

## 0. Find a source (daily automatic run, or when no link was given)
```bash
python3 tools/guide_scout.py --hours 72 --top 12
```
Ranks fresh GTA 6 guide videos by views/hour and prints their chapters. Skip anything in
`media/guides_used.csv` (same video+chapter or same TOPIC), glitches/exploits (rule 4) and topics we already posted.
Pick ONE concrete, visual payoff (free car, hidden weapon, money spot, secret quest, stat boost) that the
footage shows step by step. After publishing add a row to `media/guides_used.csv`.

## 1. Prep (one command)
```bash
python3 .claude/skills/guide-video/scripts/guide.py prep <name> "<youtube-url>" <start> <end>
```
`<name>` short slug (e.g. `rr`). Start/end as `4:52` or seconds; use the video's chapters
(`media/raw/yt/<name>/src.info.json` → `chapters`) when the owner says "number 7".
Prints the creator's transcript (section seconds) and writes a contact sheet `/tmp/guide_<name>/sheet.jpg`
(timestamps in yellow) - Read it. Zoom in with `sheet <name> <from> <to> [step]` and read menu/map text
with `frame <name> <t>` (exact item names, prices, mission names - never guess).
YouTube auto-subs are rate-limited (429); Scribe is the transcript.

## 2. Script (EN, ~30-40 s, ~90-110 words)
- Line 1 = payoff/proof + hook: "This is how you get this <X> in GTA 6 for FREE." / "This hidden quest in GTA 6 makes YOU the next victim."
- Line 2 = promise: "Here's how ... in literally two minutes." or a qualifier ("And yes, it works even in chapter two.")
- Then one short sentence per visible step (map marker → go there → the action → reward/where to register).
- End right after the payoff + a twist or flex ("green flames out the back. You're welcome.").
- ONLY facts visible in the footage or said by the creator (hard rule 2). Clickbait in the title is OK
  (rule 3), but say honestly in the VO what it costs (e.g. "register it for 9,500").
- Start with `[excited]`; a `[whispers]` before a twist works.

```bash
python3 .claude/skills/guide-video/scripts/guide.py vo <name> "[excited] This is how you ..."
```
Prints VO sentences with start/end times.

## 3. Config `media/configs/<YYYY-MM-DD>_guide_<slug>.json`
```json
{
 "footage": "media/raw/yt/<name>/section.mp4",
 "vo": "media/raw/yt/<name>/vo.mp3",
 "words": "media/raw/yt/<name>/vo_words.json",
 "title": ["FREE ROLLS ROYCE", "IN GTA 6"],
 "title_until": null,
 "gamma": 1.1,
 "cuts": [[0.0, 25.2], [4.1, 108.0, 1.25], [7.0, 6.0]],
 "red_words": ["FREE", "FAST"],
 "music": "media/music/synthwave_trap_01.mp3", "music_vol": 0.05,
 "credit": "Footage: @<creator> (YouTube)",
 "tail": 0.8,
 "out": "media/edits/<YYYY-MM-DD>_guide_<slug>.mp4"
}
```
- `cuts` = `[vo_time, section_time, optional_gamma]`; each runs until the next cut. Put a cut at the start
  of every VO sentence (split long sentences at the key word, e.g. "there she is").
- **Cut 0 must show the payoff in a BRIGHT frame from frame 1** (owner: dark start = swipe). Check the sheet:
  a cut that starts 1 s early can still show the previous scene. Dark/night shots: gamma 1.3-1.7.
- **Title box ALWAYS** (CLAUDE.md checklist #7): 2 short caps lines, what you get. `title_until: null` = whole
  video (captions then sit below the gameplay automatically).

## 4. Build + check
```bash
python3 tools/guide_build.py media/configs/<file>.json
python3 .claude/skills/guide-video/scripts/guide.py check <name> <config-name-without-.json>
```
Read `/tmp/guide_<name>/check.png` (phone crop): first frame bright + shows the payoff, title box readable,
each cut matches its sentence, nothing cut off. Fix cuts → rebuild (≈1 min).

## 5. Publish
Commit config + mp4 to `main`, confirm the raw URL returns 200, then Buffer per playbook slots/caps
(TikTok 07:00/12:00/17:00, day-by-day rule). Caption: hook + question + `🎥 Footage: @creator` +
"Fan page, not affiliated with Rockstar Games." + 5 hashtags. Story/side-quest twist → caption starts
with "SPOILER". Log in `log.md` + `scoreboard.csv`.
