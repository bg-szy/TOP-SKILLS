#!/usr/bin/env python3
"""
Static analysis / security verification for collected Claude Code skills.
Checks: valid frontmatter, dangerous patterns, file size limits, binary files.
"""

import os
import re
import sys
import json
import yaml
import logging
import argparse
import mimetypes
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple, Optional

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
SKILLS_DIR = PROJECT_ROOT / "skills"
LOGS_DIR = PROJECT_ROOT / "logs"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOGS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Verification checks
# ---------------------------------------------------------------------------

class VerificationResult:
    """Collects verification results."""

    def __init__(self):
        self.passed = 0
        self.warnings = 0
        self.errors = 0
        self.details: List[dict] = []

    def add_pass(self, skill: str, check: str, message: str = ""):
        self.passed += 1
        self.details.append({"skill": skill, "check": check, "status": "pass", "message": message})

    def add_warning(self, skill: str, check: str, message: str):
        self.warnings += 1
        self.details.append({"skill": skill, "check": check, "status": "warning", "message": message})

    def add_error(self, skill: str, check: str, message: str):
        self.errors += 1
        self.details.append({"skill": skill, "check": check, "status": "error", "message": message})

    @property
    def is_pass(self) -> bool:
        return self.errors == 0

    def summary(self) -> dict:
        return {
            "passed": self.passed,
            "warnings": self.warnings,
            "errors": self.errors,
            "overall": "PASS" if self.is_pass else "FAIL",
        }


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_all_skills(base_dir: Path) -> List[Tuple[str, Path]]:
    """Walk skills directory and return list of (skill_name, skill_path)."""
    skills = []
    if not base_dir.exists():
        return skills
    for source_dir in base_dir.iterdir():
        if not source_dir.is_dir() or source_dir.name.startswith("."):
            continue
        for skill_dir in source_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith("."):
                continue
            sk_path = skill_dir / "SKILL.md"
            if sk_path.is_file():
                skills.append((f"{source_dir.name}/{skill_dir.name}", skill_dir))
    return skills


def parse_frontmatter(content: str) -> Optional[dict]:
    content = content.strip()
    if not content.startswith("---"):
        return None
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return None
    yaml_block = content[3:end_idx].strip()
    if not yaml_block:
        return None
    try:
        return yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        return None


# --- Individual checks ---

def check_frontmatter(skill_name: str, sk_path: Path, result: VerificationResult):
    """Validate SKILL.md has proper frontmatter with required fields."""
    try:
        content = sk_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result.add_error(skill_name, "frontmatter_readable", f"Cannot read SKILL.md: {e}")
        return content  # type: ignore

    fm = parse_frontmatter(content)
    if fm is None:
        result.add_error(skill_name, "frontmatter_exists", "No valid YAML frontmatter found (must start with ---)")
        return None
    if not isinstance(fm, dict):
        result.add_error(skill_name, "frontmatter_type", "Frontmatter is not a dictionary")
        return None

    # Required fields
    required = ["name", "description"]
    missing = [f for f in required if f not in fm or not fm[f]]
    if missing:
        result.add_error(skill_name, "frontmatter_fields",
                         f"Missing required frontmatter fields: {missing}")
    else:
        result.add_pass(skill_name, "frontmatter_fields", "Required fields present")

    # Name format
    name = fm.get("name", "")
    if not re.match(r'^[a-z0-9][a-z0-9_-]*[a-z0-9]$', str(name)) and name:
        result.add_warning(skill_name, "frontmatter_name_format",
                           f"Skill name '{name}' not in kebab-case convention")

    return fm


def check_dangerous_patterns(skill_name: str, skill_dir: Path, config: dict, result: VerificationResult):
    """Scan all files for dangerous patterns."""
    blocked = config.get("verification", {}).get("blocked_patterns", [])

    if not blocked:
        return

    compiled = []
    for pattern in blocked:
        try:
            compiled.append(re.compile(pattern))
        except re.error as e:
            log.warning("Invalid regex pattern '%s': %s", pattern, e)

    for file_path in skill_dir.rglob("*"):
        if not file_path.is_file():
            continue
        # Skip binary files
        if is_binary_file(file_path):
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        rel_path = str(file_path.relative_to(skill_dir))
        for i, regex in enumerate(compiled):
            match = regex.search(content)
            if match:
                matched_text = match.group()[:80]
                result.add_error(
                    skill_name, "dangerous_pattern",
                    f"Matched blocked pattern [{i}] in {rel_path}: '{matched_text}'"
                )
                return  # One error per skill is enough to flag it


