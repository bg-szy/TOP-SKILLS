# TOP-SKILLS Development Workflow

This skill defines the development workflow: changes must be verified, recorded, and committed atomically.

## Workflow Steps

Every functional change follows this sequence:

```
1. Implement → 2. Verify → 3. Record → 4. Commit
```

### Step 1: Implement
Make changes to the relevant files. Follow the project conventions.

### Step 2: Verify
Run verification to confirm changes are correct:
```bash
# For data pipeline changes:
python scripts/generate_site.py

# For site changes:
python -m http.server 8080 -d site/ &
# Check: http://localhost:8080

# For config changes:
python -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

Verification checks:
- Site generates without errors
- Statistics look reasonable
- All links work
- Language toggle functions
- Charts render
- No console errors

### Step 3: Record
Update CHANGELOG.md with the change. Use this format:

#### For new features:
```markdown
### 新增
- **Feature Name** — Brief description of what was added
```

#### For bug fixes:
```markdown
### 修复
- **Bug Name** — What was broken and how it was fixed
```

#### For config/refactoring changes:
```markdown
### 变更
- **Change Name** — What changed and why
```

Group under the current date heading (`## YYYY-MM-DD`). If the date heading doesn't exist, create it. If it does, append to the appropriate category.

### Step 4: Commit
Create a structured commit:
```bash
git add <specific files>
git commit -m "<type>: <short description>

- Detail what changed (bullet points if needed)"
```

Commit types:
- `feat`: new feature
- `fix`: bug fix  
- `chore`: config, tooling, refactoring
- `docs`: documentation
- `i18n`: language/translation changes

## Auto-Record Rule

After verifying a functional change:
1. Update CHANGELOG.md immediately (before commit)
2. Stage both the change and the CHANGELOG update together
3. Commit with a message referencing the CHANGELOG entry

This ensures every functional change is atomically paired with its record.

## Git Rules

- **Do NOT** push to master directly without verification
- **Do NOT** use `--no-verify` or `--no-gpg-sign`
- **Do NOT** amend published commits
- **Do NOT** commit secrets or credentials
- Prefer specific file paths in `git add`, not `git add .`
