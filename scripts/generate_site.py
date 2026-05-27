#!/usr/bin/env python
"""
Generate static site data for the TOP-SKILLS web dashboard.
Reads manifest.json, SKILL.md files, and git history;
outputs site/data/skills.json for the frontend SPA.
"""

import os
import re
import sys
import json
import yaml
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = PROJECT_ROOT / "skills" / "manifest.json"
SKILLS_DIR = PROJECT_ROOT / "skills"
OUTPUT_DIR = PROJECT_ROOT / "site" / "data"
OUTPUT_FILE = OUTPUT_DIR / "skills.json"
LOGS_DIR = PROJECT_ROOT / "logs"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Translation (optional)
# ---------------------------------------------------------------------------
TRANSLATION_CACHE_PATH = PROJECT_ROOT / "site" / "data" / "translation_cache.json"


def load_translation_cache() -> dict:
    if TRANSLATION_CACHE_PATH.exists():
        try:
            with open(TRANSLATION_CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_translation_cache(cache: dict):
    TRANSLATION_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRANSLATION_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def translate_text(text: str, cache: dict, enable: bool) -> str:
    """Translate English text to Chinese with caching. Falls back to original on failure."""
    if not enable or not text or len(text) < 20:
        return text
    key = text[:200]
    if key in cache:
        return cache[key]
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="en", target="zh-CN").translate(text[:5000])
        if translated and translated != text:
            cache[key] = translated
            return translated
    except Exception as e:
        log.warning("Translation failed for '%s...': %s", text[:30], e)
    return text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    content = content.replace("\r\n", "\n").strip()
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        end = content.find("---", 3)
        if end == -1 or end > 2000:
            return {}
        yb = content[3:end].strip()
    else:
        yb = content[3:end].strip()
    try:
        return yaml.safe_load(yb) or {}
    except yaml.YAMLError:
        return {}


