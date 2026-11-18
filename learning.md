# Learning

## Current Rules
- (starting hypotheses — test, don't treat as law) Official trailer clips beat text-only number posts;
  countdowns are the cheapest reliable format; credited creator clips and HOW TO posts pull saves/shares;
  emotional era-ending one-liners pull high like ratios.

- OWNER STYLE BRIEF (2026-11-18, from 6 reference TikToks; these override the hypotheses above):
  1. Never a static/plain background. Always moving GTA 6 footage behind the text (official trailer
     footage credited "Footage: Rockstar Games", or credited creator gameplay after launch).
  2. Info videos = catchy topic hook + moving background + editing graphics: arrows, circles,
     highlight boxes, pop-in/slide animations on text and images, fast cuts. Owner's favourite format.
  3. Slideshows work: image + bold text per slide with useful info (e.g. "5 things to do first").
  4. Vibe edits: little or no speech, footage + music + mood. Voiceover optional for these.
  5. MEMES are top priority: relatable, shareable GTA 6 memes (format jokes, reactions, "me when...").
     Aim for many. Rules still apply: no fake news/quotes, no leaks, no AI art passed off as gameplay,
     no story spoilers, nothing that implies we are Rockstar.
  - Reference files are in media/references/ (studied 2026-11-18). Concrete recipe:
    * INFO (info_word_captions_arrows.mp4, owner's favourite): 9:16 frame = blurred zoomed copy of the
      footage as full background + sharp 16:9 footage band in the middle; GTA VI logo at top; ONE word
      at a time captions, bold yellow, centre of band, a key word in red; red arrow pointing at the
      subject; a new shot every 2-3s; ~25s. Hook topic is a relatable "did you know" angle.
    * MEME (meme_lucia_apologize.mp4, meme_wake_up_bro.png): one relatable line in white TikTok-style
      text with emoji over a short scene, 10-35s, no voiceover, trending sound. "Wake up bro..." style
      text-over-clip memes.
    * VIBE (vibe_trailer_montage.mp4): 25s fast montage of the best trailer shots (aerial city, airboat,
      boat, parachute, chase), music only, no text.
    * SLIDES (img_*): bold infographic carousels: big headline, GTA VI logo, labels/icons, comparisons
      (GTA V vs GTA VI). Post as image carousel / photo-mode TikTok.
  - CAUTION about the references: copy the STYLE, not the content. Several are AI-made images/clips
    with unverified claims ("170+ animals", "50+ brands confirmed", travel times, scenes not in any
    trailer) and one implies relationship mechanics. Our versions use only official footage and only
    facts in facts.md; anything AI-made is branding/meme art, never shown as real gameplay.
- OpusClip trial exports carry an "OpusClip" watermark top-left (~x120-480, y250-335 on 1080x1920):
  always cover it (solid header band) or crop it out. Download host signed-ext.cdn.opus.pro is allowed.

- ⛔ MEMES DROPPED (owner, 2026-11-18, after seeing 3 AI-skit memes): never make memes again. Only
  streamer/creator clips, news, HOW TO/info videos. The brief below is kept for reference only.
- (archived) OWNER HUMOR BRIEF (2026-11-18, 6 more refs in media/references/: export_*.mov, v1*/v2*.mp4; 2 German).
  Owner verdict on our first memes (meme_nz_wait): "very bad". Why: it was an INFOGRAPHIC with a joke title
  (timetable, yellow word captions, trailer footage, no person, nothing funny happening). Real memes are:
  * ONE short relatable line in a WHITE TikTok pill (black bold text, rounded white box per line), top third,
    1 emoji max. Formats that work: "Me trying to sleep on November 18th 😭", "POV: the first day of GTA 6
    release", "POV: you're booting up GTA 6 on Nov 19", "Everyone on Nov 19 at 00:01 🤣", "Me and the boys".
    NO yellow one-word captions, NO voiceover, NO lists, NO numbers, NO explaining the joke.
  * A HUMAN REACTING is the joke (the face sells it): guy giggling/kicking in bed, screaming streamer with a
    crown over GTA key art, soldiers cheering "me and the boys", guy boots GTA 6 and instantly gets "WASTED"
    and faceplants, a whole apartment building where every window is a guy on a couch with a controller.
  * Exaggeration + shared moment (sleepless night, release midnight, calling in sick, girlfriend/mom/boss,
    GTA 5 Online grinders, the wait). Self-own > dunking on people.
  * Short: 7-23 s, one beat (or setup -> punchline at ~60%). Music/trending sound only.
  * Visual: full-screen 9:16 scene. Allowed: AI-generated PEOPLE and ROOMS (clearly a skit, labelled
    "AI-generated scene"), official Rockstar key art/trailer as backdrop (credited). NEVER AI fake gameplay,
    never AI images of GTA 6 screens shown as real, never AI versions of Jason/Lucia passed off as official.
  * Build: `tools/meme_build.py media/configs/<name>.json` (white pill caption, pops for punchline, footer
    with AI label + fan-page line, music loudnorm -14). AI clips: ElevenLabs kling-2.5-turbo, 9:16, 5 s,
    ~2.1k credits each (Seedance 2.5 = 14k, too pricey). Keep raw AI clips in media/raw/ai/ for reuse.
  * Write 5 captions per idea, pick the one a 19-year-old would send to the group chat. If you have to
    explain it, kill it.

## Wins

## Losses

## Weekly reviews

## Notes
- 2026-11-18 04:15 run: no GTA 6 posts sent yet (first goes out 08:15), so nothing to score. Test set up for
  this run: a no-VO text-over-clip MEME (meme_nz_wait, 11 s) vs the VO info videos (launch v4, how-to v5),
  same platforms, same day. Compare shares+comments per view at the next run.
- Build env: system Pillow is broken in fresh containers; run info_build.py with a venv python
  (`python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pillow`). Memes without voice: pass a silent
  mp3 (media/raw/silence_10s.mp3) as `vo` and `words: []`; keep title2 at size <=46 for long lines.
- 2026-11-18: The TikTok account still shows older Fortnite posts (Sep–Nov 2026) from a previous niche.
  Expect early GTA 6 reach to come from non-followers; judge posts on reach, not follower count.

## Tools (2026-11-18)
- `media/official/trailer2_landscape_clean.mp4`: official GTA 6 Trailer 2, 1920x772, watermark + black bars
  cropped, no audio. Use as background footage (credit "Footage: Rockstar Games (Trailer 2)").
  Avoid ~0-6 s (rating card/fade), ~10 s and ~155 s (OpusClip emoji stickers), ~70-74 s ("Rockstar presents").
- `tools/info_build.py`: builds the owner's favourite info style (blurred bg + sharp band, one-word
  captions from ElevenLabs Scribe word timings, red arrow pop-ins, checklist). Pass PRECROP=null for the
  clean trailer file. Edit the `steps` list per video.
