# Learning

## Current Rules
- (2026-11-21 07:30) No Buffer refresh since 02:18 UTC (all numbers identical to the 04:18 run; rewi quote cut 07:00 too fresh) -> no new scores. Applied standing rules: (1) Mentality = 2nd proven winner (5,266 views, 16.55 s avg watch) -> built 'Papaplatte GTA 6 Mentality' (5 beats: 'vorsichtig fahren' setup -> Militärbasis-Tor -> 5 Sterne Jet -> Motor aus/WASTED -> '1500 Dollar geblowt, aber wir hatten einmal das Gefühl'; 34.7 s) for TT Nov 22 21:00 = 1 Mentality/day from a different DE streamer; (2) compilation-overlap rule: Eli Kroko quote cut could not move to Nov 23 (in the Top 3) -> Nov 24 07:00. Test mentality_streamer: does a Papaplatte Mentality reach Monte's 5.2K/16.5 s? Craft: Papaplatte cam (KoRo clipper edits) facecam [1480,300,440,286], game_crop [430,40,880,915] keeps the clipper subs (y~1000) and the KoRo logo out; story stills crop h<=960 to drop burned-in subs.
- (2026-11-21 04:20, Buffer TikTok refresh 02:18 UTC) Monte 'Mentality' v2 (35 s) = 5,266 views / 59 likes / 9 shares at 6.3 h, avg watch 16.55 s (best ever) vs Top-5 'Streamer-Fails' (66 s) 667 views at 9.6 h (avg 14.35 s) and Monte Billard (33 s) 718 at 13 h (avg 6.4 s). Delfin 75.4K / 2,236 likes / 254 shares. YouTube Shorts: Top-5 and Papaplatte Tankstelle = 1 view each at 9-15 h -> YT still not distributing. RULES: (1) compilations <=45 s with 3 items (applied: Nov 23 'Top 3 Tier-Momente', 41.7 s); (2) YouTube max 1 Short/day from Nov 23 (only the daily creative, 17:30) until a Short beats 50 views; YT 11:30 slots stay empty; (3) the Mentality format is our 2nd proven winner -> keep 1 per day from a different DE streamer.
- (2026-11-21 03:11, OWNER TikTok profile) Delfin 75.4K views but account only 53 followers (~25 from the video, ~0.03%). Diagnosis: one-off viral video, profile gives no reason to follow (no pinned videos, grid mixes English CaseOh posts with German Monte, nothing tells the viewer 'more of THIS is coming'). FIX: SERIES. Follow-up to a viral video within 24-36 h, labelled 'TEIL 2' in the hook + 'FOLG FÜR TEIL 3' card in the last 3 s + caption 'Teil 2 nach dem Delfin ... Folg für Teil 3'. Monte Krokodil moved to TT Nov 21 21:00 as Teil 2 (tips video -> Nov 22 10:30). Owner actions: pin Delfin (+ Mentality 5.2K) on the profile, pinned comment on Delfin pointing to Teil 2, set the English CaseOh posts to private. Measure: followers gained per 10K views on Teil 2 vs Delfin.
- (2026-11-21 01:20, FIRST BUFFER TIKTOK REFRESH SINCE NOV 19, read 21:46 UTC) Monte 'Mentality' v2 (35 s, cards+hits, no music) = 2,449 views / 27 likes / 9 shares at only 1.8 h, avg watch 16.4 s = our best avg watch ever (Delfin 13.1 s) -> the Mentality format holds people. Top-5 'Streamer-Fails' TT (66 s) = 450 views / 13 likes at 5.3 h, avg 13.8 s of 66 s (most leave before #1); Monte Billard (33 s) 574 views, avg 6.7 s = hook lost them. IG Top-5 = 0 views/0 reach at 7 h (IG suppression after the originality warning) vs IG Papaplatte 197. RULES: (1) build 1 Mentality edit per day from a DIFFERENT DE streamer (Eli today, Papaplatte/Trymacs next), 35-40 s, put it in the best TikTok slot; (2) compilations/Top-5 <= 45 s (3 items, not 5) - long countdowns lose half before the payoff; (3) IG: watch the Nov 21 Top-5 IG read - if 0 again, pause IG and tell owner.
- (2026-11-21 00:20, OWNER) Instagram warning 'Content you recently shared may go against our originality guidelines' (~21 h old = Nov 19 single re-cuts: Monte Schradin, CaseOh, Speed, ohnePixel). IG punishes aggregator re-uploads much harder than TikTok. RULE: IG = only our own creative formats (Top-5, Versus, supercut, DE tip video), max 1/day; single creator clips TikTok/YouTube only. The 2 scheduled IG singles were moved to drafts.
- (2026-11-20 23:51, OWNER screenshot) Top-5 'Streamer-Fails' layout broken on TikTok (560 views): title in the black header ran under the search bar and off both edges, ranking list at x 36 was cut off on the left, credit sat under the TikTok caption. Cause: phones are 19.5:9 -> TikTok crops ~100 px per side; UI covers top ~230 px and bottom ~360 px. FIX: top5_build.py rebuilt TikTok-safe (no header; coloured title words in black boxes on the facecam/gameplay seam; list x>=130 at y 990; captions y 1420; credit y 1490), Nov 21 Top-5 + Nov 22 Versus re-rendered (_safe.mp4) and swapped in all 6 Buffer posts. info_build defaults: credit_y 1480, end_text_y 960 for new builds. RULE: every new video gets a phone-crop check frame (crop=883:1920:98:0) before publishing.
- (2026-11-20 23:55, OWNER) Mentality edits: put the black 'Monte GTA 6 Mentality' card + its hit sound ALSO at the very start (0.0 s), so a viewer swiping by knows the format immediately - otherwise it looks like a random clip. Done in tools/mentality_build.py (intro_card default true). General lesson: the format/brand signal must be in the first frame.
- (2026-11-20 23:46, OWNER TikTok Studio) Monte 'Delfin' at 13.3 h: 72.2K views (5x the 2.9 h read, still climbing), 2,100 likes, 46 comments, 248 shares, 322 saves, avg watch 13.1 s of 23.7 s (up from 11.2 s), 22.1% full (up from 16%), 28 new followers (was 0). Saves (322) > shares (248) > comments (46) -> people keep it; interaction rate ~3.8% likes/views. The slow-mo replay half is now watched more (22% full) -> keep the 20-30 s replay format, don't cut to 12 s for Monte. Followers finally convert (28) -> German bio/DE niche works. RULE: Delfin = the template (DE top creator + animal + black humor + harmless wrong detail in hook + SPOILER + A/B). Make 1 'animal' Monte/DE clip per day while it works (Krokodil 'Pony' clip Nov 22 10:30 = first repeat) and build the Nov 23 creative as 'Top 5 Tier-Momente'.
- (2026-11-20 22:17) 8th run without a Buffer metrics refresh -> nothing new to score. Applied the Delfin recipe on purpose: Monte + animal + ONE harmless wrong visual detail in the hook (deer called 'PONY') + A/B end question; new test animal_wrongdetail (compare its TikTok views/comments vs Delfin 14.3K at the same age). Craft: (1) system python PIL is broken in this container -> run builds with /tmp/venv/bin/python (pip install pillow numpy yt-dlp); (2) end_text max ~20 chars ('FALSCHE BEUTE ODER SKILL ISSUE?' ran off both edges); (3) cut dead air with a 2-segment pre-concat BEFORE replay_extend so total stays <30 s.
- (2026-11-20 21:45 evening review) BEST today: Monte 'Delfin' TikTok (stacked, DE, black humor, wrong-animal hook) 14.3K views/273 likes/22 shares/31 saves at 2.9 h (owner read). WORST today: CaseOh 'Grandma Peggy' TikTok (EN, old band layout, 07:00) 258 views at 3.7 h = 55x less in the same morning. RULE (confirmed): packaging + language decide reach - every TikTok = DE streamer + stacked layout + a hook that withholds the payoff; no EN singles, no band layout for streamer clips. Buffer TikTok metrics frozen 22 h (7 runs) -> owner TikTok Studio reads are the only truth until Buffer refreshes. TOMORROW'S TEST (one variable = FORMAT LENGTH): quote_cut_vs_full - Nov 21 TikTok quote cuts (rewinside 07:00, 12 s; Giggand 14:00, 7 s) vs full slow-mo-replay clip (Papaplatte Flugzeug 10:30, 27 s); same language (DE), same layout (stacked). Compare views + avg watch % at 12 h.
- (2026-11-20 19:16) 6th run without a Buffer metrics refresh -> no new numbers. Applied: DE creators only, A/B question in every caption, fresh-first swaps. New test versus_ab: an A-vs-B creative (two DE streamers doing the same kind of thing, viewers vote A/B) should pull more COMMENTS than a Top-5 because answering takes one letter - compare comments/views vs the Top-5s (Nov 20/21) once metrics exist. Scheduling lesson: never let a single clip run on the same day as a compilation that contains it (Monte Apfel was in the Nov 21 Top-5 AND a Nov 21 single) - check new creatives' items against the same day's singles. Craft: yt-dlp/ffmpeg inside a `while read` loop eat stdin -> always use `-nostdin` / `</dev/null`.
- (2026-11-20 15:16) 5th run without a Buffer metrics refresh -> no new numbers; owner screenshots stay the only source (Delfin 14.3K). Applied standing rules: DE creators only, quote cuts 1-2/day, first German helpful tip video built (TikTok search boost). Craft: (1) quote_cut emoji = ONE plain emoji - ZWJ emoji (🐻‍❄️) splits into 2 glyphs and pushes line 2 off-screen; (2) info_build pop_texts are fixed 64 px -> max ~20 chars; credit line max ~55 chars at 28 px (drop '(Twitch)' for 4 creators); (3) a 'tip' video can be built 100% from credited streamer fails ('4 Fehler, die dich sofort killen') = helpful format with zero guessed mechanics. Test helpful_search_de: compare its TikTok views/saves vs quote cuts once metrics exist.
- (2026-11-20 13:15) 4th run without a Buffer metrics refresh (TikTok last read 22:44 UTC Nov 19) -> no new numbers, standing DE rules applied. Testing 2 new DE creators (rewinside quote cut, Eli Sandwich) to find a 2nd Monte-level source; compare their TikTok views vs Monte/Papaplatte. Craft: quote cuts where line and fail are far apart -> pre-concat line + fail into one file (cut the menu/inventory dead air); long quotes -> "\n" in the config for 2 lines; Twitch clipper subs sit at y~1000 -> game_crop y<=970.
- (2026-11-20 13:26, TikTok notice) TikTok BOOSTED our HOW TO video ('How to play GTA 6 the second it unlocks', EN, Nov 18) as a 'helpful post': +398 extra views, ~7 people found it via SEARCH and shares. TikTok's helpful-post program wants: video >20 s, useful details, honest tips. -> Add 1 helpful/searchable video every 1-2 days in GERMAN with search-style titles ('GTA 6 Tipps für Anfänger', 'GTA 6 schnell Geld', 'GTA 6 Einstellungen'), 25-40 s, info layout + Nicholas voice. Content only from official sources (facts.md) or things clearly visible in streamer gameplay (credited) - never guessed mechanics.
- (2026-11-20 13:24, TikTok Studio) FIRST VIRAL POST: Monte 'Delfin' 14.3K views in 2.9 h (19x our previous best), 273 likes, 22 shares, 31 saves; comments = 'das ist kein Delfin'. Winning recipe = DE top creator (Monte) + black humor + question hook that withholds the payoff ('WAS SOLL SCHON PASSIEREN?') + ONE harmless wrong visual detail in the hook + SPOILER tag + A/B end question. Avg watch 11.2 s of 23.7 s (16% full) -> the slow-mo replay half is mostly skipped; test shorter (12-16 s) Monte cuts next. 0 new followers from 14K views -> profile doesn't convert (English bio for a DACH audience); asked owner to switch the bio to German.
- (2026-11-20 12:10, OWNER) 'Delfin' title was an accident (it's an orca/Wal) but the wrong word drove lots of 'das ist kein Delfin' comments -> owner wants more. RAGEBAIT TRICK: one harmless, obviously wrong on-screen detail (animal, car, colour, name of an object) in the hook/caption. Only trivial visual details the viewer can see for himself; NEVER wrong game facts, news, dates, features or quotes (hard rules 1-2).
- (2026-11-20 11:53, OWNER) Monte Delfin TikTok (stacked, 24 s, SPOILER, black humor, 'Lustig oder traurig?' A/B) = BEST so far: 1898 views in 1.4 h + most comments. Owner likes it. Repeat: Monte + black humor + stacked + A/B question. NEW FORMAT from owner ref (media/references/mentality_eli.mp4): '<Name> GTA 6 Mentality' edit = facecam top 0-800 / gameplay below, 0.7 s black cards with plain white '<Name> GTA 6 Mentality' + boom between beats, phonk bed starts at first card (setup beat has no music), punchy contrast/saturation grade, fast hard cuts, ~35 s. Tool: tools/mentality_build.py.
- (2026-11-20 10:42, OWNER + TikTok screenshot) 'Die CaseOh Videos laufen nicht gut.' TikTok views: Papaplatte Tankstelle 785 (11.7 h), Monte Schradin 759 (22 h) vs CaseOh 200 IQ 262 (18.5 h), CaseOh Peggy 258 (3.7 h), CaseOh seaplane 134 (15 h). DE clips get ~3-5x the views. RULE: NO MORE CaseOh / EN creator single clips on any platform; only German streamers (Monte > Papaplatte > Trymacs/Giggand/xrohat). EN creators only inside compilations if at all.
- (2026-11-20 10:15) Still no Buffer refresh (3rd run in a row) -> no new numbers; kept DE/Monte rule. Craft: info_build red_words match the word WITHOUT punctuation ("WHOOPS", not "WHOOPS."). Monte facecam this week sits at x~1210-1710, y~745-1070 of 1920x1080; keep facecam x>=1200 so in-game subtitles at x<1200 don't leak into the top panel.
- (2026-11-20 07:15) No Buffer refresh since 22:44 UTC -> no new numbers. Applied standing rules: tomorrow's creative built a day ahead (DE-only Top-5, Monte-heavy = proven winner). Test top5_de_vs_top5_mixed: compare Nov 21 DE Top-5 vs Nov 20 mixed Top-5 on TikTok views/likes and YT views. Craft: pre-concat a cut (setup + payoff, drop the silent middle) when a top-5 item has dead air; top5 configs >70 s go over 50 MB at crf 23 -> use "crf": 25.
- (2026-11-20 04:15) No new metrics (Buffer last refresh 22:44 UTC) -> no new lesson; kept applying DE-creator rule (Papaplatte next). Scheduling check: always list TikTok posts per slot before adding one - 21:00 Nov 20 had 2 clips (fixed). Twitch clipper edits often burn in their own subs at y~1000-1060 + in-game subs at y~950: crop game_crop to y<=920.
- (2026-11-20 research, see research/2026-11-20_algorithm.md) YouTube cut reach for Shorts that re-upload other creators' videos (TeamYouTube 2026-10-01); even narration voice-over doesn't count. Our stream re-cuts = exactly that -> explains 0 views. TikTok same idea ('unoriginal'). Need OUR idea/voice per video (own gameplay, rankings/debates/compilations around a take); #shorts not needed, 3-5 hashtags.
- (2026-11-20 03:37, YT Studio) YouTube Shorts: all public, no copyright/restriction, but 0 views on every Short after the first Monte one (531). Not blocked -> not distributed (new channel, 1 sub, ~8 short re-cut Shorts in 24 h). Test today: 20-23 s slow-mo replay versions. If still 0 after 12 h -> YT 1/day max or pause.
- (2026-11-20 01:15, FIRST BUFFER REFRESH IN 23 h, read 22:44 UTC) LANGUAGE DECIDES TIKTOK REACH: DE creator clips get the push, EN ones don't.
  TikTok: Monte Schradin DE 757 views/26 likes/1 share (10.9 h); Papaplatte DE 317 views/22 likes in 42 min (6.9% eng., before the 'unoriginal' flag);
  CaseOh EN respray 118/5 (7.4 h); CaseOh EN seaplane 85/0 (4 h); EN night clips 0-4. The account's audience is DACH -> every TikTok/YT/IG slot = German
  streamer (Monte first, then Papaplatte/Trymacs/xrohat/rewinside). EN creators only if the moment is huge. APPLIED: swapped YT/IG 17:30 CaseOh seaplane -> Monte Polizei;
  new clip = Monte (Apfel). Test name de_vs_en.
- (2026-11-20 01:15) IG Monte Schradin = 0 reach after 12 h while IG CaseOh got 234 views/11.95 s avg watch and IG HOW TO is at 1208 views -> IG may have
  suppressed the Schradin reel (old band layout, Opa joke). Watch the next DE IG reel; if it also gets 0, ask owner to check IG account status. X stays dead (1-31 impressions; best = image hot take 31, ranking 22).
- (2026-11-19 23:29, OWNER SCREENSHOT) TikTok restricted Papaplatte Tankstelle (12.3 s, posted 23:01) from the For You feed: "Unoriginal, low-quality" (= imported/copied without new creative edits; very short videos). Our stacked re-cut + captions + title is NOT enough transformation for TikTok. OWNER 23:40: NO AI voice on clips ("die ist nicht gut"). Fix = `tools/replay_extend.py` (slow-mo 0.5x replay of the payoff + 'NOCHMAL IN ZEITLUPE'/'SLOW-MO REPLAY' label, captions repeated) -> every creator clip 20-30 s. Avoid stream overlays/logos.
- (2026-11-19 22:15) Buffer metrics have been empty for ~22 h on TikTok/IG/X; until they refresh, keep repeating the only proven winner (Monte DE, edgy line, A/B end question) and judge nothing else.
- (2026-11-19 evening, data) YT/IG slots = strongest Monte-style clip only (big DE streamer, edgy line, full setup->payoff, 20-30 s). Info/hype and 12 s chops got 0 views on YT Shorts. Active test: stacked_vs_band.
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
- 2026-11-20 Monte 'Delfin' TikTok: 14.3K views/273 likes/22 shares/31 saves at 2.9 h (owner read) - first viral post; stacked + DE + withheld-payoff hook + wrong-detail ragebait.
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

- 2026-11-19 01:15 run — FIRST REAL READS (Buffer refreshed TikTok/IG at ~23:40 UTC; YT + X still useless):
  TikTok: MontanaBlack 30 s DE 782 views/34 likes/2 shares/1 comment, avg watch 11.95 s (best overall);
  HOW TO v5 info+VO 761/43 likes (most likes); Papaplatte 20 s 766/15; Monte 12 s cut 727/16, avg 5.8 s;
  launch v4 info+VO 715/15, avg watch only 3.6 s. IG: HOW TO v5 828 views/reach 720 (best IG by 4x);
  Monte 12 s 191; launch v4 96; two early IG reels reach 1. X: 0-7 impressions per tweet (account has no reach yet).
  LESSON 1: every TikTok lands at ~700-800 views (= baseline FYP push); what differs is likes/comments. The
  30 s Monte clip with a full setup->payoff arc beat the 12 s cut of the same streamer on likes (34 vs 16),
  shares and watch time -> do NOT chop clips to 12 s by default; keep the whole mini-story (setup + punchline),
  13-20 s, and remove dead air instead. LESSON 2: the useful HOW TO info video was the like/IG winner while the
  generic "it's out" hype video had the worst hook (3.6 s avg watch) -> useful/practical > hype; next info video
  should be a practical day-1 tip. APPLIED this run: CaseOh clip keeps full setup (red car -> respray black ->
  lies to the cop), 14.6 s, dead air jump-cut, A/B end question "Genius or lucky?".
- 2026-11-19 04:15 run: no Buffer refresh since 23:42 UTC, so no new winner/loser. Pattern so far: MontanaBlack (DE, edgy, full
  setup->payoff) is our best clip on likes/shares/watch time, and every daytime TikTok gets the same ~700-800 view push.
  APPLIED: next clip = Monte again (repeat the winner's creator + tone), 16.7 s with two segments and dead air cut,
  hook line ("Was macht denn Schradin hier?") in the first 0.2 s, A/B end card "Verdient oder zu hart?". Test monte_de_repeat:
  does a 2nd Monte clip beat the 34-like benchmark? Also first owner-style thirst post on X (Lucia, tall official still).
- 2026-11-19 16:15 run: Buffer still frozen since 23:42 UTC (16.5 h) -> no new winner/loser (the 2nd Monte clip went out 12:47, needs the nightly refresh).
  APPLIED the owner-ref lesson ("moment choice right, packaging was the gap"): Monte again (our best creator) in the STACKED layout with a
  question hook that withholds the payoff ("MONTE LÄSST DEN DELFIN FREI / WAS SOLL SCHON PASSIEREN?"), payoff at ~6 s, 23.7 s full arc,
  A/B "Lustig oder traurig?". Test stacked_vs_band: compare likes/shares/saves per view vs the band-layout Monte clips once reads exist.
  Craft: cutscene clips have letterbox bars + subtitles at y~930-1010 (1080p) -> game_crop [x,60,w,820] removes both; keep the facecam
  rect right of the subtitle line (x>=1250 for Monte's cam).
- 2026-11-19 19:15 run: Buffer still frozen since 23:42 UTC (~19.5 h, longest gap yet) -> no new winner/loser; best stays MontanaBlack 30 s
  TikTok (782 views, 34 likes, 2 shares, 1 comment). APPLIED: stacked layout + question hook that withholds the payoff ("KOMMT ER HIER NOCH
  RAUS?") + A/B end card, on a new DE creator (Giggand) to widen the creator pool. Craft: Twitch clips made by clippers often carry
  BURNED-IN purple-highlight subtitles at source y~990-1060 -> keep game_crop bottom <= ~940 and check the bottom edge of the gameplay half.
  If the nightly refresh stays missing again, ask owner for native TikTok numbers in the evening review.

- 2026-11-19 21:45 EVENING REVIEW: 0 Buffer errors. Buffer TikTok/IG/X feed still frozen since 23:42 UTC Nov 18 (~22 h) -> NONE of today's
  posts (Monte Schradin 12:47, CaseOh respray 16:17/17:31, seaplane 19:47, 8 tweets) has a real read; X today 0 impressions at send minute.
  NEW DATA: YouTube refreshed once (00:37 UTC): MontanaBlack 30 s DE edgy full-arc Short = 531 views / 7 likes (1.32%) at ~18.6 h;
  every other Short = 0-2 views (Papaplatte 20 s 2, launch info 0, HOW TO info 0, Monte 12 s cut 0).
  Best measured (3 days) = MontanaBlack 30 s: TikTok 782 views/34 likes/2 shares + YT 531 views. Worst = YT info/hype Shorts (0 views)
  and night TikToks (4 views).
  RULE: YT/IG only get 2 slots/day -> fill them with the strongest Monte-style clip (big DE streamer, edgy line, full setup->payoff,
  20-30 s); never spend a YT/IG slot on an info/hype video or a 12 s chop.
  TOMORROW'S TEST (one variable = LAYOUT): stacked_vs_band - same creator (MontanaBlack), same language, same black-humor tone:
  band layout "Opa Schradin" (Nov 19 12:47 TikTok) vs STACKED "Delfin" (Nov 20 10:30 TikTok). Compare likes+shares+saves per view and
  avg watch % once a real read exists.

## Losses
- 2026-11-20 CaseOh 'Grandma Peggy' TikTok (EN, band layout, 07:00): 258 views at 3.7 h vs Delfin 14.3K same morning -> EN + old layout dead on this DACH account.
- 2026-11-18 launch v4 info video: 3.6 s avg watch on TikTok, 96 views IG -> generic hype hook loses.
- 2026-11-18: none measurable (Buffer metrics frozen at send for all posts except Monte TikTok).
- 2026-11-18 YouTube Shorts: launch info 0, HOW TO info 0, Monte 12 s cut 0, Papaplatte 20 s 2 views (read ~8-18 h) vs Monte 30 s 531 -> on YT only the edgy full-arc clip got pushed.

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
- 2026-11-19 04:10 (owner + data): NIGHT POSTING LOSES. TikToks at 00:30/02:00/03:30 Vienna: 19/4/4 views after 1-3 h, vs
  715-782 for daytime clips (Monte TikTok had 376 within 40 min at 07:00). Even US-evening timing doesn't help: TikTok's
  first test audience for this account is EU. RULE: no videos 00:00-08:00 Vienna; clip slots 12:30/17:30/21:00 (+15:00 TikTok).
- 2026-11-19 OWNER: thirst/vibe posts on X (ref 'Mandy in GTA 6 🥵🔥' went viral). Rule added to playbook: real footage only (official or credited streamer gameplay), no AI fakes, no nudity, adults only, 1 per run on X in 16:45-22:45.
- 2026-11-19 07:15 run: Buffer still frozen since 23:42 UTC -> no new winner/loser. Only new data = owner's night TikTok reads (19/4/4)
  already turned into the no-night rule. APPLIED: first "impressive/jaw-drop" creator clip (CaseOh seaplane crash that floats) vs our
  funny/fail clips, same 12-15 s length, payoff line kept, rating-style A/B ("10/10 or 0/10?"). Test impressive_vs_funny: compare
  likes+shares/view vs CaseOh respray (Nov 19 17:30) once reads exist. Craft: X hot takes must not presuppose unconfirmed modes
  (e.g. "GTA 6 Online") - keep to official places/characters from the trailers.
- 2026-11-19 10:15 run: Buffer STILL frozen since 23:42 UTC (11 h) -> no new winner/loser; the TikTok metric feed seems to refresh
  only about once a day, so judge clips on the next nightly refresh, not per run. APPLIED the standing winners' pattern (full
  setup->payoff, DE big streamer, punchline line in the first 1 s, A/B end card "Mutig oder dumm?"): Papaplatte gas-station crash,
  12.3 s, cut ends ON the WASTED card (frame-checked at 13.9 s source, no black). New test fail_payoff_prime_time: first clip in the
  21:00 slot -> compare with the 12:30/17:30 clips once reads exist. Craft: info_build uppercases words and strips .,!? before
  matching red_words, and "ß" becomes "SS" (write red_words as e.g. "SCH*ISSE").
- 2026-11-19 13:00 OWNER REFERENCE (media/references/ref_stacked_monte.png, a Monte/Schradin repost with 8.9k likes, 958 saves,
  6k shares): STACKED layout looks much better than our blurred band -> new default for streamer clips: facecam full width on top,
  gameplay below, title = black TikTok Sans on white rounded line boxes on the seam, phrased as a question. Built into
  info_build.py ("facecam" key). Craft: pick a facecam rect with aspect ~1.54 that keeps the whole head (cap included); the
  gameplay half is a centre crop, so check that the action isn't at the far left/right. NOTE the reference got 958 saves +
  6k shares on the SAME Monte/Schradin moment we posted -> moment choice is right, packaging was the gap.
- 2026-11-19 13:15 run: Buffer still frozen since 23:42 UTC (13.5 h) -> no new winner/loser. Standing winners (Monte 30 s full arc 34 likes,
  HOW TO info 43 likes) say: full setup->payoff + a pick-a-side question. APPLIED: CaseOh "Grandma Peggy" keeps the whole callback arc
  (prediction at 1.5 s -> payoff at 9-14 s), black-humor A/B "Too far or funny?". New test morning_slot_dark_humor: first clip in the
  07:00 TikTok slot -> compare with the 12:47/16:15 clips once reads exist. Craft: top Twitch clips repeat across days (the 17k
  "How did they survive" = our seaplane clip) -> check media/raw/clips + Scribe text against earlier cuts before building.
