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

- TWITCH CLIP PULL (tested 2026-11-18): yt-dlp works per channel (list top clips by views, range 24hr/7d,
  download 1080p mp4). `tools/twitch_clips.sh` loops over Twitch creators in watchlist.md. NOT working:
  whole GTA 6 category listing (yt-dlp unsupported; unofficial Twitch API rejected). Full-category
  discovery: `python3 tools/twitch_top.py <hours> <n> <langs>` (official API, WORKS since 2026-11-18;
  token = env var TWITCH_TOKEN in the CLOUD gta6 environment, verified working 2026-11-18; expires ~60 days (~mid-Jan 2027) -> on 401 tell owner to redo the authorize link with redirect_uri https://github.com/73Cosmin/gta6channel and update the variable). Download a clip with
  yt-dlp <clip url>. Skip anything claiming to play early / before release (hard rule 4).

- OWNER (2026-11-18): don't filter clips for crude/dark/edgy humor; owner likes black humor (e.g. MontanaBlack).
  Only reject for the hard rules (leaks/play-early, spoilers, unverified facts, takedown list) or content
  that would get the post removed by the platform (slurs, nudity, real threats).

- Trailer 2 file ends (~2:40) on the OLD date card "MAY 26, 2026". Never use frames/clips from ~2:35 on.

## Wins
- 2026-11-18 MontanaBlack TikTok (30 s, German, edgy line): 376 views/14 likes/1 share in ~40 min, 3.99% eng. but
  0 comments and avg watch 9.6 s = viewers leave at ~1/3. LESSON: cut creator clips to 10-15 s with the punchline
  inside the first 3 s, and end the caption with a question that forces a pick (A or B?) instead of an open
  'what do you do first?' -> applied to tonight's 'Jason or Lucia?' X post.

- 2026-11-18 13:16 run: Buffer only refreshes TikTok metrics reliably; YT/IG/X still show the read taken
  minutes after sending (all 0) -> do not score those as losses, re-read next run. Only data point stays
  Monte TikTok (376 views, avg watch 9.6 s of 30 s). APPLIED: next creator clip cut to 12 s starting 0.4 s before
  the reaction line, title states the moment ("sieht GTA 6 zum ersten Mal"), end text + caption force an A/B pick
  ("Besser als GTA 5: ja oder nein?"). Test: does 12 s lift avg watch % and comments vs the 30 s cut?
- Build note: DejaVu font cannot draw emoji in burned-in text (renders boxes) -> no emoji in config text fields.

- 2026-11-18 16:15 run: still only ONE scored post (Monte TikTok 30 s: 376 views, avg watch 9.6 s, 0 comments).
  Buffer has not refreshed any YT/IG/X metric since send, and newer TikToks show stale 0s -> no new winners/losers yet.
  APPLIED: (1) fail/punchline inside the first 2 s (xQc thrown out of the car at 1.5 s), 15 s total;
  (2) first ENGLISH creator clip (all earlier clips were German) to test reach with the US/EU-English audience;
  (3) A/B question in caption + end card ("Harder than GTA 5?"). Compare vs Monte 12 s DE clip next runs.
- 2026-11-18 21:45 EVENING REVIEW: 29 posts sent Nov 18, 0 errors. Buffer metrics are FROZEN at send time for every
  post (metricsUpdatedAt = send minute; IG returns no metrics at all); aggregate endpoint also only knows the Monte
  TikTok. Best = MontanaBlack TikTok 30 s (376 views, 14 likes, 1 share, 0 comments, 3.99% eng.). Worst = not
  measurable (no other post has a real read; do NOT count stale 0s as losses).
  RULE: never change format/slot because of Buffer 0s. A post only counts as a win/loss once its metricsUpdatedAt is
  >=3 h after sentAt; otherwise leave scoreboard blank and ask owner for native-app numbers (TikTok/YT Studio/IG).
  TOMORROW'S TEST (one variable = LANGUAGE): EN vs DE creator clips at the same length (12-15 s, punchline <=3 s,
  A/B caption). Compare xQc/ohnePixel (EN, Nov 19 00:30/02:00) vs Monte 12 s (DE, Nov 18 15:15) on TikTok views
  + avg watch % once real reads exist. Name: lang_en_vs_de.
- Build note: title1 at size 96 overflows 1080 px past ~16 characters -> use 84 for 17+ chars; end_text max ~22 chars.

## Losses
- 2026-11-18: none measurable (Buffer metrics frozen at send for all posts except Monte TikTok).

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
- 2026-11-18 07:18 run: still no GTA 6 post old enough to score (first sends 06:58-07:02). Old Fortnite TikToks
  show the pattern to copy: posts with a question/claim caption ("Do you also think I am the best console
  player?", 8.6k views) out-reach plain emoji captions ~8x; avg watch 7-20 s -> keep clips <=20 s.

- 2026-11-18 19:15 run: still no fresh numbers (Buffer metrics frozen at send time for YT/IG/X and recent TikToks), so no new winner/loser yet. Applied existing lesson: clip cut to 13.6 s, fail lands at ~9 s, A/B question in caption. NEW craft rule: Twitch clips often fade to BLACK after a WASTED screen -> always end the cut on the WASTED card (check the last 3 s for black before publishing). Fallback when ElevenLabs is down: `python3 -m pip install faster-whisper` + model 'small' with word_timestamps (wrap the loop in try/except, it can crash on the final segment).

- ELEVENLABS VIA ENV (owner, 2026-11-18): the MCP connector failed (400), so the owner added the API key as env var ELEVENLABS_TOKEN
  in the cloud gta6 environment (same as TWITCH_TOKEN). Use `tools/eleven.py` (check/tts/scribe/music). It only
  reaches sessions started after the variable was added. Run `python3 tools/eleven.py check` at the start of a run;
  on 'No ElevenLabs key' or HTTP 401 -> tell owner (ACTION NEEDED) the variable is missing/expired.

- 2026-11-18 22:15 run: still no real reads (Buffer frozen at send for all but Monte TikTok) -> no new winner/loser; rule stands.
  NEW craft lesson: many top Twitch "GTA 6" clips are (a) muted/silent re-uploads or (b) the game's own story dialogue, not
  the streamer talking (Speed robbery: lines are Lucia's, in-game subs visible). Check volumedetect (> -60 dB) and the in-game
  subtitle line before picking; prefer clips where the STREAMER reacts. Applied: rejected silent Kai clip; Speed clip labelled SPOILER.
  Twitch clip "uploader" in yt-dlp is the clipper, not the streamer -> name files by the clip URL, credit the channel.
