# TOP-SKILLS Data Pipeline Guide

You are maintaining the data collection, verification, and site generation pipeline for TOP-SKILLS.

## Pipeline Overview

```
config.yaml → collect_skills.py → verify_skills.py → generate_site.py → site/data/skills.json
```

## Collection (`scripts/collect_skills.py`)

- Reads sources from `config.yaml`
- Clones/pulls each repository
- Scans for SKILL.md files
- Updates `skills/manifest.json` with new/updated skills
- Deduplicates by SHA hash
- Tracks `first_seen` and `updated` timestamps

## Verification (`scripts/verify_skills.py`)

- Validates YAML frontmatter
- Scans for dangerous patterns (curl to raw IP, eval injection, base64 encoded scripts)
- Checks file size limits
- Removes invalid skills automatically

## Site Generation (`scripts/generate_site.py`)

- Reads manifest.json + skills from disk
- Parses YAML frontmatter and content snippets
- Builds timeline from git log
- Generates `site/data/skills.json`

### Key data structures:

```python
stats = {
    "total_skills": int,
    "total_sources": int,
    "total_files": int,
    "avg_read_time": float,
    "by_source": {"source_name": count},
    "source_repos": {"source_name": "owner/repo"},
    "source_branches": {"source_name": "branch"},
    "source_descriptions": {"source_name": "English / 中文"},
    "generated_at": "ISO timestamp",
}
```

### source_descriptions format:
- All descriptions MUST use `"English text / 中文文本"` format (space-slash-space separator)
- The frontend splits on ` / ` to extract the right language
- Descriptions should be concise (under 100 chars per language)

## Config (`config.yaml`)

- `sources`: list of `{repo, branch}` objects
- `github.token`: for API calls (empty = token from env)
- `verification.max_file_size`: 10MB default
- `pipeline.max_skills_per_run`: 500 default

## Adding a New Source

1. Add repo to `config.yaml` under `sources`
2. Add bilingual description to `generate_site.py`'s `source_descriptions` dict
3. Update `README.md` source table
4. Run `python scripts/generate_site.py` to verify
5. Update site dashboard if any data format changes
