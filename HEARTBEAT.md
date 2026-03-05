# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## Periodic Checks

- **MuninnDB health:** run `muninn status` — if any service is down, run `systemctl --user restart muninn` and report.
