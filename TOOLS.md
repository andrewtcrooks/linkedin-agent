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
- Note: `agent-browser` currently depends on `playwright-core` under the hood.

### Marketing

- Brand voice: Practical, direct, helpful (no hype)
- Primary platforms: LinkedIn, X/Twitter, Website blog
- Posting frequency: 3x/week
- Target audience: Small businesses (5–50 employees) with manual ops workflows
- Core offer: "Fix one workflow in 7 days"
- CTA: 15-minute workflow triage call
- Preferred verticals: Local services, agencies, clinics, retail

### System Maintenance

**Cache Cleanup Policy:**
- **NEVER** clear anything from `~/.cache/qmd/` — contains vector index DB and GGUF models
- QMD data locations:
  - Index/vectors: `~/.cache/qmd/index.sqlite`
  - Models: `~/.cache/qmd/models/`
  - Config: `~/.config/qmd/index.yml`
