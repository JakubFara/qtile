#!/bin/sh

# systemtray
# ~/Programming/my_keyboard/src/switch_keyboards.sh
setxkbmap -layout nm
# ~/Programming/xrandr/xrandr.sh
# /usr/bin/emacs --daemon
compton &
pulseaudio -k # && sudo alsa force-reload
# pulseaudio --start
# gnome-shell
# xcompmgr
# programs
# mullvad connect
