# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### Web Browsing Policy

- Default web page browsing/automation path: **agent-browser** skill/workflow.
- Prefer agent-browser for opening pages, interacting with sites, scraping, screenshots, and web testing tasks.
- For operating discipline, follow: `docs/browser-operating-protocol-v1.md`
- Prefer `web_search` / `web_fetch` before browser automation when a lighter tool can answer the request.
- Note: `agent-browser` currently depends on `playwright-core` under the hood.

### Marketing

- Brand voice: Practical, direct, helpful (no hype)
- Primary platforms: LinkedIn, X/Twitter, Website blog
- Posting frequency: 3x/week
- Target audience: Small businesses (5–50 employees) with manual ops workflows
- Core offer: "Fix one workflow in 7 days"
- CTA: 15-minute workflow triage call
- Preferred verticals: Local services, agencies, clinics, retail

### Sub-Agent Model Policy

- Default background / unattended / batch sub-agent work should use the cheaper default model path: **GPT-5.4**
- Use heavier models only when explicitly requested or clearly justified by the task (for example, deep strategy, difficult research synthesis, or especially tricky reasoning)
- In practice: prefer `agentId: main` or the default GPT-5.4 path for background jobs; reserve `deep` / heavier agents for exceptional cases

### GitHub Authentication

**ALWAYS use GitHub App credentials for ALL GitHub operations** (issues, PRs, API calls, etc.)

**Setup:**
- GitHub App credentials stored in `~/.openclaw/.env` (APP_ID, INSTALLATION_ID, KEY_PATH)
- Token generator: `/home/claw/.openclaw/workspace/bin/gh-app-token`
- Git credential helper: `/home/claw/.openclaw/workspace/bin/git-credential-gh-app`

**For `gh` CLI operations:**
```bash
TOKEN=$(/home/claw/.openclaw/workspace/bin/gh-app-token) && echo "$TOKEN" | gh auth login --with-token
```

**For git operations:**
- Already configured via `credential.helper` in git config
- All remotes use HTTPS URLs (not SSH)
- **No SSH keys** — removed to enforce GitHub App usage only

**Primary use cases:**
- Submitting bug reports/issues to external repos
- Creating PRs
- Interacting with GitHub API
- All workspace backup operations (to `andrewtcrooks/openclaw-rook`)

### System Maintenance

**Cache Cleanup Policy:**
- **NEVER** clear anything from `~/.cache/qmd/` — contains vector index DB and GGUF models
- QMD data locations:
  - Index/vectors: `~/.cache/qmd/index.sqlite`
  - Models: `~/.cache/qmd/models/`
  - Config: `~/.config/qmd/index.yml`

### Mem0 Auto-Capture (Always On)

**Before every response:** Search mem0 for relevant context using the user's message as the query:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-search.js "USER_QUERY" --limit=3
```
Inject returned memories into your reasoning before replying. If mem0 fails, continue — never block a response.

**After every substantive exchange:** Store the conversation so mem0 can extract learnings:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-add.js --messages='[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]'
```

**Explicit "remember this":** Store immediately as a direct fact:
```bash
node /home/claw/.openclaw/workspace/skills/mem0/scripts/mem0-add.js "exact fact to remember"
```

**Rules:**
- Always search first, respond second
- Store after conversations containing preferences, patterns, corrections, or new facts
- Do NOT store: secrets, API keys, temporary context, errors, things already in MEMORY.md
- If mem0 errors, log it silently and continue — never surface mem0 failures to the user
