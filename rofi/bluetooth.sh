#!/usr/bin/env bash

# Ensure environment for GUI and notifications
export DISPLAY=:0
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Simple notify wrapper
function notify() {
    if command -v notify-send >/dev/null; then
        notify-send "$1" "$2"
    else
        echo "$1: $2"
    fi
}

# Get list of paired devices with connection status
device_list=()
mapfile -t lines < <(bluetoothctl devices)

for line in "${lines[@]}"; do
    mac=$(echo "$line" | awk '{print $2}')
    name=$(echo "$line" | cut -d ' ' -f 3-)

    if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
        device_list+=("⚪ $name | $mac")
    else
        device_list+=("   $name | $mac")
    fi
done

# If no devices found
if [[ ${#device_list[@]} -eq 0 ]]; then
    notify "Bluetooth" "No paired devices found."
    exit 1
fi

# Show selection in rofi
selection=$(printf '%s\n' "${device_list[@]}" | rofi -dmenu -p "Bluetooth Devices" -l 10)
[[ -z "$selection" ]] && exit 0

# Extract MAC and name
mac=$(echo "$selection" | awk -F'\\| ' '{print $2}')
name=$(echo "$selection" | awk -F'\\| ' '{print $1}' | sed 's/^✅ //;s/^ *//')

# If already connected
if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
    action=$(echo -e "Disconnect\nForget" | rofi -dmenu -p "$name is connected. Choose action:")
    case "$action" in
        Disconnect)
            bluetoothctl disconnect "$mac" && notify "Bluetooth" "🔌 Disconnected from $name"
            ;;
        Forget)
            bluetoothctl remove "$mac" && notify "Bluetooth" "🗑 Removed $name"
            ;;
    esac
else
    notify "Bluetooth" "🔄 Connecting to $name..."
    bluetoothctl connect "$mac" > /tmp/bt_connect.log 2>&1
    sleep 2
    if bluetoothctl info "$mac" | grep -q "Connected: yes"; then
        notify "Bluetooth" "✅ Connected to $name"
    else
        notify "Bluetooth" "❌ Failed to connect to $name"
        cat /tmp/bt_connect.log
    fi
fi
