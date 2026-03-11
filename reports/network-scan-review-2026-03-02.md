# Network Scan Review — 2026-03-02 10:00 PT

Compared against baseline report: `reports/network-scan-2026-02-28.md`.

## Current snapshot
- Network: `192.168.1.0/24`
- Ping-responsive hosts: 14
- Open common TCP ports scanned: 22, 53, 80, 139, 443, 445, 554, 631, 1883, 8080

## Exposure delta vs baseline
### New responsive hosts
- `192.168.1.125` (no common ports found open)
- `192.168.1.151` (`22`, `80` open)

### Hosts no longer responsive
- `192.168.1.18`

### Unchanged notable exposure
- SMB still visible on multiple hosts: `.1, .21, .40, .41, .42, .130` (`139/445`)
- Legacy-risk host still exposed: `.130` (`22,80,139,443,445`)
- MQTT still exposed on `.44:1883`
- RTSP still exposed on `.50:554`

## Prioritized next actions
1. Identify device owners for `.151` and `.125`; confirm expected behavior.
2. Prioritize hardening `.130` (legacy Dropbear + SMB + web services).
3. Reduce SMB exposure scope (disable where unnecessary, segment VLANs where possible).
4. Keep `.44` MQTT and `.50` RTSP LAN-only with strong auth/ACLs.

## Raw current map (common ports)
- 192.168.1.1: 53, 80, 139, 445
- 192.168.1.20: 80, 443, 631, 8080
- 192.168.1.21: 139, 445
- 192.168.1.40: 22, 139, 445
- 192.168.1.41: 80, 139, 445
- 192.168.1.42: 22, 80, 139, 443, 445
- 192.168.1.43: 22, 80
- 192.168.1.44: 22, 1883
- 192.168.1.50: 554
- 192.168.1.101: 80, 443, 8080
- 192.168.1.130: 22, 80, 139, 443, 445
- 192.168.1.151: 22, 80
- 192.168.1.200: 22, 80, 443
