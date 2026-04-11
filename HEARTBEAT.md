# HEARTBEAT.md

Use heartbeat as a lightweight watchdog for GetRook, not as a heavy work loop.

On each heartbeat:
1. Check `/home/claw/.openclaw/workspace/getrook/NOW.md` exists.
2. Check whether the GetRook operating files still exist and look healthy:
   - `/home/claw/.openclaw/workspace/getrook/START_HERE.md`
   - `/home/claw/.openclaw/workspace/getrook/AGENTS.md`
   - `/home/claw/.openclaw/workspace/getrook/EXECUTION.md`
   - `/home/claw/.openclaw/workspace/getrook/NOW.md`
3. Check whether the daily progress channel exists conceptually by relying on the known channel id:
   - `1492387680468860979`
4. Check whether GetRook cron jobs exist in `/home/claw/.openclaw/cron/jobs.json`:
   - `91d60d6d-4df4-4a5d-83f8-9d3c5c3e9b01`
   - `1e7931c5-1efd-46d0-82ca-4fd13b9d9c02`
   - `8a0f8f57-c958-4219-bf92-aeb6e0a6c503`
5. If any of the above is missing or obviously broken, alert briefly with the specific missing item.
6. Otherwise reply exactly `HEARTBEAT_OK`.

Rules:
- Do not do heavy project work from heartbeat.
- Do not repeat old project summaries.
- Do not run broad research from heartbeat.
- Only surface concrete breakage or absence.
