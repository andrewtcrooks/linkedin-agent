# TOOLS.md - Local Setup Notes

## Web Search

- **Default: SearXNG** at `http://192.168.1.3:8888`
- Script: `/home/claw/.openclaw/workspace/bin/search "query" [num_results]`
- Never use `web_search` or brave unless SearXNG fails.
- Use `agent-browser` only for page interaction/scraping, not search.

## Web Browsing

- Default: **agent-browser** skill for page interaction, scraping, screenshots, forms.
- Try `web_fetch` first when a lighter tool can answer.
- Operating discipline: `docs/browser-operating-protocol-v1.md`

## Marketing

- Brand voice: Practical, direct, helpful (no hype)
- Platforms: LinkedIn, X/Twitter, Website blog — 3x/week
- Audience: Small businesses (5–50 employees) with manual ops workflows
- Offer: "Fix one workflow in 7 days" — CTA: 15-min triage call
- Verticals: Local services, agencies, clinics, retail

## Model Policy

- Default/background/batch work: **gpt-5.4**
- Heavier models only when explicitly justified (deep strategy, difficult synthesis)
- Coding agent: **Codex only** — Claude Code references in older notes are stale

## Tool / Plugin Intake

- OpenClaw first-class tools first. CLI over daemons.
- Before adding anything new: does OpenClaw already have it? Can a script solve it? What's the auth scope?
- Avoid server daemons unless clearly worth the complexity.

## GitHub Authentication

**Always use GitHub App credentials** for all GitHub operations.

- Credentials: `~/.openclaw/.env` (APP_ID, INSTALLATION_ID, KEY_PATH)
- Token: `/home/claw/.openclaw/workspace/bin/gh-app-token`
- Git credential helper: `/home/claw/.openclaw/workspace/bin/git-credential-gh-app`
- For `gh` CLI: `TOKEN=$(/home/claw/.openclaw/workspace/bin/gh-app-token) && echo "$TOKEN" | gh auth login --with-token`
- All remotes use HTTPS. No SSH keys.

## System Maintenance

- **NEVER** clear `~/.cache/qmd/` — contains vector index and GGUF models
- QMD: index at `~/.cache/qmd/index.sqlite`, models at `~/.cache/qmd/models/`

## Mem0 Auto-Capture (Always On)

**Before every response:** search mem0 for context:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-search.js "USER_QUERY" --limit=3
```

**After substantive exchanges:** store conversation:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-add.js --messages='[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]'
```

**Explicit "remember this":** store as direct fact:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-add.js "fact"
```

Rules: search first, respond second. Store preferences/patterns/corrections. Don't store secrets, API keys, or things already in MEMORY.md. Fail silently — never block a response.

## ClawHub CLI

- Binary: `/home/claw/.npm-global/bin/clawhub` (always use full path)
- `clawhub skills list` — list installed skills
- `clawhub search <term>` — search marketplace

## Exec Approval Policy

Always use absolute paths — never `bash -lc 'export PATH=...'`.

Pre-approved (no approval needed):
- `/home/claw/.openclaw/workspace/bin/search`
- `/home/claw/.npm-global/bin/clawhub`
- `/home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-search.js`
- `/home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-add.js`
- `/home/claw/.bun/bin/qmd
- /home/claw/.openclaw/workspace/bin/mem-router`

## Coding Task Routing

**Default flow for coding tasks:**
`main` → `local-default` (Qwen, triage + jCodeMunch search + brief) → `coding` (Codex, execute packet)

Codex should almost never be first-reader. Qwen reads first, Codex acts on the compressed output.

**Escalate to Codex only when:**
- More than 2 files must be edited
- Bug spans multiple modules
- Output must be PR-quality patch
- Test creation tied to subtle implementation details

**Keep local (Qwen handles):**
- Symbol/file lookup ("where is X?")
- Log/stack trace summarization
- Diff explanation
- Single-file simple edits
- Planning and drafting

**Task packet format** (Qwen → Codex):
```
task: <one-line>
goal: <done criteria>
relevant_files: [paths]
relevant_symbols: [names]
problem: <2-4 sentences>
evidence: [key snippets, max ~50 lines total]
constraints: [must-not-break]
tests_to_update: [files]
non_goals: [do not touch]
```

**Note:** Qwen (local-default) uses jCodeMunch for all repo lookup — never reads whole files.
