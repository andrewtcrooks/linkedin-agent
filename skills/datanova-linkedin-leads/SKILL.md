---
name: datanova-linkedin-leads
description: Generate B2B leads for Data Nova Consulting from LinkedIn using agent-browser workflows: search prospects, extract profile/company signals, score against ICP, and prepare compliant outreach drafts. Use when asked to find potential clients on LinkedIn, build lead lists, personalize first-touch messages, or run prospecting batches for datanovaconsulting.com.
---

# Data Nova LinkedIn Leads

Use this skill to run a repeatable LinkedIn lead-gen workflow with `agent-browser`.

## Run sequence

1. Confirm campaign inputs before browsing:
   - Geo/market
   - Target verticals
   - Role titles/seniority
   - Team size (default 5–50)
   - Outreach volume target
2. Use `agent-browser` to collect prospects from LinkedIn search results and profile pages.
3. Score each lead with the ICP rubric in `references/icp.md`.
4. Keep only qualified leads.
5. Draft personalized outreach with templates in `references/outreach.md`.
6. Present leads + drafts for approval.
7. Send outreach only after explicit user approval.

## Data to capture per lead

- Full name
- LinkedIn URL
- Current role/title
- Company name + LinkedIn/company URL
- Estimated employee size (if visible)
- Industry/vertical
- Location
- Trigger/context note (recent post, hiring, tool-stack, pain signal)
- ICP score + reason
- Draft first message

## Output format

Return a compact table/list with:

- Qualified leads
- ICP score + 1-line rationale
- Personalized message draft
- Recommended channel (LinkedIn DM / email)

## Rules

- Use `agent-browser` for web interaction tasks.
- Do not blast generic messages.
- Personalize each message using observed profile/company context.
- Do not send any external message without explicit approval in the current session.
- If LinkedIn blocks automation or rate-limits, stop, report, and ask for a slower/manual pass.
