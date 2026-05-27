# Changelog

## 2026-05-27

### 新增
- **中英文切换** — 站点右上角新增语言切换按钮，支持中文/英文实时切换
- **仓库描述列** — 概览页和趋势页的表格新增"仓库描述"列，中英双语
- **7 个新技能来源** — 新增 FridrichMethod/awesome-skills、julianobarbosa/claude-code-skills、PracticalSwan/agent-skills、ariadoss/superskills、obviousworks/Claude-AI-skills-collection-2026、karanb192/awesome-claude-skills、Prat011/awesome-llm-skills
- **README 优化** — 完整项目描述、徽章、架构图、技能覆盖领域、数据统计表
- **Add project self-skills** — Add skills/self/ directory with site-dev, data-pipeline, review, and workflow skills; add verify-and-record automation script

### 修复
- **来源占比错误** — git log 统计按文件路径计数导致 marketplace 显示 222%（实际应为 92.7%），改为按技能目录去重
- **CI 构建失败** — scripts/ 不在 git 追踪中导致 generate_site.py 找不到，调整 .gitignore 仅暴露必要文件
- **CI 部署失败** — git clean -fdx 删除 site/ 导致部署步骤 cp 失败，改为先备份再部署
- **Actions 版本兼容** — 移除 FORCE_JAVASCRIPT_ACTIONS_TO_NODE24 标志，改用 python3 确保兼容性
- **Git 历史清理** — 误提交的 6 个脚本文件通过 filter-branch 从历史中彻底移除
- **GIT_TOKEN 权限** — 添加 permissions: contents: write 解决 push 403

### 变更
- `.gitignore` 收紧：仅暴露 `scripts/generate_site.py`，其余脚本保持本地
- 所有管道脚本（collect/verify/pipeline）从 git 追踪中移除
