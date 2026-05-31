<div align="center">

# 🏆 TOP-SKILLS

**The World's Largest Claude Code Skills Directory**  

Discover · Collect · Manage — 3,900+ AI coding skills from the community

[![Site](https://img.shields.io/github/deployments/bg-szy/TOP-SKILLS/github-pages?label=Dashboard&logo=github&style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Skills](https://img.shields.io/badge/Skills-3900+-blue?style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Sources](https://img.shields.io/badge/Sources-13-orange?style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Last Commit](https://img.shields.io/github/last-commit/bg-szy/TOP-SKILLS?style=flat-square&label=Updated)](https://github.com/bg-szy/TOP-SKILLS/commits/master)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/bg-szy/TOP-SKILLS?style=flat-square&logo=github)](https://github.com/bg-szy/TOP-SKILLS/stargazers)

[**📊 Dashboard**](https://bg-szy.github.io/TOP-SKILLS/) · [**📖 Browse Skills**](#-skill-collection) · [**🚀 Quick Start**](#-quick-start) · [**🏗️ Architecture**](#️-architecture) · [**🤝 Contribute**](#-contributing)

[**🇨🇳 中文版 → README.zh.md**](README.zh.md)

</div>

---

## 📌 Why TOP-SKILLS?

Claude Code custom instructions (`SKILL.md` files) unlock Claude's full potential — from code review and refactoring to test generation and architecture design. **TOP-SKILLS** aggregates them all in one place:

| Why Us | Benefit |
|--------|---------|
| **🌐 Single Source** | 3,900+ skills from 13 curated repositories, unified |
| **🔄 Daily Sync** | Auto-collected every day — always up to date |
| **✅ Quality Guard** | Auto-verification: security checks, dedup, format validation |
| **🔍 Smart Dashboard** | Search, filter, sort, charts, trends — all in one page |
| **💰 Zero Cost** | Pure static site on GitHub Pages, no server needed |

---

## 🌐 Live Dashboard

**→ [https://bg-szy.github.io/TOP-SKILLS/](https://bg-szy.github.io/TOP-SKILLS/)**

| Feature | Description |
|---------|-------------|
| **📊 Overview** | Total skills, source distribution, files count, reading time |
| **🔎 Browse** | Search, sort, filter by source, grid/list view, pagination |
| **📈 Trends** | Daily growth, per-source trends, activity ranking |
| **🏆 Hot Repos** | Most active source repositories ranked |
| **🌍 Bilingual** | Chinese/English UI toggle, skill content with Chinese summaries |

---

## 📦 Skill Collection

### Sources

TOP-SKILLS aggregates from these high-quality repositories:

| Prefix | Repository | Description |
|--------|-----------|-------------|
| `marketplace` | [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace) | Largest Claude Code skill marketplace |
| `awesome-skills` | [FridrichMethod/awesome-skills](https://github.com/FridrichMethod/awesome-skills) | 1,800+ auto-synced skills incl. scientific computing |
| `claude-skills` | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | Curated Claude skill collection |
| `Claude-AI-skills-collection-2026` | [obviousworks/Claude-AI-skills-collection-2026](https://github.com/obviousworks/Claude-AI-skills-collection-2026) | Community curated full-category collection |
| `skills` | [trailofbits/skills](https://github.com/trailofbits/skills) | Security toolchain skills by Trail of Bits |
| `claude-code-toolkit` | [robertguss/claude-code-toolkit](https://github.com/robertguss/claude-code-toolkit) | Toolkit and utilities |
| `claude-code-skills` | [julianobarbosa/claude-code-skills](https://github.com/julianobarbosa/claude-code-skills) | Python/DevOps/Cloud skills |
| `agent-skills` | [PracticalSwan/agent-skills](https://github.com/PracticalSwan/agent-skills) | Cross-client skills (Claude Code/Codex/Copilot) |
| `awesome-llm-skills` | [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) | LLM skills aggregation |
| `superskills` | [ariadoss/superskills](https://github.com/ariadoss/superskills) | TDD/Debug/Security/Spec skill pack |
| `Claude-meta-skill` | [YYH211/Claude-meta-skill](https://github.com/YYH211/Claude-meta-skill) | Meta-skill definitions |
| `awesome-claude-skills` | [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 50+ verified skills (TDD/Git/docs) |
| `self` | [bg-szy/TOP-SKILLS](https://github.com/bg-szy/TOP-SKILLS) | This project's own development skills |

### Skill Domains

| Domain | Skills Cover |
|--------|-------------|
| **Code Review** | Linting, type checking, best practices, security audit |
| **Refactoring** | Performance optimization, tech debt reduction, API migration |
| **Test Generation** | Unit, integration, E2E, property-based testing |
| **Documentation** | API docs, inline comments, README generation, changelogs |
| **Architecture** | System design, architecture review, technical planning |
| **Security** | Vulnerability scanning, OWASP, compliance, threat modeling |
| **Frontend** | React/Vue/Next.js, styling, responsive design, a11y |
| **Backend** | API design, DB optimization, middleware, microservices |
| **DevOps** | CI/CD, Docker/K8s, IaC, monitoring |
| **Mobile** | iOS/Android, cross-platform, mobile testing |
| **AI/ML** | Prompt engineering, model evaluation, data pipeline |
| **CLI & Tools** | Shell scripting, git workflow, productivity automation |

---

## 🚀 Quick Start

```bash
# 1. Browse skills online
open https://bg-szy.github.io/TOP-SKILLS/

# 2. Use a skill directly with Claude Code
claude -p "Please review my code using the instructions in https://github.com/bg-szy/TOP-SKILLS/blob/master/skills/marketplace/skill-name/SKILL.md"

# 3. Clone and browse locally
git clone https://github.com/bg-szy/TOP-SKILLS.git
cd TOP-SKILLS
python -m http.server 8080 -d site/
# Open http://localhost:8080

# 4. Use a local skill file
claude --skill ./skills/marketplace/skill-name/SKILL.md
```

---

## 🏗️ Architecture

```
                    ┌──────────────────┐
                    │  GitHub Upstream │
                    │ (13+ sources)    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  collect_skills   │  ← Daily collection pipeline
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  verify_skills    │  ← Security & quality check
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  generate_site    │  → site/data/skills.json
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  GitHub Actions   │  → gh-pages → GitHub Pages
                    └──────────────────┘
```

### Tech Stack

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![YAML](https://img.shields.io/badge/Config-YAML-orange)
![Vanilla JS](https://img.shields.io/badge/UI-Vanilla_JS-yellow)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-ff6384)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?logo=githubactions)

### Quality Assurance

```
✅ YAML Frontmatter Validation  →  Well-formed SKILL.md
✅ Dangerous Pattern Detection  →  No curl|bash to raw IPs
✅ File Size Limits             →  Max 10 MB per file
✅ SHA-based Deduplication      →  No duplicate content
✅ Auto-remediation             →  Invalid skills auto-removed
```

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Total Skills | 3,900+ |
| Source Repositories | 13 |
| Total Files | 9,000+ |
| Fastest Growing Source | aiskillstore/marketplace (3,620+ skills) |
| First Recorded | 2026-05-22 |
| Update Frequency | Daily at 08:00 Beijing Time |

---

## 🤝 Contributing

**⭐ Star this repo** — It helps others discover the project!

**📢 Share** — Know someone using Claude Code? Share [TOP-SKILLS](https://github.com/bg-szy/TOP-SKILLS) with them.

**🔗 Recommend a source** — [Open an Issue](https://github.com/bg-szy/TOP-SKILLS/issues/new) or PR to add new skill repositories:

```yaml
# Add to config.yaml
sources:
  - repo: your-name/your-skills
    branch: main
```

**🏷️ Tag your own repo** — If you maintain a Claude Code skill repository, add the `claude-code-skill` topic on GitHub so our search can find it.

---

## 📄 License

This project is **MIT Licensed**.

> **Note:** Each skill file (`skills/**/SKILL.md`) retains its original author's copyright. Please comply with their respective licenses when using them.

---

<div align="center">

**⭐ If you find this useful, please star the repo! It really helps. ⭐**

[![GitHub stars](https://img.shields.io/github/stars/bg-szy/TOP-SKILLS?style=social)](https://github.com/bg-szy/TOP-SKILLS/stargazers)

[**📊 Dashboard**](https://bg-szy.github.io/TOP-SKILLS/) · [**🐛 Report Issue**](https://github.com/bg-szy/TOP-SKILLS/issues) · [**⭐ Star**](https://github.com/bg-szy/TOP-SKILLS)

</div>
