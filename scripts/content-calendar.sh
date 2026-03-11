#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/claw/.openclaw/workspace"
DATA_DIR="$ROOT/data/marketing"
CAL="$DATA_DIR/content-calendar.csv"

mkdir -p "$DATA_DIR"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/content-calendar.sh init
  ./scripts/content-calendar.sh add YYYY-MM-DD PLATFORM "CONTENT" [CTA]
  ./scripts/content-calendar.sh week
  ./scripts/content-calendar.sh month

Examples:
  ./scripts/content-calendar.sh init
  ./scripts/content-calendar.sh add 2026-03-05 linkedin "Post about SMB ops bottlenecks" "Book workflow triage"
EOF
}

cmd="${1:-}"
case "$cmd" in
  init)
    if [[ ! -f "$CAL" ]]; then
      echo "date,platform,content,cta,status" > "$CAL"
      echo "Initialized: $CAL"
    else
      echo "Already exists: $CAL"
    fi
    ;;
  add)
    [[ $# -lt 4 ]] && { usage; exit 1; }
    date="$2"; platform="$3"; content="$4"; cta="${5:-}";
    [[ ! -f "$CAL" ]] && echo "date,platform,content,cta,status" > "$CAL"
    esc() { printf '%s' "$1" | sed 's/"/""/g'; }
    printf '"%s","%s","%s","%s","planned"\n' "$(esc "$date")" "$(esc "$platform")" "$(esc "$content")" "$(esc "$cta")" >> "$CAL"
    echo "Added entry for $date ($platform)."
    ;;
  week)
    [[ ! -f "$CAL" ]] && { echo "No calendar found. Run init first."; exit 1; }
    python3 - <<'PY' "$CAL"
import csv,datetime,sys
p=sys.argv[1]
today=datetime.date.today()
end=today+datetime.timedelta(days=7)
print(f"Entries {today} to {end}:")
with open(p,newline='') as f:
    for r in csv.DictReader(f):
        try:
            d=datetime.date.fromisoformat(r['date'])
        except Exception:
            continue
        if today<=d<=end:
            print(f"- {r['date']} [{r['platform']}] {r['content']} | CTA: {r['cta']} | {r['status']}")
PY
    ;;
  month)
    [[ ! -f "$CAL" ]] && { echo "No calendar found. Run init first."; exit 1; }
    python3 - <<'PY' "$CAL"
import csv,datetime,sys
p=sys.argv[1]
today=datetime.date.today()
end=today+datetime.timedelta(days=31)
print(f"Entries {today} to {end}:")
with open(p,newline='') as f:
    for r in csv.DictReader(f):
        try:
            d=datetime.date.fromisoformat(r['date'])
        except Exception:
            continue
        if today<=d<=end:
            print(f"- {r['date']} [{r['platform']}] {r['content']} | CTA: {r['cta']} | {r['status']}")
PY
    ;;
  *)
    usage
    exit 1
    ;;
esac
