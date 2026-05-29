---
name: ship
description: >-
  End-to-end branch delivery: commit (no AI attribution) → push → open a pull request → link the
  work item → after merge, clean up branch and worktree. Auto-detects the platform from the remote —
  Azure Repos + Boards (`az`, with an OAuth Bearer push fallback) or GitHub (`gh`). Use whenever
  asked to "ship", "ship it", "ship this branch", "open a PR", "push and open a PR", "raise a PR",
  "deliver this", "send this for review", or "create a PR and link the work item" — and when a
  direct push to main is blocked and the change needs to go through a PR instead.
allowed-tools:
  - Bash
  - Read
metadata:
  platform: azure-devops, github
---

# Ship

`ship` takes a finished branch the last mile: commit it cleanly, push it (working around Azure
DevOps auth when needed), open a pull request, link it to its work item, and — once it's merged —
tear down the branch and worktree. It auto-detects whether you're on **Azure Repos** or **GitHub**
and follows the matching path, so the same command works at Hypera and in a github.com repo.

It is deliberately narrow. It does *not* merge locally, run pipelines, or manage backlogs — it
hands a reviewable PR to the platform and cleans up after the merge.

## When to use this vs. neighbors

- **`ship`** — the PR-based delivery flow: push → PR → (merge happens via the platform) → cleanup.
- **`commit`** — just stage + commit + push the current branch, no PR.
- **`merge`** — merge a branch into `main` *locally* (fast-forward) and clean up. Use this when there's
  no PR gate; use `ship` when changes must go through review/policy.
- **`azure-devops`** — the deep REST/MCP toolbox (WIQL, batch updates, pipelines, comment threads).
  `ship` calls only the thin slice it needs; reach for `azure-devops` for anything richer.

## The flow

Run `scripts/ship-detect.sh` first — it prints the platform, the Azure org/project/repo (if any),
the branch, and an inferred work-item id. Everything below branches on that.

### 0. Preflight
- Confirm there's something to deliver: `git status` and `git log --oneline @{u}.. 2>/dev/null`.
- Note the platform from `ship-detect.sh`. If it says `unknown` (e.g. a custom SSH host alias),
  set `SHIP_PLATFORM=azure` or `SHIP_PLATFORM=github` for the session.

### 1. Commit — as the author, never as the tool
Stage only files for this task and commit. **Never add AI attribution** — no
`Generated with Claude`, no `Co-Authored-By: Claude`. Commits are authored by the human; tooling
provenance does not belong in git history (this repo's `commit-msg` hook strips trailers as a
backstop, but don't rely on it — don't write them in the first place). If pre-commit hooks fail on
*unrelated* issues, `--no-verify` is acceptable; if they flag *your* change, fix it.

### 2. Branch posture
- **On a feature branch** → good, continue.
- **On `main`/`master`** → you can't open a PR from main into itself. Create a branch and move the
  commit onto it before pushing:
  ```bash
  git branch feature/<slug> && git reset --hard @{u} && git checkout feature/<slug>
  ```
  (Only do this when the commits aren't yet pushed to main. If unsure, stop and ask.)
- A **blocked direct push to main** (branch policy) is the signal to take the PR path — not to
  force-push or bypass the policy.

### 3. Push
```bash
bash scripts/ship-push.sh        # pushes current branch, sets upstream
```
On Azure DevOps, if the normal push fails on auth, this automatically mints an `az` OAuth token and
retries with a Bearer header — the fallback for when neither SSH nor an HTTPS credential helper is
available. See `references/azure-devops.md` for the mechanics.

### 4. Open the PR (+ link work item, + transition state)
Draft a real description — copy `assets/pr-template.md` to a temp file, fill Summary / Changes /
Verification, and keep the `AB#<id>` line so the work item links.

```bash
bash scripts/ship-pr.sh --title "<title>" --body-file /tmp/pr-body.md \
  --work-item <id> --transition Resolved
```
- Platform is auto-detected; the script picks `az repos pr create` or `gh pr create`.
- `--work-item` is inferred from the branch name when omitted — pass it explicitly if the branch
  doesn't carry it. Confirm the id is right before linking.
- `--transition` (Azure only) moves the Board item *after* the PR opens. State names are
  process-specific (Agile: Resolved; Scrum: Committed; Basic: Doing) — verify the valid next state
  first; see `references/azure-devops.md`. Omit `--transition` to leave the board untouched.
- The script prints `pr_url=…`; surface it to the user.

### 5. After merge — cleanup
Do this only once the PR is actually merged (don't delete a branch with an open PR). Mirror the
`merge` skill's cleanup, and **ask before deleting**:
- If the branch was developed in a **worktree**, `cd` to the main repo dir first, then
  `git worktree remove <path>` — you can't delete a branch from inside its own worktree.
- `git branch -d <branch>` (lowercase `-d` refuses unmerged branches — that refusal is the safety
  net; only escalate to `-D` if the user explicitly confirms).
- `git push origin --delete <branch>` (ignore failure if it was local-only).

## Bundled tools

| Script | Does |
|--------|------|
| `scripts/ship-detect.sh [remote]` | Print platform + Azure coordinates + branch + inferred work item |
| `scripts/ship-push.sh [-r remote] [-b branch]` | Push + set upstream; Azure OAuth Bearer fallback on auth failure |
| `scripts/ship-pr.sh --title … [opts]` | Open PR on the detected platform; link work item; optional Board transition |

Platform-specific detail lives in `references/azure-devops.md` and `references/github.md` — read the
one matching the detected platform. The PR description starts from `assets/pr-template.md`.

## Safety

- **Ask before anything destructive or shared-visible** — deleting branches/worktrees, and opening a
  PR (it's visible to the team). Pushing a feature branch and creating a draft are low-risk; a
  ready PR and any branch deletion warrant a confirm.
- **Never force-push** to work around a rejected push. A rejection means diverged history or a
  policy — investigate, don't overwrite.
- **Tokens go in headers, are short-lived, and are never printed or put in URLs.**
- **No AI attribution** anywhere — commit message, PR title, or PR body.

## Gotchas

- `gh pr create` and `az repos pr create` both require the branch to be **pushed first** — keep
  step 3 before step 4.
- `ship-detect.sh` returning `unknown` is almost always a custom SSH host alias — set `SHIP_PLATFORM`.
- A linked work item does **not** change state on its own; transitioning is a separate step (4).
- Deleting a branch while its PR is still open abandons the PR — clean up only after merge (step 5).
