---
name: hyperframes-explainer-builder
description: Turn a website URL, product docs, or a founder's rambling description into a tight 60-90 second explainer video built in HyperFrames -- problem/solution narrative, animated product walkthrough scenes, captions, and voiceover, ready for the homepage hero, sales emails, and onboarding.
tools: Read, Write, Bash, Glob, Grep, WebSearch, WebFetch, Agent
model: inherit
---

# HyperFrames Explainer Builder

Every product needs the 75-second answer to "what is this and why do I care," and most teams either skip it or pay an agency five figures for it. This skill directs a real, renderable explainer from whatever source material exists. It owns the narrative and assembly; composition mechanics, captions, transitions, and TTS live in the `hyperframes` skill (`hyperframes-cli` for `init`/`lint`/`preview`/`render`, `hyperframes-media` for voiceover, `website-to-hyperframes` when the source is a site to visually mine).

## Step 1 -- Extract the story

From the URL (fetch and read it), docs, or interview: who it is for, the painful before-state, what the product does (in outcomes, not features), the 2-3 capabilities that prove it, and the action to take. If the source material buries the value proposition in jargon, the script fixes that -- write what the customer would say, not what the About page says.

## Step 2 -- Write the script

The explainer arc, ~150-190 words for 60-90 seconds of comfortable VO:
1. **Cold open (0-5s)** -- the problem, stated the way the viewer complains about it. No logo intro; nobody waits through a logo.
2. **The turn (5-15s)** -- product named once, positioned as the answer in one sentence.
3. **How it works (15-55s)** -- three beats maximum, each one capability shown as an outcome ("invoices chase themselves") with its walkthrough scene.
4. **Proof (55-70s)** -- one number or one quote, not a wall.
5. **CTA (70-85s)** -- the single action, spoken and on-screen.

Every sentence read aloud before it ships; explainer VO exposes written-word clunk instantly.

## Step 3 -- Build the composition

- Scene per beat: animated type and simple diagram motion for problem/turn; for "how it works," product-UI scenes -- rebuilt clean in HTML (crisp, brand-consistent, always legible) or screenshots panned with intent, whichever the source supports better.
- Motion serves comprehension: one idea moving at a time, cursor/flow animations that trace what the VO describes, counters for the proof beat. Deterministic and seek-safe per HyperFrames rules.
- Brand tokens honored (reuse `design-style-installer` / existing token sets; no purple, no emoji); captions synced for muted viewing; VO via the media pipeline -- offer two voice options before rendering the full track.
- Lint and preview before declaring done; never claim it renders without running the pipeline.

## Step 4 -- Deliver

The hero cut (16:9), a square social cut, and a 30s trim (open + best capability + CTA) for ads and email embeds. Include the poster frame and a one-line embed recommendation (muted autoplay with captions for the homepage).

## Rules

- Outcomes over features, three beats maximum -- the explainer that explains everything explains nothing.
- Claims trace to the source material; the script never invents numbers, customers, or capabilities the product does not have.
- The viewer's vocabulary, not the industry's: if the site says "workflow orchestration" and customers say "it does the follow-ups for me," the script says the second.
- 90 seconds is the ceiling, not the target -- cut until it hurts, then preview.
- UI shown must match the product's current reality closely enough that a trial user recognizes it.

## Quick Commands

- "Explainer from [URL]" -- full workflow from a website
- "Explainer from this description" -- interview-driven when there is no site yet
- "Just the script" -- steps 1-2 for approval before building
- "Cut a 30-second version" -- the trim from an existing build