def check_file_sizes(skill_name: str, skill_dir: Path, config: dict, result: VerificationResult):
    """Check that no file exceeds max size."""
    max_size = config.get("verification", {}).get("max_file_size", 10 * 1024 * 1024)
    max_skill = config.get("verification", {}).get("max_skill_size", 100 * 1024 * 1024)

    total_size = 0
    for file_path in skill_dir.rglob("*"):
        if not file_path.is_file():
            continue
        size = file_path.stat().st_size
        total_size += size
        if size > max_size:
            result.add_error(skill_name, "file_size",
                             f"File {file_path.name} exceeds {max_size} bytes ({size})")

    if total_size > max_skill:
        result.add_error(skill_name, "skill_size",
                         f"Total skill size {total_size} exceeds {max_skill} bytes")

    # File count check
    file_count = sum(1 for _ in skill_dir.rglob("*") if _.is_file())
    if file_count > 500:
        result.add_warning(skill_name, "file_count",
                           f"Skill has {file_count} files (may be too large)")


def is_binary_file(path: Path) -> bool:
    """Check if a file is binary by looking at first bytes."""
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except Exception:
        return True


def check_binary_files(skill_name: str, skill_dir: Path, config: dict, result: VerificationResult):
    """Warn about unexpected binary files."""
    allowed_exts = config.get("verification", {}).get("allowed_extensions", [])
    if not allowed_exts:
        return

    for file_path in skill_dir.rglob("*"):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        if ext in allowed_exts:
            continue

        # For unknown extensions, check if binary
        if is_binary_file(file_path):
            # Allow images, fonts, etc. by extension
            image_exts = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot"}
            if ext not in image_exts:
                result.add_warning(skill_name, "binary_file",
                                   f"Unexpected binary file: {file_path.name} (ext: {ext})")


def check_skill_structure(skill_name: str, skill_dir: Path, result: VerificationResult):
    """Verify skill directory structure is reasonable."""
    sk_path = skill_dir / "SKILL.md"
    if not sk_path.is_file():
        result.add_error(skill_name, "structure", "Missing SKILL.md")
        return

    # Check for required directories that should exist with content
    has_refs = (skill_dir / "references").is_dir()
    has_scripts = (skill_dir / "scripts").is_dir()

    # Check for empty directories
    for sub in skill_dir.iterdir():
        if sub.is_dir() and not any(sub.iterdir()):
            result.add_warning(skill_name, "empty_dir",
                               f"Empty directory: {sub.name}")

    result.add_pass(skill_name, "structure", "Basic structure OK")


def check_path_traversal(skill_name: str, skill_dir: Path, result: VerificationResult):
    """Check for path traversal attempts in skill files."""
    patterns = [
        r'\.\./',           # Unix path traversal
        r'\.\.\\\\',         # Windows path traversal
        r'~/\.ssh',          # SSH key access
        r'~/\.aws',          # AWS credential access
        r'/etc/passwd',      # System file access
        r'/etc/shadow',
        r'/var/log',
    ]
    compiled = [re.compile(p) for p in patterns]

    for file_path in skill_dir.rglob("*.md"):
        if not file_path.is_file():
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            rel_path = str(file_path.relative_to(skill_dir))
            for regex in compiled:
                if regex.search(content):
                    result.add_warning(skill_name, "path_traversal",
                                       f"Suspicious path pattern in {rel_path}: '{regex.pattern}'")
        except Exception:
            continue


def check_sensitive_content(skill_name: str, skill_dir: Path, result: VerificationResult):
    """Check for hardcoded secrets or sensitive data."""
    patterns = [
        (r'(?i)api[_-]?key\s*[:=]\s*["\']?(sk-[a-zA-Z0-9]{20,})', "API key pattern"),
        (r'(?i)token\s*[:=]\s*["\']?([a-zA-Z0-9_-]{20,})', "Token pattern"),
        (r'(?i)password\s*[:=]\s*["\']([^"\']{3,})["\']', "Password pattern"),
        (r'(?i)ghp_[a-zA-Z0-9]{36}', "GitHub token"),
        (r'(?i)gho_[a-zA-Z0-9]{36}', "GitHub OAuth token"),
    ]
    compiled = [(re.compile(p), label) for p, label in patterns]

    for file_path in skill_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if is_binary_file(file_path):
            continue
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            rel_path = str(file_path.relative_to(skill_dir))
            for regex, label in compiled:
                if regex.search(content):
                    result.add_warning(skill_name, "sensitive_data",
                                       f"Potential {label} in {rel_path}")
        except Exception:
            continue


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def remove_failed_skills(failed: List[str], manifest_path: Path) -> List[str]:
    """Delete failed skill directories and remove from manifest. Returns list of removed keys."""
    removed = []
    for skill_key in failed:
        parts = skill_key.split("/", 1)
        if len(parts) != 2:
            continue
        src, name = parts
        skill_dir = SKILLS_DIR / src / name
        if skill_dir.exists():
            import shutil
            shutil.rmtree(skill_dir, ignore_errors=True)
            log.info("  Deleted: %s", skill_dir)
        removed.append(skill_key)

    # Remove from manifest
    if manifest_path.exists():
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            for key in removed:
                manifest.get("skills", {}).pop(key, None)
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            log.info("  Removed %d entries from manifest", len(removed))
        except Exception as e:
            log.warning("Could not update manifest: %s", e)

    return removed


