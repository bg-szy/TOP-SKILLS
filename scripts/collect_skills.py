#!/usr/bin/env python
"""
Collect Claude Code skills from GitHub repositories using GitHub API.
Efficiently downloads only skill-related files without full git clone.
"""

import os
import re
import sys
import yaml
import json
import hashlib
import shutil
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Tuple

try:
    import requests
except ImportError:
    print("ERROR: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
SKILLS_OUTPUT = PROJECT_ROOT / "skills"
LOGS_DIR = PROJECT_ROOT / "logs"
MANIFEST_PATH = SKILLS_OUTPUT / "manifest.json"

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
# GitHub API Client
# ---------------------------------------------------------------------------

class GitHubClient:
    """Lightweight GitHub API client."""

    def __init__(self, token: str = ""):
        self.token = token or os.environ.get("GITHUB_TOKEN", "")
        self.base = "https://api.github.com"
        self.raw_base = "https://raw.githubusercontent.com"
        self.session = requests.Session()
        self.session.trust_env = False  # Bypass system proxy for GitHub
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "TOP-SKILLS-Collector/1.0",
        })
        if self.token:
            self.session.headers["Authorization"] = f"token {self.token}"

    def _request(self, url: str, params: dict = None, retries: int = 3) -> Optional[dict]:
        """Make API request with retry logic."""
        timeout = 120 if "git/trees" in url else 30  # Tree fetch needs longer timeout
        for attempt in range(retries):
            try:
                resp = self.session.get(url, params=params, timeout=timeout)
                if resp.status_code == 403 and "rate limit" in resp.text.lower():
                    wait = 60
                    log.warning("Rate limited. Waiting %ds...", wait)
                    time.sleep(wait)
                    continue
                if resp.status_code == 404:
                    return None
                if resp.status_code != 200:
                    log.warning("API error %d: %s", resp.status_code, resp.text[:150])
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return None
                return resp.json()
            except requests.RequestException as e:
                log.warning("Request failed (attempt %d/%d): %s", attempt + 1, retries, e)
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return None
        return None

    def get_repo_tree(self, repo: str, branch: str = "main") -> Optional[List[dict]]:
        """Get full file tree of a repository."""
        url = f"{self.base}/repos/{repo}/git/trees/{branch}?recursive=1"
        data = self._request(url)
        if data and "tree" in data:
            return data["tree"]
        # Fallback: maybe default branch is different
        repo_data = self._request(f"{self.base}/repos/{repo}")
        if repo_data:
            default_branch = repo_data.get("default_branch", branch)
            if default_branch != branch:
                url = f"{self.base}/repos/{repo}/git/trees/{default_branch}?recursive=1"
                data = self._request(url)
                if data and "tree" in data:
                    return data["tree"]
        return None

    def download_file(self, repo: str, file_path: str, branch: str = "main") -> Optional[bytes]:
        """Download a raw file from GitHub."""
        url = f"{self.raw_base}/{repo}/{branch}/{file_path}"
        try:
            resp = self.session.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.content
            log.debug("Failed to download %s: HTTP %d", url, resp.status_code)
            return None
        except requests.RequestException as e:
            log.debug("Failed to download %s: %s", url, e)
            return None

    def search_repos(self, query: str, per_page: int = 10) -> List[dict]:
        """Search GitHub repositories."""
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": per_page}
        data = self._request(f"{self.base}/search/repositories", params)
        if data and "items" in data:
            return data["items"]
        return []

    def check_repo_exists(self, repo: str) -> bool:
        """Check if a repository exists."""
        data = self._request(f"{self.base}/repos/{repo}")
        return data is not None