def get_git_timeline(skill_sources: set) -> tuple:
    """
    Parse git log to build overall and per-source timelines.
    Returns (overall_timeline, per_source_timeline, source_activity).
    - overall_timeline: list of {date, added, total}
    - per_source_timeline: {source: [{date, added, total}, ...]}
    - source_activity: {source: {first_seen, last_seen, commits, added}}
    """
    try:
        result = subprocess.run(
            ["git", "log", "--reverse", "--format=%H %ci", "--name-only"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
    except Exception as e:
        log.warning("Could not read git log: %s", e)
        return [], {}, {}

    seen_global = set()
    seen_per_source = {}  # source -> set of paths
    timeline = []
    per_source = {}  # source -> [{date, added, total}]
    source_activity = {}  # source -> {first_seen, last_seen, commits, added}

    current_date = None
    global_added = 0
    source_added = {}  # source -> count for current commit

    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue

        # Commit header
        if re.match(r"^[0-9a-f]{40} \d{4}-\d{2}-\d{2}", line):
            # Save previous commit data
            if current_date and global_added > 0:
                timeline.append({"date": current_date, "added": global_added})
                for src, cnt in source_added.items():
                    if cnt > 0:
                        if src not in per_source:
                            per_source[src] = []
                            source_activity[src] = {"first_seen": current_date, "last_seen": current_date, "commits": 0, "added": 0}
                        per_source[src].append({"date": current_date, "added": cnt})
                        source_activity[src]["last_seen"] = current_date
                        source_activity[src]["commits"] += 1
                        source_activity[src]["added"] += cnt

            parts = line.split()
            current_date = parts[1] if len(parts) > 1 else None
            global_added = 0
            source_added = {}
            continue

        # Track skills/ directories (deduplicate by skill dir, not individual files)
        if line.startswith("skills/") and '/' in line:
            path_parts = line.split("/")
            if len(path_parts) >= 3:
                # Extract skill directory: skills/{source}/{skill_name}
                skill_dir = f"{path_parts[0]}/{path_parts[1]}/{path_parts[2]}"
                src = path_parts[1]

                if skill_dir not in seen_global:
                    seen_global.add(skill_dir)
                    global_added += 1

                    if src not in seen_per_source:
                        seen_per_source[src] = set()
                    if skill_dir not in seen_per_source[src]:
                        seen_per_source[src].add(skill_dir)
                        if src not in source_added:
                            source_added[src] = 0
                        source_added[src] += 1

    # Last commit
    if current_date and global_added > 0:
        timeline.append({"date": current_date, "added": global_added})
        for src, cnt in source_added.items():
            if cnt > 0:
                if src not in per_source:
                    per_source[src] = []
                per_source[src].append({"date": current_date, "added": cnt})
                if src in source_activity:
                    source_activity[src]["last_seen"] = current_date
                    source_activity[src]["commits"] += 1
                    source_activity[src]["added"] += cnt

    # Accumulate totals for overall
    running = 0
    for entry in timeline:
        running += entry["added"]
        entry["total"] = running

    # Accumulate totals for per-source
    for src in per_source:
        running = 0
        for entry in per_source[src]:
            running += entry["added"]
            entry["total"] = running

    # Fill in missing sources (from disk but not in git timeline)
    for src in skill_sources:
        if src not in per_source:
            per_source[src] = []

    return timeline, per_source, source_activity


def get_content_snippet(content: str, max_len: int = 500) -> str:
    """Extract first meaningful text snippet from markdown content (skip frontmatter)."""
    text = content.replace("\r\n", "\n")
    # Strip frontmatter
    text = re.sub(r"^---[\s\S]*?---\n*", "", text).strip()
    # Strip markdown headers
    text = re.sub(r"^#+\s+", "", text)
    # Strip empty lines at start
    text = text.lstrip("\n")
    # Truncate to first meaningful paragraph
    lines = text.split("\n")
    snippet = ""
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            snippet += line + " "
            if len(snippet) >= max_len:
                break
    return snippet[:max_len].strip()


def read_skill_content(skill_dir: Path) -> dict:
    """Read SKILL.md and return frontmatter + content snippet + file list."""
    result = {
        "frontmatter": {},
        "content_snippet": "",
        "file_list": [],
    }
    sk_path = skill_dir / "SKILL.md"
    if not sk_path.exists():
        return result

    try:
        raw = sk_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return result

    result["frontmatter"] = parse_frontmatter(raw)
    result["content_snippet"] = get_content_snippet(raw)

    # List files
    for f in sorted(skill_dir.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            rel = str(f.relative_to(skill_dir))
            result["file_list"].append({
                "name": rel,
                "size": f.stat().st_size,
            })

    return result


def generate_chinese_summary(frontmatter: dict, skill_name: str, description: str, read_time: int, n_files: int, translated_desc: str = None) -> str:
    """Generate a Chinese-language structured summary from skill metadata."""
    lines = []

    name = frontmatter.get("name", skill_name)
    lines.append(f"## 技能名称\n{name}")
    lines.append("")

    # Use translated description if available, otherwise original
    cn_desc = translated_desc or description or frontmatter.get("description", "")
    if cn_desc:
        lines.append(f"## 描述\n{cn_desc}")
        lines.append("")

    # Type / classification
    skill_type = frontmatter.get("type", frontmatter.get("tag", ""))
    if skill_type:
        lines.append(f"**类型**: {skill_type}")
        lines.append("")

    # Author
    author = frontmatter.get("author", "")
    if author:
        lines.append(f"**作者**: {author}")
        lines.append("")

    # Version info
    version = frontmatter.get("version", "")
    status = frontmatter.get("status", "")
    if version:
        lines.append(f"**版本**: {version}")
    if status:
        lines.append(f"**状态**: {'已发布' if status == 'published' else '未发布' if status == 'unpublished' else status}")
    if version or status:
        lines.append("")

    # Expertise / capabilities
    for field in ["expertise", "capabilities", "skills", "features"]:
        vals = frontmatter.get(field, [])
        if isinstance(vals, list) and vals:
            labels = {"expertise": "专长领域", "capabilities": "能力", "skills": "技能", "features": "功能特点"}
            lines.append(f"## {labels[field]}")
            for v in vals:
                lines.append(f"- {v}")
            lines.append("")
            break  # use first found

    # Requirements / prerequisites
    for field in ["requirements", "prerequisites", "dependencies"]:
        vals = frontmatter.get(field, [])
        if isinstance(vals, list) and vals:
            labels = {"requirements": "前置要求", "prerequisites": "前置条件", "dependencies": "依赖"}
            lines.append(f"## {labels[field]}")
            for v in vals:
                lines.append(f"- {v}")
            lines.append("")
            break

    # Use cases from description — extract key scenarios
    if cn_desc and len(cn_desc) > 20:
        lines.append("## 适用场景")
        lines.append("根据技能描述，此技能适用于以下场景：")
        # Split description into bullet points
        sentences = [s.strip() for s in cn_desc.replace("\n", " ").split(". ") if s.strip()]
        for s in sentences[:5]:
            if s and len(s) > 10:
                lines.append(f"- {s}.")
        lines.append("")

    # Stats
    lines.append(f"**文件数**: {n_files}  |  **预计阅读时间**: {read_time} 分钟")
    lines.append("")

    # Updated date
    updated = frontmatter.get("updated", "")
    if updated:
        lines.append(f"**最后更新**: {updated}")

    return "\n".join(lines).strip()


def get_skill_readme_length(skill_dir: Path) -> int:
    """Get the approximate reading time of SKILL.md in minutes."""
    sk_path = skill_dir / "SKILL.md"
    if not sk_path.exists():
        return 0
    try:
        text = sk_path.read_text(encoding="utf-8", errors="replace")
        # Strip frontmatter
        text = re.sub(r"^---[\s\S]*?---\n*", "", text)
        word_count = len(text.split())
        return max(1, word_count // 200)  # ~200 words per minute
    except Exception:
        return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate site data for TOP-SKILLS dashboard")
    parser.add_argument("--translate", action="store_true", help="Translate English descriptions to Chinese")
    args = parser.parse_args()

    log.info("Generating site data...")

    # Load translation cache if --translate
    trans_cache = load_translation_cache() if args.translate else {}
    if args.translate:
        log.info("Translation enabled, cache has %d entries", len(trans_cache))

    # Step 1: Load manifest
    if not MANIFEST_PATH.exists():
        log.error("manifest.json not found at %s", MANIFEST_PATH)
        sys.exit(1)

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_skills = manifest.get("skills", {})
    log.info("Manifest has %d skills", len(manifest_skills))

    # Step 2: Walk skills directory — Phase 1: read metadata
    skills_data = []
    source_counter = Counter()
    total_files = 0
    readme_lengths = []
    pending_translate = []  # (index, text) for descriptions needing translation

    for source_dir in sorted(SKILLS_DIR.iterdir()):
        if not source_dir.is_dir() or source_dir.name.startswith("."):
            continue
        if source_dir.name == "node_modules":
            continue

        for skill_dir in sorted(source_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue

            sk_path = skill_dir / "SKILL.md"
            if not sk_path.exists():
                continue

            key = f"{source_dir.name}/{skill_dir.name}"
            meta = manifest_skills.get(key, {})

            content = read_skill_content(skill_dir)
            read_time = get_skill_readme_length(skill_dir)

            n_files = len(content["file_list"]) or meta.get("files", 1)
            total_files += n_files
            source_counter[source_dir.name] += 1
            readme_lengths.append(read_time)

            fm = content["frontmatter"]
            desc = fm.get("description", meta.get("description", ""))

            skills_data.append({
                "key": key,
                "name": skill_dir.name,
                "source": source_dir.name,
                "source_repo": meta.get("source", ""),
                "repo_dir": meta.get("dir_path", skill_dir.name),
                "title": fm.get("name", skill_dir.name),
                "description": desc,
                "files": n_files,
                "file_list": content["file_list"],
                "read_time": read_time,
                "first_seen": meta.get("first_seen", ""),
                "updated": meta.get("updated", ""),
                "content_snippet": content["content_snippet"],
                "frontmatter": fm,
            })

            # Collect descriptions needing translation
            if args.translate and desc and len(desc) >= 20:
                key_cache = desc[:200]
                if key_cache not in trans_cache:
                    pending_translate.append((len(skills_data) - 1, desc))

    log.info("Found %d skills on disk", len(skills_data))

    # Step 2b: Translate descriptions in parallel (if --translate)
    if args.translate and pending_translate:
        log.info("Translating %d descriptions with 8 threads...", len(pending_translate))
        translated_count = 0
        with ThreadPoolExecutor(max_workers=8) as executor:
            fut_map = {}
            for idx, desc in pending_translate:
                fut = executor.submit(translate_text, desc, trans_cache, True)
                fut_map[fut] = (idx, desc)

            for fut in as_completed(fut_map):
                idx, desc = fut_map[fut]
                try:
                    result = fut.result()
                    skills_data[idx]["_trans_desc"] = result
                    translated_count += 1
                    if translated_count % 100 == 0:
                        log.info("  Translated %d/%d...", translated_count, len(pending_translate))
                except Exception as e:
                    log.warning("Translation failed for skill %d: %s", idx, e)

        log.info("Translation complete: %d/%d translated", translated_count, len(pending_translate))
        save_translation_cache(trans_cache)
        log.info("Translation cache saved (%d entries)", len(trans_cache))

    # Step 2c: Generate cn_summaries for all skills
    for s in skills_data:
        trans_desc = s.pop("_trans_desc", None) if args.translate else None
        s["cn_summary"] = generate_chinese_summary(
            s["frontmatter"], s["name"], s["description"],
            s["read_time"], s["files"], translated_desc=trans_desc,
        )

    # Step 3: Get timeline from git
    timeline, per_source_timeline, source_activity = get_git_timeline(set(source_counter.keys()))
    log.info("Timeline has %d data points, %d sources tracked",
             len(timeline), len(per_source_timeline))
    by_source = dict(source_counter.most_common())
    avg_read_time = round(sum(readme_lengths) / len(readme_lengths), 1) if readme_lengths else 0

    # Source repo mapping
    source_repos = {}
    source_branches = {}
    source_descriptions = {}
    for s in manifest.get("sources", {}).values():
        repo = s.get("repo", "")
        prefix = repo.split("/")[-1] if repo else ""
        source_repos[prefix] = repo
        source_branches[prefix] = s.get("branch", "main")

    # Human-readable descriptions for each source
    source_descriptions = {
        "marketplace": "Largest Claude Code skill marketplace / 最大的 Claude Code 技能市场",
        "skills": "Trail of Bits security toolchain skills / 安全工具链技能",
        "claude-code-toolkit": "Claude Code toolkit and utilities / 工具包与实用工具",
        "Claude-meta-skill": "Meta-skill definitions and composition / 元技能定义与组合",
        "claude-skills": "Curated Claude skills collection / 精选 Claude 技能集合",
        "awesome-llm-skills": "LLM skills aggregation / LLM 技能聚合",
        "awesome-skills": "1,800+ auto-synced skills (scientific/bioinformatics) / 自动同步科学计算技能",
        "claude-code-skills": "Python/DevOps/cloud infrastructure skills / Python/DevOps/云基础设施",
        "agent-skills": "Cross-client skills (Claude Code/Codex/Copilot) / 跨客户端技能",
        "superskills": "TDD/debugging/security/spec skill pack / TDD/调试/安全技能包",
        "Claude-AI-skills-collection-2026": "Community curated full-category skill collection / 社区精选全品类技能集合",
        "awesome-claude-skills": "50+ verified skills (TDD/Git/docs) / 50+ 已验证技能",
        "self": "TOP-SKILLS project self-skills for development workflow / 项目自身开发工作流技能",
    }

    stats = {
        "total_skills": len(skills_data),
        "total_sources": len(source_counter),
        "total_files": total_files,
        "avg_read_time": avg_read_time,
        "by_source": by_source,
        "source_repos": source_repos,
        "source_branches": source_branches,
        "source_descriptions": source_descriptions,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    # Step 5: Write output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "timeline": timeline,
        "per_source_timeline": per_source_timeline,
        "source_activity": source_activity,
        "skills": skills_data,
    }

    # Convert non-serializable objects (e.g. date from YAML) to strings
    def json_default(o):
        if hasattr(o, 'isoformat'):
            return o.isoformat()
        return str(o)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=json_default)

    file_size = OUTPUT_FILE.stat().st_size
    log.info("Written to %s (%.1f MB)", OUTPUT_FILE, file_size / 1024 / 1024)
    log.info("Stats: %d skills, %d sources, %d files, %d timeline entries",
             stats["total_skills"], stats["total_sources"], stats["total_files"], len(timeline))

    # Output summary for pipeline
    summary = {
        "skills": len(skills_data),
        "sources": len(source_counter),
        "files": total_files,
    }
    print("\n---SUMMARY---")
    print(json.dumps(summary))
    print("---SUMMARY_END---")

    return 0


if __name__ == "__main__":
    sys.exit(main())
