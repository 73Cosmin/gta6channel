---
name: guide-video
description: >-
  Build a 1deflay-style GTA 6 secret/how-to guide video (Short, 30-45 s) from a YouTube video section:
  "This is how you get X" hook with a sliding item picture card + swoosh over moving gameplay, step-by-step
  full-screen gameplay synced to an AI voiceover, GTA VI logo on top, 2-3-word Poppins captions (layout v2).
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
A source video usually has ~10 points (chapters) -> REUSE it: rank its chapters with
`python3 tools/guide_scout.py --chapters <video_id>` (YouTube click demand per topic; `(USED)` = done) and take the
highest-demand unused point. Record the EXACT chapter title in guides_used.csv. Topics: cars, weapons, money, easter eggs,
secret quests, stat boosts.
OWNER 2026-11-26: only items people WANT - beautiful/cool/fast (supercars, luxury, legendary weapons, big money); no plain bikes/beaters.
Pick ONE concrete, visual payoff (free car, hidden weapon, money spot, secret quest, stat boost) that the
footage shows step by step. After publishing add a row to `media/guides_used.csv`.

## LAYOUT v2 (OWNER-APPROVED 2026-11-26 ~17:45, refs @gta6_deutschland, media/references/tt_1126) - DEFAULT for every guide
Builder: `python3 tools/guide_build_v2.py media/configs/<file>.json` (example config: media/configs/2026-11-26_guide_emerus_v2.json).
- HOOK (first ~4 s): VO starts "This is how you get <X> ..." while a PICTURE CARD of the item (bright gameplay frame,
  `hook.img_t` + `hook.crop`, rounded white border, item name pill below) SLIDES IN from the side (`hook.from`
  right/left/top/bottom) with a swoosh (media/music/swoosh.wav, swoosh_vol 0.7 = owner-approved level), stays centred
  (hook_y ~840, not covering the logo), then slides out. Then "Here's how." and the walkthrough FROM THE START.
- Behind the card MOVING GAMEPLAY, never a still image (owner: keeps people watching).
- Gameplay ZOOMED to nearly full screen (band 1080x1500 at y 210); per cut `[vo_t, src_t, gamma, xfocus]` -
  xfocus 0..1 picks which part of the 16:9 frame stays visible (e.g. 0.95 for menus on the right).
- GTA VI logo top centre the whole video (brand/logo/gta6_logo.png, y 232 = below the TikTok search bar).
- Captions: 2-3 words, Poppins ExtraBold, white + one yellow key word (numbers/yellow_words/longest word), soft
  shadow, y ~1330. NO black/white title boxes (owner: unprofessional) - replaces checklist #7 for guides.
- Credit TINY in the bottom-left corner (builder default), NO "fan page / not affiliated" line (owner hard rule 2026-11-26). Music bed quiet (0.05) under the VO.

## ALGORITHM CHECK (owner 2026-11-26 ~21:30, Emerus Studio read + tiktok-algorithm skill) - EVERY guide
Emerus guide (dark night opening, payoff word at ~3 s) = 441 views @2.4 h, **24% avg watch, ~60% gone by 0:03**;
but 8 saves (36% of likes) and **47.5% of views from TikTok SEARCH**. Completion is the #1 ranking signal, the first
2 s decide it, and guides live off search + saves. So:
1. **Frame 0 = bright** (mean luma >= 90 on frames 0-3 s; measure:
   `ffmpeg -i out.mp4 -vf "fps=1,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -f null - 2>&1 | grep -o 'YAVG=[0-9]*'`).
   Night footage: cut gamma 1.4-1.8, or pick a daytime/studio shot for cut 0. No dark run-up (man at a gate, walking at night).
   Quick fix for a finished file: `eq=gamma=1.2,eq=gamma=1.15:enable='lt(t,6)'` -> new filename.
2. **Payoff word in the first 1.5 s of VO**: put the item first, e.g. "[excited] FREE hypercar in GTA 6! Here's how you get it."
   or keep "This is how you get a FREE <X>" short - never a long adjective chain before the item ("one of the fastest...").
