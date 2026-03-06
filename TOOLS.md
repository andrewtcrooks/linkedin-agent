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

### MuninnDB — Cognitive Memory

MuninnDB is running on this Pi as a systemd user service (`muninn.service`).
It provides persistent, cognitive memory across sessions via MCP.

- **MCP endpoint:** `http://localhost:8750/mcp`
- **REST API:** `http://localhost:8475`
- **Web UI:** `http://localhost:8476` (admin / password — change after first login)
- **Data dir:** `~/.muninn/data`
- **Service:** `systemctl --user status muninn`
- **Logs:** `muninn logs`
- **Upgrade:** `muninn upgrade`

MCP tools available (call `muninn_guide` for full vault-aware usage instructions):
- `muninn_remember` — store a memory (concept + content + optional tags)
- `muninn_recall` — retrieve relevant memories by context
- `muninn_activate` — context-aware ranked recall (full cognitive pipeline)
- `muninn_search` — text search across memories
- `muninn_forget` — delete a specific memory
- `muninn_guide` — get usage instructions from the DB itself

### Web Browsing Policy

- Default web page browsing/automation path: **agent-browser** skill/workflow.
- Prefer agent-browser for opening pages, interacting with sites, scraping, screenshots, and web testing tasks.
- Note: `agent-browser` currently depends on `playwright-core` under the hood.

### Marketing

- Brand voice: Practical, direct, helpful (no hype)
- Primary platforms: LinkedIn, X/Twitter, Website blog
- Posting frequency: 3x/week
- Target audience: Small businesses (5–50 employees) with manual ops workflows
- Core offer: "Fix one workflow in 7 days"
- CTA: 15-minute workflow triage call
- Preferred verticals: Local services, agencies, clinics, retail
