# OpenClaw-Native Proactive Memory Loop (OpenAI-compatible)

This replaces external `memU` runtime requirements with an OpenClaw-native loop that works with existing model access.

## What it does

1. **Session capture loop (every 6 hours)**
   - Reviews recent conversation context
   - Appends concise notes to `memory/YYYY-MM-DD.md`
   - Focuses on decisions, requests, follow-ups, and TODOs

2. **Long-term distill loop (daily)**
   - Reviews recent daily notes + `MEMORY.md`
   - Promotes durable items into `MEMORY.md`
   - Avoids duplication and stale details

## Why this approach

- No external API keys required for separate Python runtimes
- Uses OpenClaw-native memory files and tool access
- Keeps notes human-readable and auditable in workspace

## Files involved

- `memory/YYYY-MM-DD.md` (raw daily notes)
- `MEMORY.md` (curated long-term memory)

## Operational notes

- Capture job should stay mostly silent unless there is a meaningful note or action item.
- Distill job should update long-term memory only when truly durable insights appear.
- All outputs should avoid sensitive secret material.
