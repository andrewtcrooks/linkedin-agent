#!/usr/bin/env bash
# linkedin_common.sh - Shared setup sourced by all linkedin-agent scripts
# Source this file at the top of each script: source "$(dirname "$0")/linkedin_common.sh"

# Load openclaw .env for LINKEDIN_SESSION_ID
if [[ -f "${HOME}/.openclaw/.env" ]]; then
  set -a
  source "${HOME}/.openclaw/.env"
  set +a
fi

# Load config from standard locations (first found wins)
for CONFIG_PATH in \
  "${LINKEDIN_AGENT_CONFIG}" \
  "${HOME}/.linkedin-agent/config" \
  "$(dirname "$0")/../config" \
  "$(dirname "$0")/config"
do
  if [[ -n "$CONFIG_PATH" && -f "$CONFIG_PATH" ]]; then
    source "$CONFIG_PATH"
    break
  fi
done

# Support legacy LINKEDIN_PROFILE variable — migrate to LINKEDIN_USERNAME
if [[ -z "$LINKEDIN_USERNAME" ]] && [[ -n "$LINKEDIN_PROFILE" ]]; then
  # Strip full URL if someone set LINKEDIN_PROFILE to https://linkedin.com/in/username
  LINKEDIN_USERNAME="${LINKEDIN_PROFILE##*/in/}"
  LINKEDIN_USERNAME="${LINKEDIN_USERNAME%%/*}"
fi

if [[ -z "$LINKEDIN_USERNAME" ]]; then
  echo "ERROR: LINKEDIN_USERNAME not set. Copy config.example to ~/.linkedin-agent/config and fill it in."
  exit 1
fi

if [[ -z "$AGENT_BROWSER" ]]; then
  # Try to find agent-browser in PATH or common locations
  AGENT_BROWSER=$(which agent-browser 2>/dev/null)
  if [[ -z "$AGENT_BROWSER" ]]; then
    echo "ERROR: AGENT_BROWSER not set and agent-browser not found in PATH."
    exit 1
  fi
fi

AB="$AGENT_BROWSER"

BASE_URL="https://www.linkedin.com/in/${LINKEDIN_USERNAME}"

# Strip ANSI color codes from agent-browser output
strip_ansi() {
  sed 's/\x1b\[[0-9;]*m//g'
}

# Inject the li_at session cookie into agent-browser
inject_session_cookie() {
  if [[ -z "$LINKEDIN_SESSION_ID" ]]; then
    echo "ERROR: LINKEDIN_SESSION_ID not set in ~/.openclaw/.env"
    exit 1
  fi
  $AB cookies set li_at "$LINKEDIN_SESSION_ID" \
    --domain .linkedin.com \
    --path "/" \
    --httpOnly \
    --secure 2>/dev/null
}

# Check for session expiry and re-inject cookie if needed
check_session() {
  local CURRENT_URL
  CURRENT_URL=$($AB get url 2>/dev/null | strip_ansi)
  if [[ "$CURRENT_URL" == *"login"* ]] || [[ "$CURRENT_URL" == *"authwall"* ]]; then
    echo "INFO: Session expired, re-injecting LinkedIn session cookie..."
    inject_session_cookie
    return 1
  fi
  return 0
}

# Open a URL and verify session
open_url() {
  local URL="$1"
  $AB open "$URL" 2>/dev/null
  $AB wait 2000
  check_session
  if [[ $? -ne 0 ]]; then
    $AB open "$URL" 2>/dev/null
    $AB wait 2000
  fi
}
