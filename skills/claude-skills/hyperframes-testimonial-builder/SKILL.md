---
name: hyperframes-testimonial-builder
description: Turn real customer reviews, quotes, and case-study results into polished social-proof videos built in HyperFrames -- single-testimonial spotlights, review-wall montages, and stat-driven proof reels with captions and voiceover, cut for vertical, square, and wide. The highest-converting content most businesses never make.
tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch, Agent
model: inherit
---

# HyperFrames Testimonial Builder

Nothing sells like a customer saying it. This skill takes the proof a business already has -- Google reviews, testimonial emails, case-study numbers, NPS comments -- and directs it into renderable HyperFrames video. It owns the selection and the story; for composition mechanics, captions, transitions, and TTS, invoke the `hyperframes` skill (`hyperframes-cli` for `init`/`lint`/`preview`/`render`, `hyperframes-media` for voiceover).

## Step 1 -- Gather the proof

Take whatever exists: pasted reviews, a review export, `customer-review-aggregator` output, case-study docs, or a profile URL to pull from. For each candidate quote capture the text verbatim, the name/attribution available, the specific result mentioned, and the source.

Select for specificity: "They saved us $40K and two weeks" outperforms "Great company, highly recommend" every time. Rank candidates by concrete detail, emotional arc (skeptic-to-believer beats always-happy), and relevance to the audience the video targets.

## Step 2 -- Pick the format

- **Spotlight (20-30s)** -- one strong story: setup (the problem in the customer's words), the turn, the result, CTA.
- **Review wall (15-25s)** -- 4-6 short quotes in rhythm, star ratings and names, momentum building to an aggregate line ("300+ five-star reviews") and CTA.
- **Proof reel (30-45s)** -- stats-forward: animated counters for the numbers (customers served, dollars saved, rating), interleaved with the two best quote lines.

## Step 3 -- Build the composition

- Quote text is the hero visual: large, readable, animated in phrase by phrase, timed to the VO. Attribution (first name, business/role, star row) small and consistent.
- Verbatim always -- trim with ellipses where needed, never rewrite a customer's words into marketing-speak; the texture of real speech is the credibility.
- Brand rules honored: the business's palette and type (reuse a `claude-design-system-architect` or `design-style-installer` token set if present); no purple, no emoji.
- Captions synced (muted autoplay is the default viewing mode), counters and star fills animated deterministically per HyperFrames seek-safety rules, VO via the media pipeline reading the quotes with a neutral warm voice -- or silence with music-bed timing if the user prefers.
- Lint and preview before declaring done; never claim it renders without running the pipeline.

## Step 4 -- Deliver

Platform cuts (9:16, 1:1, 16:9), a thumbnail frame, and the caption text for the post. Note where each cut runs best: review wall for the Google Business Profile and Instagram, spotlight for the website hero and proposals, proof reel for paid.

## Rules

- Real quotes from real customers only. Never fabricate, composite, or "improve" a testimonial -- fabricated social proof is a legal problem, not a style choice.
- Get-permission reminder in the deliverable: quotes from private emails need the customer's OK before public use; public reviews are fair to feature.
- Attribution as strong as permitted: full name and business beats first name beats anonymous, in that order of asking.
- One result number per beat -- stacked stats blur; sequenced stats land.
- The CTA matches where the proof points: reviews about service -> book a call; reviews about results -> see pricing.

## Quick Commands

- "Testimonial video from [reviews/file]" -- full workflow, format recommended
- "Review wall from my Google reviews" -- wall format from a profile or export
- "Spotlight [customer story]" -- single-story treatment
- "Proof reel from [case study]" -- stats-forward cut
