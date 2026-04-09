#!/usr/bin/env python3
import json, urllib.request, urllib.parse, os, subprocess

STATE_FILE = os.path.expanduser('~/.openclaw/workspace/bin/rookceo-milestones-state.json')

# Load env
env = {}
with open(os.path.expanduser('~/.openclaw/.env')) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

DISCORD_TOKEN     = env['DISCORD_BOT_TOKEN']
ERPNEXT_KEY       = env['ERPNEXT_API_KEY']
ERPNEXT_SECRET    = env['ERPNEXT_API_SECRET']
THREAD_MILESTONES = '1491555993169952870'

# Milestones: every order of magnitude
MILESTONES = [10 ** i for i in range(7)]  # 1, 10, 100, 1000, 10000, 100000, 1000000

def discord_post(thread_id, content):
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'https://discord.com/api/v10/channels/{thread_id}/messages',
        '-H', f'Authorization: Bot {DISCORD_TOKEN}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({'content': content})
    ], capture_output=True, text=True)
    return json.loads(result.stdout)

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {'fired': []}

def save_state(state):
    json.dump(state, open(STATE_FILE, 'w'))

# Get current lead count
try:
    params = urllib.parse.urlencode({
        'filters': '[["campaign_name","=","rookceo.com"]]',
        'fields': '["name"]',
        'limit': 10000
    })
    req = urllib.request.Request(f'https://erpnext.datanovaconsulting.com/api/resource/Lead?{params}')
    req.add_header('Authorization', f'token {ERPNEXT_KEY}:{ERPNEXT_SECRET}')
    with urllib.request.urlopen(req) as r:
        total = len(json.loads(r.read()).get('data', []))
except Exception as e:
    print(f'ERPNext error: {e}')
    raise SystemExit(1)

state = load_state()

for m in MILESTONES:
    if total >= m and m not in state['fired']:
        discord_post(THREAD_MILESTONES, f"""🏆 **Milestone: {m:,} waitlist signup{'s' if m > 1 else ''}!**

rookceo.com just crossed **{m:,}** {'people' if m > 1 else 'person'} on the waitlist.
Total now: **{total:,}**""")
        state['fired'].append(m)
        print(f'Fired milestone: {m}')

save_state(state)
print(f'Done. Total leads: {total}, fired so far: {state["fired"]}')
