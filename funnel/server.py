#!/usr/bin/env python3
import csv
import json
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path('/home/claw/.openclaw/workspace/funnel')
LEADS = Path('/home/claw/.openclaw/workspace/data/marketing/leads.csv')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _json(self, code, obj):
        b = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        if self.path != '/submit':
            return self._json(404, {'ok': False, 'error': 'not_found'})
        try:
            n = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(n)
            data = json.loads(raw.decode('utf-8'))
        except Exception:
            return self._json(400, {'ok': False, 'error': 'bad_json'})

        business = (data.get('business') or '').replace('\n', ' ').strip()
        email = (data.get('email') or '').replace('\n', ' ').strip()
        score = int(data.get('score') or 0)
        answers = data.get('answers') or []
        notes = f"score={score}/8 answers={answers} submitted_at={datetime.now().isoformat(timespec='seconds')}"

        LEADS.parent.mkdir(parents=True, exist_ok=True)
        if not LEADS.exists():
            with LEADS.open('w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['business_name','contact_name','phone','email','city','vertical','pain_score','status','next_step','notes'])

        with LEADS.open('a', newline='') as f:
            w = csv.writer(f)
            w.writerow([business,'','',''+email,'','',''+str(score),'new','workflow triage',notes])

        return self._json(200, {'ok': True})

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 8099), Handler).serve_forever()
