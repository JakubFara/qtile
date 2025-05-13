#!/usr/bin/env bash
#
# rofi-wifi-setup.sh — pick a Wi-Fi SSID via rofi and store its password
#
# Usage: sudo ./rofi-wifi-setup.sh

set -euo pipefail

# 1) Ensure nmcli is present
if ! command -v nmcli &>/dev/null; then
  echo "Installing NetworkManager…"
  apt update
  DEBIAN_FRONTEND=noninteractive apt install -y network-manager
fi

# 2) Ensure rofi is present
if ! command -v rofi &>/dev/null; then
  echo "Installing rofi…"
  apt update
  DEBIAN_FRONTEND=noninteractive apt install -y rofi
fi

# 3) Scan for SSIDs (one per line, unique)
SSIDS="$(nmcli -t -f SSID dev wifi \
        | grep -v '^$' \
        | sort -u)"

# 4) Pick an SSID
SSID="$(printf '%s\n' "$SSIDS" \
    | rofi -dmenu -p "Select Wi-Fi SSID:" -a 0 -no-custom)"

# Exit if they hit Esc or leave blank
[ -z "$SSID" ] && exit 0

# 5) See if a connection with that name already exists
EXISTING_PSK=""
if nmcli connection show "$SSID" &>/dev/null; then
  EXISTING_PSK="$(nmcli -s -g 802-11-wireless-security.psk \
                   connection show "$SSID" 2>/dev/null || true)"
fi

# 6) Use existing PSK or prompt for it
if [ -n "$EXISTING_PSK" ]; then
  PASSWORD="$EXISTING_PSK"
else
  PASSWORD="$(rofi -dmenu -password -p "Password for $SSID:" -a 0 -no-custom\
      -theme-str 'window { width: 30%; }')"
  [ -z "$PASSWORD" ] && exit 0
fi

# 7) Detect your Wi-Fi interface
IFACE="$(nmcli -t -f DEVICE,TYPE device \
    | awk -F: '$2=="wifi"{print $1; exit}')"
if [ -z "$IFACE" ]; then
  rofi -e "❌ No Wi-Fi interface found!"
  exit 1
fi

# 8) (Re)create the NetworkManager profile
nmcli connection delete "$SSID" &>/dev/null || true
nmcli connection add \
    type wifi \
    ifname "$IFACE" \
    con-name "$SSID" \
    autoconnect yes \
    ssid "$SSID"

nmcli connection modify "$SSID" \
    wifi-sec.key-mgmt wpa-psk \
    wifi-sec.psk "$PASSWORD"

# 9) Activate it now
if nmcli connection up "$SSID"; then
  rofi -e "✅ Connected to $SSID"
else
  rofi -e "❌ Failed to connect to $SSID"
  exit 1
fi
