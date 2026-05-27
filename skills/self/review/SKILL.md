# TOP-SKILLS Code Review Standards

Review all changes against these standards before committing.

## General Rules

1. **No emojis in code files** — only in README/CHANGELOG
2. **No comments** unless the WHY is non-obvious
3. **Minimal diffs** — only change what's needed, no scope creep
4. **No backwards-compatibility hacks** — if something is unused, delete it
5. **Safe by default** — no command injection, XSS, or security regressions

## Dashboard (index.html)

- All text strings MUST use the `I18N` + `t()` system
- All chart creation MUST be wrapped in try-catch
- CSS changes should use `:root` variables, not hardcoded colors
- No external dependencies beyond Chart.js CDN
- Responsive: test at 768px breakpoint

## Data Pipeline

- `source_descriptions` must use `"EN / ZH"` format with ` / ` separator
- JSON output must use `ensure_ascii=False` for Chinese support
- Git timeline must deduplicate by skill directory, not file path
- All scripts should handle re-entrant execution (safe to run multiple times)

## README / CHANGELOG

- README is bilingual (Chinese + English)
- CHANGELOG uses categories: **新增** / **修复** / **变更**
- All dates in CHANGELOG use YYYY-MM-DD format
- Badges in README should be kept up-to-date

## Git

- No force push to master
- No `--no-verify` to skip hooks
- No committing .env, credentials, or tokens
- Commit messages should explain WHY, not WHAT
- Separate functional changes into distinct commits
