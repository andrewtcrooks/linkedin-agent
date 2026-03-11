#!/usr/bin/env bash
# LinkedIn Contact Info Scraper
# Reads lead-generator-first-third-preview.csv, visits each profile,
# opens Contact info overlay, extracts email + website.
set -euo pipefail

WORKSPACE="/home/claw/.openclaw/workspace"
INPUT="$WORKSPACE/leads/lead-generator-first-third-preview.csv"
OUTPUT="$WORKSPACE/leads/leads-with-contact.csv"
SESSION="datanova-leads"
LOG="$WORKSPACE/leads/contact-scrape.log"

ab() {
  agent-browser --session-name "$SESSION" "$@" 2>&1 || true
}

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

# Write CSV header
echo "first_name,last_name,designation,company_name,linkedin_url,industry,no_of_employees,source,status,campaign_name,email,website,phone" > "$OUTPUT"

# Read CSV (skip header)
total=$(tail -n +2 "$INPUT" | wc -l)
i=0

tail -n +2 "$INPUT" | while IFS=',' read -r first_name last_name designation company_name linkedin_url industry employees source status campaign; do
  # Strip quotes
  linkedin_url=$(echo "$linkedin_url" | tr -d '"')
  first_name=$(echo "$first_name" | tr -d '"')
  last_name=$(echo "$last_name" | tr -d '"')
  company_name=$(echo "$company_name" | tr -d '"')

  i=$((i+1))
  log "[$i/$total] $first_name $last_name @ $company_name"
  log "  URL: $linkedin_url"

  # Navigate directly to contact-info overlay (avoids needing to click button)
  overlay_url="${linkedin_url%/}/overlay/contact-info/"
  ab open "$overlay_url"
  ab wait --load networkidle
  sleep 2

  # Get page text
  page_text=$(ab snapshot) || page_text=""

  # Extract email
  email=$(echo "$page_text" | grep -oE '[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}' | grep -v 'linkedin\|example\|test' | head -1 || echo "")

  # Extract website (non-linkedin URL in snapshot)
  website=$(echo "$page_text" | grep -oP '(?<=/url: )https?://(?!(?:www\.)?linkedin\.com)[^\s]+' | head -1 || echo "")

  # Extract phone (basic pattern)
  phone=$(echo "$page_text" | grep -oP '\+?[0-9][0-9 \-\.()]{6,18}[0-9]' | head -1 || echo "")

  log "  email=${email:-none} website=${website:-none}"

  # Append to CSV
  printf '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' \
    "$first_name" "$last_name" "$designation" "$company_name" "$linkedin_url" \
    "$industry" "$employees" "$source" "$status" "$campaign" \
    "$email" "$website" "$phone" \
    | tr -d '\r' >> "$OUTPUT"

  # Polite pause (3-5 seconds)
  sleep $((3 + RANDOM % 3))
done

log "Done. Output: $OUTPUT"
with_email=$(tail -n +2 "$OUTPUT" | awk -F',' '{print $11}' | grep -v '^""$' | grep -v '^$' | wc -l)
log "Leads with email: $with_email / $total"
