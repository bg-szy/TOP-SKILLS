# TOP-SKILLS Site Development Guide

You are helping maintain the TOP-SKILLS web dashboard — a single-page application for browsing and analyzing Claude Code skills.

## Key Files

| File | Purpose |
|------|---------|
| `site/index.html` | Complete SPA: all CSS inline, all JS inline |
| `site/data/skills.json` | Generated data (10 MB, gitignored) |
| `scripts/generate_site.py` | Generates skills.json from manifest + disk |

## Architecture

- **Single page**: All HTML, CSS, JS in one file (`site/index.html`)
- **Dark theme**: CSS variables in `:root` for theming
- **Chart.js**: Loaded from CDN, wrapped in try-catch
- **Data flow**: `skills.json` → `fetch` → `DATA` global → render functions

## i18n System

The dashboard supports Chinese/English real-time switching:

```javascript
const I18N = {
  keyName: ['中文文本', 'English Text'],
};
let currentLang = 'zh';  // 'zh' or 'en'
function t(key) { return I18N[key][currentLang === 'zh' ? 0 : 1]; }
function switchLang() { currentLang = currentLang === 'zh' ? 'en' : 'zh'; applyLang(); }
function applyLang() { /* update static DOM + re-render dynamic content */ }
```

### i18n Rules:
1. All UI strings MUST be in `I18N` object as `[zh, en]` pairs
2. Use `t('keyName')` in JS, never hardcode display text
3. Bilingual descriptions use format: `"English text / 中文文本"` with ` / ` separator
4. Use `getBilingualDesc(desc, lang)` helper to extract the right language part
5. Chart re-creation MUST be in try-catch blocks

## Chart.js Usage

- Charts are tracked in `window._charts` object
- Always call `destroyChart('name')` before creating a new chart
- Always wrap `new Chart(...)` in try-catch
- The `applyLang()` function destroys and recreates all charts

## CSS Conventions

- Use `:root` CSS variables for colors (var(--bg), var(--accent), etc.)
- Component classes: stat-card, chart-box, skill-card, source-table, etc.
- Responsive breakpoint at 768px
- Use flexbox and CSS grid for layout

## Verification

After any site change, run:
```bash
python scripts/generate_site.py
python -m http.server 8080 -d site/
```
Then open http://localhost:8080 and verify:
1. Dashboard loads with correct stats
2. Tab switching works
3. Search and filter in Browse tab
4. Skill detail modal opens/closes
5. Language toggle switches all text
6. All charts render
