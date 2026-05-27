<div align="center">

# 🏆 TOP-SKILLS

**The World's Largest Claude Code Skill Repository · Discover, Collect & Manage AI Coding Best Practices**

[![GitHub Pages](https://img.shields.io/github/deployments/bg-szy/TOP-SKILLS/github-pages?label=site&logo=github&style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Skills](https://img.shields.io/badge/skills-3900+-blue?style=flat-square)](#)
[![Sources](https://img.shields.io/badge/sources-12-orange?style=flat-square)](#)
[![Last Updated](https://img.shields.io/github/last-commit/bg-szy/TOP-SKILLS?style=flat-square&label=updated)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#)

[📊 Dashboard](https://bg-szy.github.io/TOP-SKILLS/) · [📖 Skills](#-skill-collection) · [🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#️-architecture)

[**中文版 → README.zh.md**](README.zh.md)

</div>

---

## 📌 About

**TOP-SKILLS** is a continuously integrated [Claude Code](https://claude.ai) skill aggregation hub that automatically collects, verifies, and publishes custom instruction skills from high-quality open-source repositories on GitHub.

> *Claude Code Skills are predefined prompt instruction files (SKILL.md) that guide Claude's behavior in specific coding tasks — from code review, refactoring, and test generation to architecture design, covering the entire software development lifecycle.*

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Scale** | **3900+** skills collected from 12+ curated sources |
| **Freshness** | Daily auto-sync to stay up-to-date |
| **Quality** | Auto-verification removes duplicates, dangerous, and low-quality skills |
| **Dashboard** | Online Dashboard with stats, search, and trend analysis |
| **Cost** | Pure static site + GitHub Pages, zero server cost |

---

## 🌐 Dashboard

**https://bg-szy.github.io/TOP-SKILLS/**

- **Overview** — Total skills, source distribution, file count, reading time
- **Browse** — Search, sort, and paginate through all skills
- **Trends** — Daily growth, per-source trends, activity ranking

---

## 📦 Skill Collection

### Sources

| Source | Repository | Description |
|--------|-----------|-------------|
| `marketplace` | [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace) | Largest Claude Code skill marketplace |
| `claude-skills` | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | Curated skill collection |
| `skills` | [trailofbits/skills](https://github.com/trailofbits/skills) | Security toolchain skills |
| `claude-code-toolkit` | [robertguss/claude-code-toolkit](https://github.com/robertguss/claude-code-toolkit) | Toolkit and utilities |
| `Claude-meta-skill` | [YYH211/Claude-meta-skill](https://github.com/YYH211/Claude-meta-skill) | Meta-skill definitions |
| `awesome-llm-skills` | [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) | LLM skills aggregation |
| `awesome-skills` | [FridrichMethod/awesome-skills](https://github.com/FridrichMethod/awesome-skills) | 1,800+ auto-synced skills incl. scientific computing |
| `claude-code-skills` | [julianobarbosa/claude-code-skills](https://github.com/julianobarbosa/claude-code-skills) | Python/DevOps/Cloud skills |
| `agent-skills` | [PracticalSwan/agent-skills](https://github.com/PracticalSwan/agent-skills) | Cross-client skills (Claude Code/Codex/Copilot) |
| `superskills` | [ariadoss/superskills](https://github.com/ariadoss/superskills) | TDD/Debug/Security/Spec skill pack |
| `Claude-AI-skills-collection-2026` | [obviousworks/Claude-AI-skills-collection-2026](https://github.com/obviousworks/Claude-AI-skills-collection-2026) | Community curated full-category collection |
| `awesome-claude-skills` | [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 50+ verified skills (TDD/Git/docs) |
| `self` | [bg-szy/TOP-SKILLS](https://github.com/bg-szy/TOP-SKILLS) | Project's own development workflow skills |

### Skill Domains

| Domain | Description |
|--------|-------------|
| **Code Review** | Code review, linting, type checking, best practices |
| **Refactoring** | Code refactoring, performance optimization, debt reduction |
| **Test Generation** | Unit, integration, and E2E test generation |
| **Documentation** | API docs, inline comments, README generation |
| **Architecture** | System design, architecture review, technical planning |
| **Security** | Vulnerability scanning, security audit, compliance |
| **Frontend** | React/Vue/Next.js components, styling systems, responsive design |
| **Backend** | API design, DB optimization, middleware, microservices |
| **DevOps** | CI/CD pipelines, Docker/K8s, infrastructure as code |
| **Mobile** | iOS/Android development, cross-platform frameworks |

---

## 🚀 Quick Start

### Using Skills

Each skill is provided as a `SKILL.md` file, usable directly as a Claude Code custom instruction:

```bash
# Use remote skill file directly
claude -p "Please review my code following the instructions in skills/marketplace/skill-name/SKILL.md"

# Or clone locally
git clone https://github.com/bg-szy/TOP-SKILLS.git
claude --skill ./skills/marketplace/skill-name/SKILL.md
```

### Browsing Skills Locally

```bash
git clone https://github.com/bg-szy/TOP-SKILLS.git
cd TOP-SKILLS

# Start local dashboard (requires Python 3)
python -m http.server 8080 -d site/
# Open http://localhost:8080
```

### Running the Pipeline

```bash
# Full pipeline: collect → verify → generate site → commit
python scripts/generate_site.py

# With translation (optional, requires deep_translator)
python scripts/generate_site.py --translate
```

---

## 🏗️ Architecture

```
                    ┌──────────────────┐
                    │  GitHub Upstream │
                    │ (12+ sources)    │
                    └────────┬─────────┘
                             │ git clone / fetch
                    ┌────────▼─────────┐
                    │  collect_skills   │  ← Daily collection
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  verify_skills    │  ← Static analysis & security check
                    │  (auto-remove)   │  ← Auto-remove invalid skills
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  generate_site    │  → site/data/skills.json
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  GitHub Actions   │  → gh-pages branch
                    │  (auto deploy)   │  → GitHub Pages
                    └──────────────────┘
```

### Tech Stack

- **Data**: Python + YAML + JSON
- **Visualization**: Vanilla JS + Chart.js + Dark theme CSS
- **CI/CD**: GitHub Actions (auto build & deploy)
- **Storage**: Plain text files
- **Hosting**: GitHub Pages (free static site)

### Quality Assurance

```
✅ Syntax Check    →  Validate SKILL.md format
✅ Security Check  →  Detect and remove dangerous patterns
✅ Size Check      →  Reject oversized files
✅ Deduplication   →  SHA-based dedup
✅ Validation      →  Auto-validate before each commit
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Skills | 3,900+ |
| Sources | 12 |
| Total Files | 9,000+ |
| Fastest Source | marketplace (3,620 skills) |
| First Recorded | 2026-05-22 |
| Auto Update | Daily sync |

---

## 🔧 Customization

### Adding New Sources

Edit the `sources` field in `skills/manifest.json`:

```json
{
  "sources": {
    "my-source": {
      "repo": "username/repo-name",
      "branch": "main"
    }
  }
}
```

### Contributing

Feel free to open an Issue or PR to recommend new Claude Code skill sources.

---

## 📄 License

This project is open-sourced under the **MIT License**.

> *Note: Each skill file (`skills/**/SKILL.md`) is copyright its original author/repository. Please comply with their respective open-source licenses when using them.*

---

<div align="center">

**TOP-SKILLS** — Helping every developer find the perfect Claude Code skill

[⭐ Star](https://github.com/bg-szy/TOP-SKILLS) · [🐛 Report Issue](https://github.com/bg-szy/TOP-SKILLS/issues) · [📬 Contact](mailto:bg-szy@users.noreply.github.com)

</div>