# ---------------------------------------------------------------------------
# Skill Detection
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML frontmatter from markdown content."""
    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not content.startswith("---"):
        return None
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        end_idx = content.find("---", 3)
        if end_idx > 1000:  # Safety: frontmatter shouldn't be this long
            return None
        if end_idx == -1:
            return None
        yaml_block = content[3:end_idx].strip()
    else:
        yaml_block = content[3:end_idx].strip()

    if not yaml_block:
        return None
    try:
        return yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        return None


def is_claude_code_skill(frontmatter: dict) -> bool:
    """Check if frontmatter represents a Claude Code skill."""
    if not isinstance(frontmatter, dict):
        return False
    name = frontmatter.get("name")
    if not name or not isinstance(name, str):
        return False
    desc = frontmatter.get("description")
    if not desc or not isinstance(desc, str):
        return False
    # Additional signals: specific Claude Code skill frontmatter fields
    trigger = frontmatter.get("trigger")
    if trigger:
        return True
    # Skills often have these
    for key in frontmatter:
        if key in ("name", "description", "trigger", "model", "temperature"):
            continue
        return True  # Has additional custom fields
    return True  # Minimum: name + description


# ---------------------------------------------------------------------------
# Repository Processing
# ---------------------------------------------------------------------------

def process_repo(github: GitHubClient, repo: str, branch: str) -> Tuple[List[dict], List[str]]:
    """
    Fetch repo tree, find all skills, download them.
    Returns (skills_found, errors).
    """
    log.info("Fetching file tree for %s ...", repo)
    tree = github.get_repo_tree(repo, branch)
    if tree is None:
        log.error("Cannot access repository %s. It may not exist or is private.", repo)
        return [], [f"Failed to access {repo}"]

    log.info("  Tree has %d entries", len(tree))

    # Find all SKILL.md files
    skill_entries = []  # List of (skill_name, parent_path, file_entries)
    errors = []

    # Group tree entries by their parent directory
    dir_files: Dict[str, List[dict]] = {}
    for entry in tree:
        path = entry.get("path", "")
        entry_type = entry.get("type", "")

        # Only process blob (files)
        if entry_type == "blob":
            parent = str(Path(path).parent).replace("\\", "/")
            if parent == ".":
                parent = ""
            if parent not in dir_files:
                dir_files[parent] = []
            dir_files[parent].append(entry)

    # Look for directories containing SKILL.md
    skill_count = 0
    seen_skill_names = set()

    for dir_path, files in dir_files.items():
        # Normalize path separators (Windows compat)
        dir_path_norm = dir_path.replace("\\", "/")

        # Check if this directory has a SKILL.md
        target = f"{dir_path}/SKILL.md" if dir_path else "SKILL.md"
        has_skill_md = any(f.get("path") == target for f in files)

        if not has_skill_md:
            continue

        # Get SKILL.md content to validate
        sk_path = f"{dir_path}/SKILL.md" if dir_path else "SKILL.md"
        sk_path = sk_path.replace("\\", "/")
        sk_content = github.download_file(repo, sk_path, branch)
        if sk_content is None:
            log.debug("  Could not download %s", sk_path)
            continue

        try:
            text_content = sk_content.decode("utf-8")
        except UnicodeDecodeError:
            text_content = sk_content.decode("utf-8", errors="replace")

        fm = parse_frontmatter(text_content)
        if not is_claude_code_skill(fm):
            log.debug("  SKILL.md at %s does not appear to be a Claude Code skill (bad frontmatter)", sk_path)
            continue

        # Extract skill name
        skill_name = fm.get("name", "").strip().lower().replace(" ", "-").replace("/", "-")

        # Collect all files in this skill directory (needed for hash computation)
        skill_files = {}
        for f in files:
            rel_path = f.get("path", "")
            size = f.get("size", 0)
            # Make path relative to skill directory
            if dir_path_norm:
                rel_to_skill = rel_path[len(dir_path_norm) + 1:]
            else:
                rel_to_skill = rel_path
            skill_files[rel_to_skill] = {
                "path": rel_path,
                "size": size,
                "sha": f.get("sha", ""),
            }

        # Compute content hash for dedup (same logic as main())
        m = hashlib.md5()
        for k, v in sorted(skill_files.items()):
            m.update(f"{k}:{v['sha']}".encode())
        skill_hash = m.hexdigest()[:12]

        # Handle duplicate names: skip if identical content, rename if different
        if skill_name in seen_skill_names:
            existing_hash = seen_skill_names[skill_name]
            if skill_hash == existing_hash:
                log.warning("  Duplicate skill name '%s' (identical content), skipping", skill_name)
                continue
            else:
                # Different content — disambiguate by appending dir_path suffix
                suffix = dir_path_norm.replace("/", "-") if dir_path_norm else "root"
                skill_name = f"{skill_name}__{suffix}"
                log.info("  Renamed duplicate skill to '%s' (content differs)", skill_name)

        seen_skill_names[skill_name] = skill_hash

        skill_entries.append({
            "name": skill_name,
            "dir_path": dir_path_norm,
            "files": skill_files,
            "frontmatter": fm,
            "has_skill_md": True,
        })
        skill_count += 1

    log.info("  Found %d valid skills", skill_count)
    return skill_entries, errors


def download_skill(github: GitHubClient, repo: str, branch: str,
                   skill: dict, dest_dir: Path) -> List[str]:
    """Download all files for a skill. Returns list of downloaded file paths."""
    downloaded = []
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Download SKILL.md first
    sk_path = f"{skill['dir_path']}/SKILL.md" if skill["dir_path"] else "SKILL.md"
    content = github.download_file(repo, sk_path, branch)
    if content:
        (dest_dir / "SKILL.md").write_bytes(content)
        downloaded.append("SKILL.md")

    # Download other files
    for rel_path, info in skill["files"].items():
        if rel_path == "SKILL.md":
            continue
        # Skip hidden files
        if rel_path.startswith("."):
            continue
        # Skip node_modules
        if "node_modules" in rel_path:
            continue

        remote_path = info["path"]
        file_content = github.download_file(repo, remote_path, branch)
        if file_content:
            file_dest = dest_dir / rel_path
            file_dest.parent.mkdir(parents=True, exist_ok=True)
            file_dest.write_bytes(file_content)
            downloaded.append(rel_path)
        else:
            log.debug("    Failed to download %s", remote_path)

    return downloaded


# ---------------------------------------------------------------------------
# Repository Search
# ---------------------------------------------------------------------------

def search_new_repos(github: GitHubClient, config: dict, existing_sources: set) -> List[dict]:
    """Search GitHub for new repositories containing skills."""
    queries = config.get("github", {}).get("search_queries", [])
    new_sources = []

    for query in queries:
        log.info("  Searching: '%s'", query)
        items = github.search_repos(query, per_page=10)
        for item in items:
            full_name = item.get("full_name", "")
            if full_name and full_name not in existing_sources:
                log.info("  Found new repo: %s (stars: %d)", full_name, item.get("stargazers_count", 0))
                new_sources.append({
                    "repo": full_name,
                    "branch": item.get("default_branch", "main"),
                    "base_path": "",
                })
                existing_sources.add(full_name)
        time.sleep(0.3)  # Rate limiting

    new_sources.sort(key=lambda x: x.get("_stars", 0), reverse=True)
    return new_sources[:10]


# ---------------------------------------------------------------------------
# Config & Manifest
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        log.error("config.yaml not found at %s", CONFIG_PATH)
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"updated_at": "", "sources": {}, "skills": {}}


def save_manifest(manifest: dict):
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Collect Claude Code skills from GitHub")
    parser.add_argument("--no-search", action="store_true", help="Skip GitHub search for new repos")
    parser.add_argument("--sources", nargs="+", help="Specific repos to collect (e.g., anthropics/skills)")
    parser.add_argument("--max-skills", type=int, default=None, help="Maximum skills to collect per run")
    args = parser.parse_args()

    config = load_config()
    if args.max_skills is None:
        args.max_skills = config.get("pipeline", {}).get("max_skills_per_run", 500)
    gh_config = config.get("github", {})
    token = gh_config.get("token", "")
    github = GitHubClient(token)

    sources = list(config.get("sources", []))
    existing_repos = {s["repo"] for s in sources}

    log.info("=== TOP-SKILLS Collection Pipeline ===")
    log.info("Configured sources: %d", len(sources))

    if not token and not args.no_search:
        log.info("No GITHUB_TOKEN set — search is disabled (use --no-search to suppress).")
        log.info("To enable: set GITHUB_TOKEN env var or put token in config.yaml")
        args.no_search = True

    # Search for new repos
    if not args.no_search and token:
        log.info("Searching GitHub for new skill repositories...")
        new_repos = search_new_repos(github, config, existing_repos)
        if new_repos:
            log.info("Found %d new repositories", len(new_repos))
            sources.extend(new_repos)
        else:
            log.info("No new repositories found")

    # Filter to specific sources if requested
    if args.sources:
        sources = [s for s in sources if s["repo"] in args.sources]
        log.info("Filtered to %d specific source(s)", len(sources))

    # Process each source
    manifest = load_manifest()
    skills_collected = {}
    total_new = 0
    total_updated = 0
    total_errors = 0

    # Enforce minimum free disk space
    min_disk_gb = config.get("pipeline", {}).get("min_disk_gb", 5)
    try:
        disk_usage = shutil.disk_usage(SKILLS_OUTPUT)
        free_gb = disk_usage.free / (1024**3)
        log.info("Disk %s: %.1f GB free (threshold: %.1f GB)",
                 SKILLS_OUTPUT.drive or "?", free_gb, min_disk_gb)
        if free_gb < min_disk_gb:
            log.warning("LOW DISK SPACE: %.1f GB free < %.1f GB threshold. Skipping new additions.", free_gb, min_disk_gb)
            update_only = True
        else:
            update_only = False
    except Exception as e:
        log.warning("Could not check disk space: %s. Proceeding without limit.", e)
        update_only = False

    for source in sources:
        repo = source["repo"]
        branch = source.get("branch", "main")
        source_prefix = repo.split("/")[-1]  # e.g., "skills"

        log.info("--- Processing: %s ---", repo)

        # Check repo existence
        if not github.check_repo_exists(repo):
            log.warning("  Repository %s not found, skipping", repo)
            total_errors += 1
            continue

        skills_found, errors = process_repo(github, repo, branch)
        if errors:
            total_errors += len(errors)

        if not skills_found:
            log.info("  No skills found in %s", repo)
            continue

        # Download each skill
        for skill in skills_found:
            if args.max_skills > 0 and len(skills_collected) >= args.max_skills:
                log.warning("Reached max skills limit (%d)", args.max_skills)
                break

            skill_name = skill["name"]
            dest = SKILLS_OUTPUT / source_prefix / skill_name

            # Check if already exists and unchanged (by SHA)
            skill_key = f"{source_prefix}/{skill_name}"
            existing = manifest.get("skills", {}).get(skill_key, {})

            # Skip new skills when at capacity
            if update_only and not existing:
                log.debug("  - %s (skipped new, at capacity)", skill_name)
                continue

            m = hashlib.md5()
            for k, v in sorted(skill["files"].items()):
                m.update(f"{k}:{v['sha']}".encode())
            skill_sha = m.hexdigest()[:12]

            if existing.get("sha") == skill_sha and dest.exists():
                # Still update dir_path if missing
                if not existing.get("dir_path"):
                    existing["dir_path"] = skill["dir_path"]
                log.info("  = %s (unchanged)", skill_name)
                continue

            log.info("  + %s (%d files): %s",
                     skill_name, len(skill["files"]),
                     skill["frontmatter"].get("description", "")[:80])

            downloaded = download_skill(github, repo, branch, skill, dest)
            if downloaded:
                if skill_key not in skills_collected:
                    total_new += 1
                    first_seen = datetime.now(timezone.utc).isoformat()
                else:
                    first_seen = existing.get("first_seen", datetime.now(timezone.utc).isoformat())

                skills_collected[skill_key] = {
                    "name": skill_name,
                    "source": repo,
                    "source_prefix": source_prefix,
                    "dir_path": skill["dir_path"],
                    "files": len(downloaded),
                    "description": skill["frontmatter"].get("description", "")[:200],
                    "sha": skill_sha,
                    "first_seen": first_seen,
                    "updated": datetime.now(timezone.utc).isoformat(),
                }
                total_updated += 1
            else:
                log.warning("  ! %s download failed (0 files)", skill_name)

        log.info("  Done: %d skills from %s", len(skills_found), repo)

    # Update manifest
    source_key = source_prefix if args.sources else "all"
    manifest["sources"] = manifest.get("sources", {})
    for source in sources:
        key = source["repo"].split("/")[-1]
        manifest["sources"][key] = {
            "repo": source["repo"],
            "branch": source.get("branch", "main"),
            "last_collected": datetime.now(timezone.utc).isoformat(),
        }

    manifest_skills = manifest.get("skills", {})
    for key, info in skills_collected.items():
        manifest_skills[key] = info
    manifest["skills"] = manifest_skills
    save_manifest(manifest)

    # Summary
    log.info("=== Summary ===")
    log.info("New: %d | Updated: %d | Errors: %d | Total: %d",
             total_new, total_updated, total_errors, len(manifest["skills"]))

    summary = {
        "new": total_new,
        "updated": total_updated,
        "errors": total_errors,
        "total": len(manifest["skills"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    print("\n---SUMMARY---")
    print(json.dumps(summary))
    print("---SUMMARY_END---")

    return 0 if total_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
