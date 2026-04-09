#!/usr/bin/env python3
import json, urllib.request, urllib.parse, datetime, os, sys, subprocess

# Load env
env = {}
with open(os.path.expanduser('~/.openclaw/.env')) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

DISCORD_TOKEN     = env['DISCORD_BOT_TOKEN']
UMAMI_USER        = env['UMAMI_USER']
UMAMI_PASSWORD    = env['UMAMI_PASSWORD']
ERPNEXT_KEY       = env['ERPNEXT_API_KEY']
ERPNEXT_SECRET    = env['ERPNEXT_API_SECRET']
UMAMI_WEBSITE_ID  = '4b3a6b6a-385c-4146-87b6-1a603f1384e9'

THREAD_MILESTONES = '1491555993169952870'
THREAD_LEADS      = '1491552844619448321'
THREAD_TRAFFIC    = '1491552622237454538'

# Date range: yesterday midnight → today midnight (local)
now           = datetime.datetime.now()
today_start   = datetime.datetime(now.year, now.month, now.day)
yesterday     = today_start - datetime.timedelta(days=1)
start_ms      = int(yesterday.timestamp() * 1000)
end_ms        = int(today_start.timestamp() * 1000)
date_str      = yesterday.strftime('%B %d, %Y')

def discord_post(thread_id, content):
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'https://discord.com/api/v10/channels/{thread_id}/messages',
        '-H', f'Authorization: Bot {DISCORD_TOKEN}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({'content': content})
    ], capture_output=True, text=True)
    return json.loads(result.stdout)

def umami_get(path, token):
    req = urllib.request.Request(f'https://umami.datanovaconsulting.com{path}')
    req.add_header('Authorization', f'Bearer {token}')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def erpnext_get(path):
    req = urllib.request.Request(f'https://erpnext.datanovaconsulting.com{path}')
    req.add_header('Authorization', f'token {ERPNEXT_KEY}:{ERPNEXT_SECRET}')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# ── Umami login ──────────────────────────────────────────────
data = json.dumps({'username': UMAMI_USER, 'password': UMAMI_PASSWORD}).encode()
req  = urllib.request.Request('https://umami.datanovaconsulting.com/api/auth/login', data=data, method='POST')
req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(req) as r:
    umami_token = json.loads(r.read())['token']

# ── Traffic (yesterday) ──────────────────────────────────────
stats     = umami_get(f'/api/websites/{UMAMI_WEBSITE_ID}/stats?startAt={start_ms}&endAt={end_ms}', umami_token)
visitors  = stats.get('visitors',  {}).get('value', 0)
pageviews = stats.get('pageviews', {}).get('value', 0)
bounces   = stats.get('bounces',   {}).get('value', 0)
bounce_pct = round((bounces / visitors * 100) if visitors else 0)

# Top referrers
try:
    refs     = umami_get(f'/api/websites/{UMAMI_WEBSITE_ID}/metrics?startAt={start_ms}&endAt={end_ms}&type=referrer', umami_token)
    top_refs = refs[:3] if refs else []
    ref_lines = '\n'.join(f"  • {r['x'] or 'Direct'}: {r['y']}" for r in top_refs)
except Exception:
    ref_lines = '  • No referrer data'

traffic_notable = []
if visitors == 0:
    traffic_notable.append('No traffic yesterday.')
if visitors >= 100:
    traffic_notable.append(f'Strong day — {visitors} unique visitors.')

traffic_msg = f"""**Site Traffic — {date_str}**

👥 Visitors: **{visitors}**
📄 Pageviews: **{pageviews}**
↩️ Bounce rate: **{bounce_pct}%**

**Top referrers:**
{ref_lines if ref_lines else '  • None'}
{chr(10) + ' '.join(traffic_notable) if traffic_notable else ''}
_rookceo.com · Umami_"""

discord_post(THREAD_TRAFFIC, traffic_msg)

# ── Leads ────────────────────────────────────────────────────
try:
    params = urllib.parse.urlencode({
        'filters': '[["campaign_name","=","rookceo.com"]]',
        'fields': '["name","creation","email_id"]',
        'order_by': 'creation desc',
        'limit': 500
    })
    all_leads = erpnext_get(f'/api/resource/Lead?{params}').get('data', [])
except Exception as e:
    all_leads = []
    print(f'ERPNext error: {e}', file=sys.stderr)

total_leads = len(all_leads)
yesterday_str = yesterday.strftime('%Y-%m-%d')
new_today = [l for l in all_leads if l.get('creation', '').startswith(yesterday_str)]
new_count = len(new_today)

leads_notable = []
if new_count == 0:
    leads_notable.append('No new signups yesterday.')
if new_count >= 10:
    leads_notable.append(f'Big day — {new_count} new signups!')

leads_msg = f"""**Lead Analytics — {date_str}**

📬 New signups: **{new_count}**
📊 Total waitlist: **{total_leads}**
{chr(10) + ' '.join(leads_notable) if leads_notable else ''}
_ERPNext · rookceo.com waitlist_"""

discord_post(THREAD_LEADS, leads_msg)

# ── Milestones ───────────────────────────────────────────────
milestones = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
for m in milestones:
    if total_leads >= m and new_count > 0:
        # only fire if we crossed this milestone today
        pre_today = total_leads - new_count
        if pre_today < m:
            discord_post(THREAD_MILESTONES, f"""🏆 **Milestone hit: {m} waitlist signups!**

rookceo.com crossed **{m}** people on the waitlist.
Total now: **{total_leads}**

_{date_str}_""")

print(f'Done. Leads: {total_leads} (+{new_count}), Visitors: {visitors}')
