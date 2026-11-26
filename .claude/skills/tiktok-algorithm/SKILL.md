---
name: tiktok-algorithm
description: Plan, script, and optimize TikTok (and Reels/Shorts) content in alignment with how TikTok's recommendation system actually ranks and distributes videos. Use when the user wants to understand the For You algorithm, decide what signals to optimize for, diagnose why a video under-performed, or align a script/caption/hashtags with ranking behavior. Grounded in TikTok's official documentation and ByteDance's open-sourced Monolith recommender.
metadata:
  version: 1.0.0
---

# TikTok Algorithm

Optimize short-form video for TikTok's recommendation system using evidence, not folklore. This skill separates what is **documented** (TikTok's own statements + ByteDance's published research) from what is **inferred** (creator-observed best practice), and never presents guesses as facts.

## When to Activate

- Planning or scripting a TikTok / Reels / Shorts video and deciding what to optimize for
- Choosing caption, hashtags, sounds, or posting cadence
- Diagnosing why a video under- or over-performed
- Explaining "how the For You Page works" without hype or myths

## Two-Layer Mental Model

Reason about TikTok on two layers. Confusing them is the most common mistake.

### Layer 1 — The System (how the model learns)
Source: ByteDance's **Monolith** recommender, open-sourced 2022 (github.com/bytedance/monolith, arXiv:2209.07663). Monolith is the *training/serving framework*, **not** the full "For You" ranking rulebook — treat it as directional, not a spec.

Two published properties matter for creators:

1. **Real-time / online training.** The model interacts with user feedback in near-real-time and explicitly trades system reliability for freshness to capture emerging trends fast.
   → **Implication:** the first hours after posting dominate. Early completion, replays, and shares are what the model learns from first. A weak open is not "slow to catch on" — it teaches the model to stop distributing.

2. **Collisionless embedding tables** (Cuckoo-hash based), with *expirable* embeddings and *frequency filtering* of rare features.
   → **Implication:** distinct signals are stored distinctly and persist — every interaction (watch %, rewatch, share, save, comment) feeds the profile. But stale/low-frequency signals decay, so consistency and recency beat a single old hit. Follower count is not a stored ranking feature (see Myths).

### Layer 2 — The Ranking Signals (what gets weighted)
Source: TikTok's official newsroom, "How TikTok recommends content." Three factor categories, **weighted unequally**:

1. **User interactions** — likes, shares, follows, comments, completions, content you create. *(Highest weight.)*
2. **Video information** — captions, sounds, hashtags. *(How the system understands/indexes the video.)*
3. **Device & account settings** — language, country, device type. *(Lowest weight; not an expressed preference.)*

TikTok states finishing a longer video start-to-end is **a strong indicator of interest** weighted above demographic factors.

## Signal Hierarchy (optimize top-down)

Ranked by documented + widely-observed weight. Spend effort where the weight is.

| Tier | Signals | What it rewards |
|---|---|---|
| **Strongest** | Watch time, **completion rate**, rewatches/loops | Content that holds and repeats attention |
| **Strong** | Shares, saves/favorites, comments, follows-from-video | Content worth passing on or keeping |
| **Moderate** | Likes | Passive approval (cheap signal) |
| **Lowest** | Device/account settings | Context, not merit |

Rule of thumb: **a share or a rewatch is worth far more than a like.** Design for the top of this table first.

## Actionable Playbook

### Hook (first 2 seconds)
- 71% of viewers decide in ~3s; on TikTok treat the budget as **2s**. Lead with the payoff, tension, or number — never a warm-up.
- The hook's job is to buy the *next* 2 seconds. Front-load the single strongest claim or visual.

### Hold completion (the #1 lever)
- Match length to substance. Shorter, fully-watched > longer, half-watched. Aim for a **completion-friendly length** (often 21–34s for awareness clips; only go longer if every second earns it).
- Cut every 2–3s; remove dead air; burn captions (many watch muted).
- Build a reason to reach the end (payoff, punchline, or list that resolves).

### Engineer replays & shares
- **Replays:** loop the ending into the opening, or pack info too dense to absorb once ("save this").
- **Shares:** make it useful, surprising, or identity-expressing ("send this to a dev friend").
- **Saves:** reference-style value (steps, a list, a resource) earns saves.
- **Comments:** plant one genuine question; pin a comment to seed replies. No engagement-bait if it's dishonest to the content.

### Video information (indexing layer)
- **Captions:** include real keywords the target searches — TikTok's AI reads captions to classify the video.
- **Sounds:** a trending/relevant sound can aid discovery; relevance over chasing every trend.
- **Hashtags: maximum 5.** TikTok rolled out a 5-hashtag limit (Aug 2025). Mix a couple of broad-reach tags with a few targeted niche tags. Every tag must earn its place — no stuffing.

### Timing & consistency
- Because training is real-time, post when your audience is active so early signals land fast.
- Consistency compounds (embeddings favor recent, repeated signals); sporadic posting decays.

## Diagnosing a Weak Video

Walk the funnel top-down and fix the earliest break:
1. **Low reach / stalled at a few hundred views** → weak early signals. Suspect the hook or completion, not "shadowban."
2. **Views but low completion %** → open is fine, middle sags. Tighten pacing, cut length.
3. **Good completion but no shares/saves** → entertaining but not passable/useful. Add a payoff worth sending.
4. **Good everything, still flat** → try a different sound/caption framing; the indexing layer may be mis-classifying the niche.

## Myths to Reject (stay honest)

- **"Follower count boosts the algorithm."** TikTok states follower count and past high-performers are **not direct ranking factors**. Big accounts get more views via their existing audience, not a model boost.
- **"There's a magic post time / hashtag that guarantees FYP."** No single tag or time overrides weak retention.
- **"Deleting and reposting resets the algorithm."** No evidence; you lose the original's accumulated signals.
- **"Shadowban explains my low views."** Usually weak early-retention signals. Only community-guideline violations restrict distribution; verify in the app rather than assuming.

## Honest Limitations

- Monolith is a *framework*, not the deployed "For You" ranking logic — use it for system intuition, not exact weights.
- Exact ranking weights are **not public**. This skill states directional weight (what TikTok confirms is stronger/weaker), never invented percentages.
- The platform changes; re-verify specifics (e.g., hashtag caps, length sweet spots) against current sources before relying on them.

## Output Format

When asked to optimize content, return:
- Which **signals** this piece targets (from the hierarchy) and why
- Hook, completion, and share/save mechanics baked into the plan
- Caption + ≤5 hashtags (broad + niche mix)
- What to watch in the first hours, and the diagnostic to run if it stalls

## Sources

- TikTok Newsroom — How TikTok recommends content: https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- Monolith (paper), ByteDance, RecSys 2022: https://arxiv.org/abs/2209.07663
- Monolith (code), ByteDance: https://github.com/bytedance/monolith
- TikTok 5-hashtag limit (Aug 2025): https://www.socialmediatoday.com/news/tiktok-implements-five-hashtag-limit-per-post/757857/

## Related Skills

- `video` / video-marketing — script structure and hooks
- `content-engine` — platform-native drafting
- `crosspost` — per-platform adaptation (Reels penalizes TikTok watermarks; Shorts needs searchable titles)
