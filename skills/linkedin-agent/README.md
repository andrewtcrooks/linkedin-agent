# linkedin-agent

Professional LinkedIn profile management via browser automation. Full read/write control over every profile section, designed for use with AI agents (OpenClaw, Claude Code) or directly from the command line.

## What it does

- **Edit every profile section**: intro/header, summary, experience, education, skills, services, projects, volunteering, honors, languages
- **Manage Open To Work**: titles, location types, start date, employment types, visibility
- **Posts management**: list, audit (with engagement metrics), delete, create
- **Profile analytics**: views, search appearances, post impressions (read-only)
- **Endorsement protection**: endorsed skills cannot be deleted — only reordered

## Requirements

- [agent-browser](https://github.com/browserbase/agent-browser) installed
- `bash` 4+
- LinkedIn `li_at` session cookie (see Authentication below)

## Authentication

These scripts use your LinkedIn session cookie instead of a username and password. LinkedIn does not provide an official API, so cookie-based auth is the standard approach for automation.

### Getting your li_at cookie

1. Open Chrome and go to [linkedin.com](https://www.linkedin.com)
2. Log in to your LinkedIn account
3. Open DevTools: `Cmd+Option+I` (Mac) or `Ctrl+Shift+I` (Windows)
4. Click the **Application** tab
5. In the left sidebar, expand **Cookies** → click `https://www.linkedin.com`
6. Find the cookie named **`li_at`**
7. Click it and copy the full value from the **Value** column

### Storing the cookie

Add it to `~/.openclaw/.env`:

```bash
LINKEDIN_SESSION_ID=AQEDATxxxxxxxxxxxxxxxxxxxxxx...
```

The scripts automatically source `~/.openclaw/.env` and inject this cookie into agent-browser on each run. If the session expires, simply get a fresh `li_at` value from Chrome and update the file.

> **Note:** The `li_at` cookie is tied to your browser session. LinkedIn may expire it after a period of inactivity or if you log out. If scripts start redirecting to the login page, refresh the cookie.

## Quick Start

```bash
git clone <repo-url> ~/.openclaw/workspace/skills/linkedin
cd ~/.openclaw/workspace/skills/linkedin
./install.sh
```

Then edit `~/.linkedin-agent/config`:
```bash
LINKEDIN_PROFILE="your-username"
AGENT_BROWSER="$HOME/.openclaw/workspace/node_modules/.bin/agent-browser"
```

And add to `~/.openclaw/.env`:
```bash
LINKEDIN_SESSION_ID=<paste your li_at value here>
```

## Scripts

| Script | Purpose |
|--------|---------|
| `linkedin_edit_intro.sh` | Name, headline, pronouns, industry, location |
| `linkedin_edit_summary.sh` | About/summary text |
| `linkedin_edit_experience.sh` | Work experience entries |
| `linkedin_edit_education.sh` | Education entries |
| `linkedin_edit_skills.sh` | Skills (with endorsement guard + reorder) |
| `linkedin_edit_otw.sh` | Open To Work settings |
| `linkedin_edit_services.sh` | Services page |
| `linkedin_edit_projects.sh` | Projects section |
| `linkedin_edit_volunteering.sh` | Volunteering section |
| `linkedin_edit_honors.sh` | Honors & Awards |
| `linkedin_edit_languages.sh` | Languages |
| `linkedin_manage_posts.sh` | Recent posts (list, audit, delete, create) |
| `linkedin_analytics.sh` | Profile/search/post analytics (read-only) |

See [SKILL.md](SKILL.md) for full usage documentation.

## AI Agent Integration

This repo includes `SKILL.md` — a skill file compatible with both OpenClaw and Claude Code. Drop this repo into your skills directory and your agent gains full LinkedIn profile control.

```
# Example agent prompt
Use linkedin-agent to audit my profile and optimize it for a
Senior Data Engineer role targeting remote positions at Series B startups.
```

## Safety

- Scripts never store credentials — authentication uses a session cookie stored in `~/.openclaw/.env`
- `--remove` on skills checks endorsements first and permanently blocks deletion of endorsed skills
- `--delete` on posts is irreversible — use `--audit` to review before deleting
- Analytics scripts are read-only

## License

MIT
