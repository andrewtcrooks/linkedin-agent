#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/claw/.openclaw/workspace"
DATA_DIR="$ROOT/data/marketing"
METRICS="$DATA_DIR/metrics.csv"

mkdir -p "$DATA_DIR"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/analytics-report.sh weekly
  ./scripts/analytics-report.sh compare

Optional metrics file format (CSV headers):
week_start,platform,impressions,engagements,clicks,followers_delta,conversions
EOF
}

ensure_metrics() {
  if [[ ! -f "$METRICS" ]]; then
    echo "week_start,platform,impressions,engagements,clicks,followers_delta,conversions" > "$METRICS"
    echo "Created template metrics file: $METRICS"
  fi
}

cmd="${1:-}"
case "$cmd" in
  weekly)
    ensure_metrics
    python3 - <<'PY' "$METRICS"
import csv,sys
p=sys.argv[1]
rows=list(csv.DictReader(open(p)))
if not rows:
    print("No metrics yet. Add rows to data/marketing/metrics.csv")
    raise SystemExit(0)
last=max(rows,key=lambda r:r['week_start'])['week_start']
rw=[r for r in rows if r['week_start']==last]
print(f"Weekly report ({last})")
for r in rw:
    imp=float(r.get('impressions') or 0)
    eng=float(r.get('engagements') or 0)
    ctr=(float(r.get('clicks') or 0)/imp*100) if imp else 0
    er=(eng/imp*100) if imp else 0
    print(f"- {r['platform']}: impressions={int(imp)}, engagement_rate={er:.2f}%, ctr={ctr:.2f}%, followers_delta={r.get('followers_delta','0')}, conversions={r.get('conversions','0')}")
PY
    ;;
  compare)
    ensure_metrics
    python3 - <<'PY' "$METRICS"
import csv,sys
p=sys.argv[1]
rows=list(csv.DictReader(open(p)))
weeks=sorted({r['week_start'] for r in rows})
if len(weeks)<2:
    print("Need at least 2 weeks of data to compare.")
    raise SystemExit(0)
cur,we=weeks[-1],weeks[-2]
print(f"Comparing {we} -> {cur}")
for platform in sorted({r['platform'] for r in rows}):
    a=[r for r in rows if r['week_start']==we and r['platform']==platform]
    b=[r for r in rows if r['week_start']==cur and r['platform']==platform]
    if not a or not b:
      continue
    a,b=a[0],b[0]
    def num(r,k):
      try:return float(r.get(k) or 0)
      except:return 0.0
    print(f"- {platform}: impressions {int(num(a,'impressions'))}->{int(num(b,'impressions'))}, engagements {int(num(a,'engagements'))}->{int(num(b,'engagements'))}, conversions {int(num(a,'conversions'))}->{int(num(b,'conversions'))}")
PY
    ;;
  *)
    usage
    exit 1
    ;;
esac