def main():
    parser = argparse.ArgumentParser(description="Verify collected Claude Code skills")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    parser.add_argument("--skill", help="Verify only a specific skill")
    parser.add_argument("--auto-remove", action="store_true", help="Auto-delete skills that fail verification")
    args = parser.parse_args()

    config = load_config()
    skills = get_all_skills(SKILLS_DIR)

    log.info("=== TOP-SKILLS Verification Pipeline ===")
    log.info("Skills to verify: %d", len(skills))

    if not skills:
        log.warning("No skills found in %s", SKILLS_DIR)
        summary = {"passed": 0, "warnings": 0, "errors": 0, "overall": "PASS (empty)", "total": 0}
        print("\n---SUMMARY---")
        print(json.dumps(summary))
        print("---SUMMARY_END---")
        return 0

    result = VerificationResult()

    for skill_name, skill_dir in skills:
        if args.skill and args.skill not in skill_name:
            continue

        sk_path = skill_dir / "SKILL.md"

        # Check 1: Frontmatter
        fm = check_frontmatter(skill_name, sk_path, result)

        # Check 2: Skill structure
        check_skill_structure(skill_name, skill_dir, result)

        # Check 3: Dangerous patterns (skip if frontmatter is completely broken)
        if fm is not None:
            check_dangerous_patterns(skill_name, skill_dir, config, result)

        # Check 4: File sizes
        check_file_sizes(skill_name, skill_dir, config, result)

        # Check 5: Binary files
        check_binary_files(skill_name, skill_dir, config, result)

        # Check 6: Path traversal
        check_path_traversal(skill_name, skill_dir, result)

        # Check 7: Sensitive content
        check_sensitive_content(skill_name, skill_dir, result)

    # Final evaluation
    if args.strict:
        final_pass = result.errors == 0 and result.warnings == 0
    else:
        final_pass = result.errors == 0

    overall = "PASS" if final_pass else "FAIL"
    result_summary = result.summary()
    result_summary["overall"] = overall
    result_summary["total"] = len(skills)

    log.info("=== Verification Results ===")
    log.info("PASSED:   %d", result.passed)
    log.info("WARNINGS: %d", result.warnings)
    log.info("ERRORS:   %d", result.errors)
    log.info("OVERALL:  %s", overall)

    if result.errors > 0:
        log.info("--- Failed checks ---")
        for d in result.details:
            if d["status"] == "error":
                log.info("  [%s] %s: %s", d["skill"], d["check"], d["message"])

    # Output JSON summary
    print("\n---SUMMARY---")
    print(json.dumps(result_summary))
    print("---SUMMARY_END---")

    # Auto-remove failed skills (after summary output, so pipeline sees original result)
    if args.auto_remove and result.errors > 0:
        failed_keys = set()
        for d in result.details:
            if d["status"] == "error":
                failed_keys.add(d["skill"])
        if failed_keys:
            log.info("--- Auto-removing %d failed skills ---", len(failed_keys))
            manifest_path = SKILLS_DIR / "manifest.json"
            removed = remove_failed_skills(list(failed_keys), manifest_path)
            log.info("Removed: %s", removed)
            remaining = sum(1 for _ in SKILLS_DIR.rglob("SKILL.md"))
            if remaining == 0:
                log.warning("No skills remaining after auto-remove!")
            else:
                log.info("%d skills remaining after cleanup", remaining)
            # Auto-remove handled the failures — signal pipeline to proceed
            return 0

    return 0 if final_pass else 1


if __name__ == "__main__":
    sys.exit(main())