3. **Hook card image bright** (`img_gamma` 1.3-1.6 for dim shots) - the item must read at thumbnail size.
4. **Length 25-35 s**; cut every 2-3 s, no step that isn't needed.
5. **End**: last VO line or caption = save prompt ("Save this before you forget 📌") + a question viewers can answer/correct.
6. **Caption = the exact search phrase** people type ("how to get the free hypercar in GTA 6", "gta 6 secret car location")
   + item name + save prompt + question + credit + **max 5 hashtags** (2 broad #gta6 #fyp + 2-3 niche #gta6cars #gta6secrets #gta6tips).
7. **Read at ~3 h** (owner Studio): <30% avg watch -> hook problem (fix 1-2); >40% watched but shares+saves <1% -> payoff problem;
   high Search share -> keep it up, guides grow for days via search, never delete early.

8. **NO JUMP CUTS (owner 2026-11-26: "komische Jumpcuts ganz random" in the Emerus guide - stop it).** A jump cut = the
   picture skips a bit inside the SAME shot (same place, slightly moved/repeated) and looks like a glitch. Rules:
   - Never start a new cut 0.1-2 s before/after where the previous one would continue: let the footage keep PLAYING and
     only cut when the picture changes to a different shot. One VO sentence does NOT need its own cut.
   - Never jump backwards inside a shot (repeats frames).
   - tools/guide_build_v2.py enforces this automatically (JUMP-CUT GUARD): skips < 2 s are merged into continuous
     playback, same-looking skips (frame diff 0.01-0.16) get a 0.3 s dissolve, real shot changes stay hard cuts.
     Read its "jumpcut guard:" lines - many merges = cuts planned too finely; pick fewer, bigger cuts.
     `"keep_cut": [i]` forces a cut, `"dissolve_below"` tunes the threshold.
   - Check: watch every cut boundary (frames 0.2 s before/after) - nothing may look like the video stuttered.

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

## 2. Script (EN, ~30-40 s, ~85-110 words) - HOOK STRUCTURE v2 (owner 2026-11-26)
- Sentence 1 = hook, starts EXACTLY like: "This is how you get <X> in GTA 6 for free!" (<X> = 1-3 words, payoff spoken by ~1.5 s - see ALGORITHM CHECK) (or "...start the hidden
  <quest>..."), optional tease ("green flames included", "most players walk right past it"). The picture card
  shows <X> during this sentence.
- Sentence 2 = "Here's how." -> then explain FROM THE START, one short sentence per visible step
  (map marker -> go there -> the action -> reward / where to register).
- End right after the payoff + a twist or flex ("You're welcome." / "[whispers] Because the next victim... is you.").
- ONLY facts visible in the footage or said by the creator (hard rule 2). Clickbait hook is OK (rule 3), but the
  VO says honestly what it costs ("Register it as yours for 9,500").
- Start with `[excited]`; `[whispers]` before a twist works.
- Check Scribe's word list for mishearings ("defenses" vs "the fences", "VI" -> builder shows "6") and fix
  `vo_words.json` before building - captions are built from it.

```bash
python3 .claude/skills/guide-video/scripts/guide.py vo <name> "[excited] This is how you get ..."
```
Prints VO sentences with start/end times (one ElevenLabs generation - never re-roll on scheduled runs).

## 3. Config `media/configs/<YYYY-MM-DD>_guide_<slug>_v2.json` (builder tools/guide_build_v2.py)
```json
{
 "footage": "media/raw/yt/<name>/section.mp4",
 "vo": "media/raw/yt/<name>/vo.mp3",
 "words": "media/raw/yt/<name>/vo_words.json",
 "cuts": [[0.0, 36.0, 1.15], [6.06, 4.0, 1.0, 0.5], [6.96, 8.0, 1.0, 0.8], [9.96, 18.0, 1.2]],
 "hook": {"img_t": 25.0, "crop": [470, 330, 1570, 949], "img_gamma": 1.0,
          "label": "BUCKINGHAM BOURBON WINDSOR", "in": 0.0, "out": 5.6, "from": "right"},
 "hook_y": 840, "caption_y": 1330,
 "yellow_words": ["LUXURY", "FREE", "WINDSOR"],
 "music": "media/music/synthwave_trap_01.mp3", "music_vol": 0.05,
 "credit": "Footage: @<creator> (YouTube)",
 "tail": 0.8,
 "out": "media/edits/<YYYY-MM-DD>_guide_<slug>_v2.mp4"
}
```
- `cuts` = `[vo_time, section_time, gamma?, xfocus?]`; each runs until the next cut. Cut only where the SHOT changes
  (ALGORITHM CHECK #8 - no jump cuts); a sentence can play over continuous footage. xfocus 0..1 = which horizontal part of the 16:9 frame
  stays in the zoomed crop (0.9-1.0 for menus on the right, ~0.1 for prices bottom-left).
- **Cut 0 = MOVING, BRIGHT gameplay** (driving, walking in daylight) - it runs behind the hook card. Never a
  still image/photo there, never a dark or black frame at 0.0 s: measure brightness of the first frames
  (`ffmpeg -ss T -i section.mp4 -frames:v 1 -vf scale=32:18,format=gray -f rawvideo -` -> mean > ~70) - scene
  transitions often flash black. Dark night shots: gamma 1.3-1.8.
- `hook.img_t` = the most beautiful BRIGHT frame of the item (studio shot, daylight photo, garage); `hook.crop` =
  `[x0,y0,x1,y1]` in source px (~16:9) so the item fills the card (grid-check the frame first). `label` = exact
  in-game name from the menu. `in` 0.0 (card flies in during the first 0.4 s), `out` = end of the hook sentence.
- A source segment must not run past the end of its scene (count: next cut vo_time - this vo_time).

## 4. Build + check
```bash
python3 tools/guide_build_v2.py media/configs/<file>.json
```
Measure luma of 0-3 s (ALGORITHM CHECK #1, >= 90) and check phone-crop frames (crop=883:1920:98:0) at 0.03 s, ~2 s (card in), the end of the hook, one frame per
sentence and the last frame -> Read them: first frame bright + moving gameplay, card centred and not covering the
logo or captions, captions readable, each cut matches its sentence, nothing black/cut off. Fix -> rebuild (~1 min).
When replacing an already scheduled file, publish it under a NEW filename (raw.githubusercontent caches ~5 min)
and swap the asset with Buffer edit_post (same post IDs).
Old builder tools/guide_build.py (blurred band + black/white title box) = legacy, don't use for new guides.

## 5. Publish
Commit config + mp4 to `main`, confirm the raw URL returns 200, then Buffer per playbook slots/caps
(TikTok max 4/day: 07:00/10:00/14:30/20:00, CONTENT PLAN v4, day-by-day rule; YT/IG only the 1-2 strongest guides/day). Caption (ALGORITHM CHECK #6): search phrase + save prompt + question + `🎥 Footage: @creator` +
max 5 hashtags (NO "fan page / not affiliated" line). Story/side-quest twist → caption starts
with "SPOILER". Log in `log.md` + `scoreboard.csv`.
