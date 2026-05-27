<div align="center">

# 🏆 TOP-SKILLS

**全球最大的 Claude Code 技能库 · 发现、收集、管理 AI 编码助手的最佳实践**

[![GitHub Pages](https://img.shields.io/github/deployments/bg-szy/TOP-SKILLS/github-pages?label=site&logo=github&style=flat-square)](https://bg-szy.github.io/TOP-SKILLS/)
[![Skills](https://img.shields.io/badge/skills-3900+-blue?style=flat-square)](#)
[![Sources](https://img.shields.io/badge/sources-12-orange?style=flat-square)](#)
[![Last Updated](https://img.shields.io/github/last-commit/bg-szy/TOP-SKILLS?style=flat-square&label=updated)](#)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#)

[📊 在线看板](https://bg-szy.github.io/TOP-SKILLS/) · [📖 技能列表](#-技能列表) · [🚀 快速开始](#-快速开始) · [🏗️ 架构](#️-架构)

[**English → README.md**](README.md)

</div>

---

## 📌 项目简介

**TOP-SKILLS** 是一个持续集成的 [Claude Code](https://claude.ai) 技能（Skills）聚合仓库，自动从 GitHub 上的多个优质开源仓库收集、验证并发布 Claude Code 的自定义指令技能。

> Claude Code Skills 是预定义的提示指令文件（SKILL.md），用于指导 Claude 在特定编码任务中的行为模式——从代码审查、重构、测试生成到架构设计，覆盖软件开发生命周期的各个环节。

### 核心能力

| 特性 | 说明 |
|------|------|
| **大规模** | 已收录 **3900+** 来自 12+ 个优质来源的技能 |
| **持续更新** | 每日自动同步最新技能，确保前沿性 |
| **质量保障** | 自动验证机制，剔除重复、危险和不达标的技能 |
| **可视化** | 在线 Dashboard 提供统计、搜索与趋势分析 |
| **零成本部署** | 纯静态站点 + GitHub Pages 托管，无需服务器 |

---

## 🌐 在线看板

**https://bg-szy.github.io/TOP-SKILLS/**

- **统计概览** — 技能总数、来源分布、文件数、阅读时长
- **技能浏览** — 按来源/关键字搜索、排序、分页浏览所有技能
- **趋势分析** — 日增技能走势、各来源增长曲线、活跃度排名

---

## 📦 技能列表

### 收录来源

| 来源 | 仓库 | 描述 |
|------|------|------|
| `marketplace` | [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace) | 最大的 Claude Code 技能市场 |
| `claude-skills` | [OneWave-AI/claude-skills](https://github.com/OneWave-AI/claude-skills) | 精选 Claude 技能集合 |
| `skills` | [trailofbits/skills](https://github.com/trailofbits/skills) | Trail of Bits 安全工具链技能 |
| `claude-code-toolkit` | [robertguss/claude-code-toolkit](https://github.com/robertguss/claude-code-toolkit) | Claude Code 工具包 |
| `Claude-meta-skill` | [YYH211/Claude-meta-skill](https://github.com/YYH211/Claude-meta-skill) | 元技能定义与组合 |
| `awesome-llm-skills` | [Prat011/awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) | LLM 技能聚合 |
| `awesome-skills` | [FridrichMethod/awesome-skills](https://github.com/FridrichMethod/awesome-skills) | 1,800+ 自动同步技能（含科学计算/生物信息） |
| `claude-code-skills` | [julianobarbosa/claude-code-skills](https://github.com/julianobarbosa/claude-code-skills) | Python/DevOps/云基础设施技能 |
| `agent-skills` | [PracticalSwan/agent-skills](https://github.com/PracticalSwan/agent-skills) | 跨客户端技能（Claude Code/Codex/Copilot） |
| `superskills` | [ariadoss/superskills](https://github.com/ariadoss/superskills) | TDD/调试/安全/规约技能包 |
| `Claude-AI-skills-collection-2026` | [obviousworks/Claude-AI-skills-collection-2026](https://github.com/obviousworks/Claude-AI-skills-collection-2026) | 社区精选全品类技能集合 |
| `awesome-claude-skills` | [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | 50+ 已验证技能（TDD/Git/文档） |
| `self` | [bg-szy/TOP-SKILLS](https://github.com/bg-szy/TOP-SKILLS) | 项目自身开发工作流技能 |

### 技能覆盖领域

| 领域 | 说明 |
|------|------|
| **代码审查与质量** | 代码审查、linting、类型检查、最佳实践建议 |
| **重构与优化** | 代码重构、性能优化、减少技术债务 |
| **测试生成** | 单元测试、集成测试、端到端测试自动生成 |
| **文档编写** | API 文档、内联注释、README 生成 |
| **架构设计** | 系统设计、架构评审、技术方案建议 |
| **安全分析** | 漏洞扫描、安全审计、合规检查（Trail of Bits） |
| **前端开发** | React/Vue/Next.js 组件、样式系统、响应式设计 |
| **后端开发** | API 设计、数据库优化、中间件、微服务 |
| **DevOps** | CI/CD 管道、Docker/K8s 配置、基础设施即代码 |
| **移动开发** | iOS/Android 应用开发、跨平台框架 |

---

## 🚀 快速开始

### 使用技能

每个技能以 `SKILL.md` 文件形式提供，可直接作为 Claude Code 的自定义指令使用：

```bash
# 直接使用远程技能文件
claude -p "请根据 skills/marketplace/skill-name/SKILL.md 的指令帮我审查代码"

# 或克隆到本地使用
git clone https://github.com/bg-szy/TOP-SKILLS.git
claude --skill ./skills/marketplace/skill-name/SKILL.md
```

### 浏览技能

```bash
git clone https://github.com/bg-szy/TOP-SKILLS.git
cd TOP-SKILLS

# 启动本地看板（需要 Python 3）
python -m http.server 8080 -d site/
# 浏览器访问 http://localhost:8080
```

### 运行管道

```bash
# 完整管道：收集 → 验证 → 生成站点 → 提交
python scripts/generate_site.py

# 带翻译功能（可选，需要 deep_translator 库）
python scripts/generate_site.py --translate
```

---

## 🏗️ 架构

```
                    ┌──────────────────┐
                    │  GitHub 上游仓库  │
                    │ (12+ 个来源)      │
                    └────────┬─────────┘
                             │ git clone / fetch
                    ┌────────▼─────────┐
                    │  collect_skills   │  ← 每日收集新技能
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  verify_skills    │  ← 静态分析与安全检查
                    │  (auto-remove)   │  ← 自动剔除不合格技能
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

### 核心技术栈

- **数据层**: Python + YAML + JSON
- **可视化**: Vanilla JS + Chart.js + 暗色主题 CSS
- **CI/CD**: GitHub Actions（自动构建与部署）
- **存储**: 纯文本文件存储
- **托管**: GitHub Pages（免费静态站点）

### 质量保障机制

```
✅ 语法检查    →  确保 SKILL.md 格式正确
✅ 安全检查    →  检测危险命令/模式并自动移除
✅ 大小检查    →  文件过大直接拒绝
✅ 防重复      →  SHA 去重避免重复收录
✅ 持续验证    →  每次提交前自动验证
```

---

## 📊 数据统计

| 指标 | 数值 |
|------|------|
| 技能总数 | 3,900+ |
| 来源数 | 12 |
| 总文件数 | 9,000+ |
| 最快来源 | marketplace（3,620 技能） |
| 首次记录 | 2026-05-22 |
| 自动更新 | 每日同步 |

---

## 🔧 自定义与扩展

### 添加新来源

修改 `skills/manifest.json` 的 `sources` 字段：

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

### 贡献技能

欢迎提交 Issue 或 PR 推荐新的 Claude Code 技能来源。

---

## 📄 许可证

本项目采用 **MIT License** 开源。

> 注意：各技能文件（`skills/**/SKILL.md`）的版权归属其原始作者/仓库，使用时请遵守各自的开源许可。

---

<div align="center">

**TOP-SKILLS** — 让每个开发者都能找到最适合的 Claude Code 技能

[⭐ Star](https://github.com/bg-szy/TOP-SKILLS) · [🐛 报告问题](https://github.com/bg-szy/TOP-SKILLS/issues) · [📬 联系作者](mailto:bg-szy@users.noreply.github.com)

</div>
