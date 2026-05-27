<div align="center">

# 🏆 TOP-SKILLS

**全球最大的 Claude Code 技能库 · 发现、收集、管理 AI 编码助手的最佳实践**  
**The World's Largest Claude Code Skill Repository · Discover, Collect & Manage AI Coding Skills**

[![GitHub Pages](https://img.shields.io/github/deployments/bg-szy/TOP-SKILLS/github-pages?label=site&logo=github&style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Skills](https://img.shields.io/badge/skills-3905+-blue?style=flat-square)](#)
[![Sources](https://img.shields.io/badge/sources-12-orange?style=flat-square)](#)
[![Last Updated](https://img.shields.io/github/last-commit/bg-szy/TOP-SKILLS?style=flat-square&label=updated)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#)

[📊 在线看板 · Dashboard](https://bg-szy.github.io/TOP-SKILLS/) · [📖 技能列表 · Skill List](#-技能列表) · [🚀 快速开始 · Quick Start](#-快速开始) · [🏗️ 架构 · Architecture](#️-架构)

</div>

---

## 📌 项目简介 · About

**TOP-SKILLS** 是一个持续集成的 [Claude Code](https://claude.ai) 技能（Skills）聚合仓库，自动从 GitHub 上的多个优质开源仓库收集、验证并发布 Claude Code 的自定义指令技能。

**TOP-SKILLS** is a continuously integrated Claude Code skill aggregation repository that automatically collects, verifies, and publishes custom instruction skills from multiple high-quality open-source repositories on GitHub.

> Claude Code Skills 是预定义的提示指令文件（SKILL.md），用于指导 Claude 在特定编码任务中的行为模式——从代码审查、重构、测试生成到架构设计，覆盖软件开发生命周期的各个环节。  
> *Claude Code Skills are predefined prompt instruction files (SKILL.md) that guide Claude's behavior in specific coding tasks — from code review, refactoring, and test generation to architecture design, covering the entire software development lifecycle.*

### 核心能力 · Core Capabilities

| 特性 Feature | 说明 Description (中文) | Description (English) |
|------|--------|--------|
| **大规模 Scale** | 已收录 **3900+** 来自 12+ 个优质来源的技能 | **3900+** skills collected from 12+ curated sources |
| **持续更新 Updates** | 每日自动同步最新技能，确保前沿性 | Daily auto-sync to stay up-to-date |
| **质量保障 Quality** | 自动验证机制，剔除重复、危险和不达标的技能 | Auto-verification removes duplicates, dangerous, and low-quality skills |
| **可视化 Dashboard** | 在线 Dashboard 提供统计、搜索与趋势分析 | Online Dashboard with stats, search, and trend analysis |
| **零成本部署 Cost** | 纯静态站点 + GitHub Pages 托管，无需服务器 | Pure static site + GitHub Pages, zero server cost |

---

## 🌐 在线看板 · Dashboard

[查看在线看板 · Visit Dashboard](https://bg-szy.github.io/TOP-SKILLS/)

- **统计概览 / Overview** — 技能总数、来源分布、文件数、阅读时长 / Total skills, source distribution, file count, reading time
- **技能浏览 / Browse** — 按来源/关键字搜索、排序、分页浏览所有技能 / Search, sort, and paginate through all skills
- **趋势分析 / Trends** — 日增技能走势、各来源增长曲线、活跃度排名 / Daily growth, per-source trends, activity ranking

---

## 📦 技能列表 · Skill Collection

### 收录来源 · Sources

| 来源 Source | 仓库 Repository | Description |
|------|------|--------|
| `marketplace` | [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace) | 最大的 Claude Code 技能市场 / Largest skill marketplace |
| `claude-skills` | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | 精选 Claude 技能集合 / Curated skill collection |
| `skills` | [trailofbits/skills](https://github.com/trailofbits/skills) | 安全工具链技能 / Security toolchain skills |
| `claude-code-toolkit` | [robertguss/claude-code-toolkit](https://github.com/robertguss/claude-code-toolkit) | 工具包与实用工具 / Toolkit and utilities |
| `Claude-meta-skill` | [YYH211/Claude-meta-skill](https://github.com/YYH211/Claude-meta-skill) | 元技能定义与组合 / Meta-skill definitions |
| `awesome-llm-skills` | [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) | LLM 技能聚合 / LLM skills aggregation |
| `awesome-skills` | [FridrichMethod/awesome-skills](https://github.com/FridrichMethod/awesome-skills) | 1,800+ 自动同步技能（含科学计算/生物信息） / Auto-synced skills incl. scientific computing |
| `claude-code-skills` | [julianobarbosa/claude-code-skills](https://github.com/julianobarbosa/claude-code-skills) | Python/DevOps/云基础设施 / Python/DevOps/Cloud |
| `agent-skills` | [PracticalSwan/agent-skills](https://github.com/PracticalSwan/agent-skills) | 跨客户端技能（Claude Code/Codex/Copilot） / Cross-client skills |
| `superskills` | [ariadoss/superskills](https://github.com/ariadoss/superskills) | TDD/调试/安全/规约技能包 / TDD/Debug/Security/Spec skill pack |
| `Claude-AI-skills-collection-2026` | [obviousworks/Claude-AI-skills-collection-2026](https://github.com/obviousworks/Claude-AI-skills-collection-2026) | 社区精选全品类技能集合 / Community curated full-category collection |
| `awesome-claude-skills` | [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 50+ 已验证技能（TDD/Git/文档） / 50+ verified skills |

### 技能覆盖领域 · Skill Domains

| 领域 Domain | 说明 Description |
|------------|--------|
| **代码审查与质量 Code Review** | 代码审查、linting、类型检查、最佳实践 / Code review, linting, type checking, best practices |
| **重构与优化 Refactoring** | 代码重构、性能优化、减少技术债务 / Refactoring, performance optimization, debt reduction |
| **测试生成 Test Generation** | 单元测试、集成测试、E2E 测试自动生成 / Unit, integration, and E2E test generation |
| **文档编写 Documentation** | API 文档、内联注释、README 生成 / API docs, inline comments, README generation |
| **架构设计 Architecture** | 系统设计、架构评审、技术方案 / System design, architecture review, technical planning |
| **安全分析 Security** | 漏洞扫描、安全审计、合规检查 / Vulnerability scanning, security audit, compliance |
| **前端开发 Frontend** | React/Vue/Next.js 组件、样式系统 / Components, styling systems, responsive design |
| **后端开发 Backend** | API 设计、数据库优化、中间件、微服务 / API design, DB optimization, middleware, microservices |
| **DevOps** | CI/CD 管道、Docker/K8s 配置、IaC / CI/CD pipelines, Docker/K8s, infrastructure as code |
| **移动开发 Mobile** | iOS/Android 应用开发、跨平台框架 / iOS/Android development, cross-platform frameworks |

---

## 🚀 快速开始 · Quick Start

### 使用技能 · Using Skills

每个技能以 `SKILL.md` 文件形式提供，可直接作为 Claude Code 的自定义指令使用。  
*Each skill is provided as a `SKILL.md` file that can be used directly as a Claude Code custom instruction.*

```bash
# 直接使用远程技能文件 / Use remote skill file directly
claude -p "请根据 skills/marketplace/skill-name/SKILL.md 的指令帮我审查代码"

# 或克隆到本地使用 / Or clone locally
git clone https://github.com/bg-szy/TOP-SKILLS.git
claude --skill ./skills/marketplace/skill-name/SKILL.md
```

### 浏览技能 · Browsing Skills

```bash
# 克隆项目 / Clone the repo
git clone https://github.com/bg-szy/TOP-SKILLS.git
cd TOP-SKILLS

# 启动本地看板 / Start local dashboard (requires Python 3)
python -m http.server 8080 -d site/
# 浏览器访问 / Open http://localhost:8080
```

### 运行管道 · Running the Pipeline

```bash
# 完整管道：收集 → 验证 → 生成站点 → 提交
# Full pipeline: collect → verify → generate site → commit
python scripts/generate_site.py

# 带翻译功能（可选，需要 deep_translator 库）
# With translation (optional, requires deep_translator)
python scripts/generate_site.py --translate
```

---

## 🏗️ 架构 · Architecture

```
                    ┌──────────────────┐
                    │  GitHub 上游仓库  │
                    │ (12+ 个来源)     │
                    └────────┬─────────┘
                             │ git clone / fetch
                    ┌────────▼─────────┐
                    │  collect_skills   │  ← 每日收集新技能 / Daily collection
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  verify_skills    │  ← 静态分析与安全检查 / Static analysis & security check
                    │  (auto-remove)   │  ← 自动剔除不合格技能 / Auto-remove invalid skills
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  generate_site    │  → site/data/skills.json
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  GitHub Actions   │  → gh-pages 分支
                    │  (自动部署)       │  → GitHub Pages
                    └──────────────────┘
```

### 核心技术栈 · Tech Stack

- **数据层 Data**: Python + YAML + JSON
- **可视化 Visualization**: Vanilla JS + Chart.js + 暗色主题 CSS / Dark theme CSS
- **CI/CD**: GitHub Actions（自动构建与部署 / Auto build & deploy）
- **存储 Storage**: 纯文本文件存储 / Plain text storage
- **托管 Hosting**: GitHub Pages（免费静态站点 / Free static site）

### 质量保障机制 · Quality Assurance

```
✅ 语法检查 Syntax Check    →  确保 SKILL.md 格式正确 / Validate SKILL.md format
✅ 安全检查 Security Check  →  检测危险命令/模式并自动移除 / Detect and remove dangerous patterns
✅ 大小检查 Size Check      →  文件过大直接拒绝 / Reject oversized files
✅ 防重复 Deduplication    →  SHA 去重避免重复收录 / SHA deduplication
✅ 持续验证 Validation      →  每次提交前自动验证 / Auto-validate before each commit
```

---

## 📊 数据统计 · Statistics

| 指标 Metric | 数值 Value |
|------|------|
| 技能总数 / Total Skills | 3,905+ |
| 来源数 / Sources | 12 |
| 总文件数 / Total Files | 9,009 |
| 最快来源 / Fastest Source | marketplace（3,620 技能 / skills） |
| 首次记录 / First Recorded | 2026-05-22 |
| 自动更新 / Auto Update | 每日同步 / Daily sync |

---

## 🔧 自定义与扩展 · Customization

### 添加新来源 · Adding New Sources

修改 `skills/manifest.json` 的 `sources` 字段 / Edit the `sources` field in `skills/manifest.json`:

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

### 贡献技能 · Contributing

欢迎提交 Issue 或 PR 推荐新的 Claude Code 技能来源。  
*Feel free to open an Issue or PR to recommend new Claude Code skill sources.*

---

## 📄 许可证 · License

本项目采用 **MIT License** 开源。  
*This project is open-sourced under the **MIT License**.*

> 注意：各技能文件（`skills/**/SKILL.md`）的版权归属其原始作者/仓库，使用时请遵守各自的开源许可。  
> *Note: Each skill file (`skills/**/SKILL.md`) is copyright its original author/repository. Please comply with their respective open-source licenses when using them.*

---

<div align="center">

**TOP-SKILLS** — 让每个开发者都能找到最适合的 Claude Code 技能  
*Helping every developer find the perfect Claude Code skill*

[⭐ Star](https://github.com/bg-szy/TOP-SKILLS) · [🐛 报告问题 / Report Issue](https://github.com/bg-szy/TOP-SKILLS/issues) · [📬 联系作者 / Contact](mailto:bg-szy@users.noreply.github.com)

</div>
