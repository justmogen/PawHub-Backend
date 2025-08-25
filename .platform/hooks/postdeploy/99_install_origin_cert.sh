#!/bin/bash
set -euo pipefail

# directory to hold certs
mkdir -p /etc/ssl/cloudflare
chmod 700 /etc/ssl/cloudflare

# decode base64 env vars into files
if [[ -n "${ORIGIN_CERT_B64:-}" && -n "${ORIGIN_KEY_B64:-}" ]]; then
  echo "$ORIGIN_CERT_B64" | base64 -d > /etc/ssl/cloudflare/origin.crt
  echo "$ORIGIN_KEY_B64"  | base64 -d > /etc/ssl/cloudflare/origin.key

  chmod 644 /etc/ssl/cloudflare/origin.crt
  chmod 600 /etc/ssl/cloudflare/origin.key

  # test nginx config then reload
  if nginx -t; then
    systemctl reload nginx || service nginx reload || true
  fi
else
  echo "ORIGIN_CERT_B64 or ORIGIN_KEY_B64 not set — skipping origin cert install" >&2
fi
