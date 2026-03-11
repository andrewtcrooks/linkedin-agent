# Network Security Scan — 2026-02-28

## Scope
- Network: `192.168.1.0/24`
- Method: safe/light scan (host discovery + common ports), followed by targeted deep probe
- Scanner host: `192.168.1.200`

## Ping-responsive hosts (13)
- 192.168.1.1
- 192.168.1.18
- 192.168.1.20
- 192.168.1.21
- 192.168.1.40
- 192.168.1.41
- 192.168.1.42
- 192.168.1.43
- 192.168.1.44
- 192.168.1.50
- 192.168.1.101
- 192.168.1.130
- 192.168.1.200

## Common open TCP ports found
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
- 192.168.1.200: 22, 80, 443

## Targeted deep probe (selected hosts)
### 192.168.1.1
- 53: open
- 80: `HTTP/1.0 200 OK | server=httpd/3.0`
- 139: open
- 445: open

### 192.168.1.40
- 22: `SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u5`
- 139: open
- 445: open

### 192.168.1.42
- 22: `SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u5`
- 80: `HTTP/1.1 200 OK | server=openresty | title=Default Site`
- 139: open
- 443: open (no banner)
- 445: open

### 192.168.1.130
- 22: `SSH-2.0-dropbear_2017.75` (legacy/old)
- 80: `HTTP/1.0 200 OK | server=httpd/2.0`
- 139: open
- 443: `HTTP/1.1 401 Unauthorized | server=lighttpd/1.4.39`
- 445: open

### 192.168.1.44
- 22: `SSH-2.0-OpenSSH_10.2`
- 1883: MQTT response present

### 192.168.1.50
- 554: `RTSP/1.0 200 OK | Server: Rtsp Server`

## Prioritized findings
1. 192.168.1.130 appears highest-risk (old Dropbear + SMB + web services).
2. SMB exposure on multiple hosts (`139/445`) should be reduced/segmented.
3. RTSP camera service (`.50:554`) should remain LAN-only with strong credentials.
4. MQTT broker (`.44:1883`) should use auth/TLS and restricted clients.

## Next review target
- Re-check on Monday around 10:00 AM PT for delta and remediation progress.
