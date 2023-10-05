# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import layout
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Bar
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger
import os
from libqtile import hook
from libqtile.layout.columns import Columns
from libqtile.layout.verticaltile import VerticalTile
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack
from libqtile.layout.floating import Floating
from libqtile.config import (
    Click,
    Drag,
    DropDown,
    Group,
    Key,
    Match,
    ScratchPad,
    Screen
)

import subprocess
from libqtile.utils import guess_terminal

from libqtile.lazy import lazy

from colors import nord_fox
# from libqtile import withet as withet_old #import Volume
from qtile_extras import widget
# from src.bar1 import bar
from palette import palette
from my_widgets import MyBattery, MyCalendar, MyVolume
from icons import ICONS
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

mod = "mod4"
home_dir = "/home/jakub/"
# terminal = guess_terminal()
terminal = "gnome-terminal"
# path_to_config = os.path.abspath(__file__)[:-len(__file__)]

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Move window focus to other window"
    ),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume by 5%"
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume by 5%"
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute 0 toggle"),
        desc="Mute/Unmute Volume"
    ),
    Key(
        [],
        'XF86MonBrightnessUp',
        lazy.spawn("brightness-controller"),
        desc="Mute/Unmute Volume"
    ),
    Key(
        [mod],
        'm',
        lazy.spawn(f"{home_dir}/.config/qtile/rofi/monitors-layout.sh"),
        desc="Mute/Unmute Volume"
    ),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "a", lazy.spawn("rofi -show drun -show-icons -modi drun, run"), desc="Spawn a command using a prompt widget"),
    Key([mod], "k", lazy.spawn(f"{home_dir}/.config/qtile/rofi/kill-process.sh"), desc="Kill process with rofi"),
    Key([mod], "n", lazy.spawn("/home/jakub/Programming/my_keyboard/src/switch_keyboards.sh"), desc="Swith keyboards."),
    Key([mod], "o", lazy.spawn("rofi -show window"), desc="Show all running apps."),
    Key([mod], "Print", lazy.spawn("flameshot gui"), desc="Show all running apps."),
]

groups = [
    Group("1", spawn="google-chrome"),
    Group("2", spawn="emacs"),
    Group("3", spawn=["discord", "skype"]),
    Group("4", spawn=[]),
    Group("5", spawn=["gnome-control-center", "blueman-manager"]),
    Group("6"),
    Group("7"),
    Group("8"),
    Group("9"),
]

groups.append(
    ScratchPad(
        '0',
        [
            DropDown(
                'term',
                'kitty',
                width=0.4,
                height=0.5,
                x=0.3,
                y=0.1,
                opacity=1
            ),
            DropDown(
                'file manager',
                'thunar',
                width=0.4,
                height=0.5,
                x=0.3,
                y=0.1,
                opacity=1
            ),
        ]
    )
)
keys.extend([
    Key([mod], "u", lazy.group['0'].dropdown_toggle('term')),
    Key([mod], "y", lazy.group['0'].dropdown_toggle('file manager')),
])

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
]

margin_const=4

layouts = [
    layout.MonadTall(
        border_focus="#9ccfd8",
        border_normal="#31748f",
        border_width=1,
        margin=margin_const
    ),
    layout.Max(),
    layout.Bsp(border_focus="#9ccfd8", border_normal="#31748f",
               border_width=1, margin=margin_const),
    layout.MonadWide(border_focus="#9ccfd8",
                     border_normal="#31748f", border_width=1, margin=margin_const),
    layout.RatioTile(border_focus="#9ccfd8",
                     border_normal="#31748f", border_width=1, margin=margin_const),
    # layout.Matrix(),
]
# widget_defaults = dict(
#     font="sans",
#     fontsize=12,
#     padding=3,
# )
# extension_defaults = widget_defaults.copy()

powerline = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_x=0, filled=False, radius=0),
        PowerLineDecoration(path='rounded_right', padding_x=0)
    ]
}
powerline_left = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_x=0, padding_y=0, filled=False, radius=0),
        PowerLineDecoration(path='rounded_left')
    ]
}

# background = "#000000a0"
background = palette.surface0 + "80"

bar = Bar(
    [
        # widget.TextBox("", background="", name="default", **powerline),
        widget.TextBox(" ", background=background, name="default", **powerline),
        # widget.Bluetooth(
        #     font="MesloLGS NF Regular",
        #     hci0="/dev_F8_94_C2_D5_B1_E0",
        #     background=palette.red,
        #     # foreground=colors[15],
        #     # fontsize=14,
        #     **powerline
        # ),
        widget.GroupBox(foreground=palette.maroon, background=palette.subtext0, **powerline_left),
        widget.TextBox(" ", name="default", **powerline),
        widget.WindowName(foreground="#00000000", background=background, **powerline),
        widget.TextBox(" ", name="default", **powerline),
        MyCalendar(foreground="#000000", background=palette.subtext0, **powerline_left),
        # widget.GroupBox(foreground=palette.base, background=palette.crust, **powerline_left),
        widget.TextBox(" ", name="default", **powerline),
        widget.CurrentLayoutIcon(foreground=palette.base, background=palette.sky, **powerline_left),
        widget.TextBox("", background="", name="default", **powerline),
        widget.TextBox(" ", name="default", **powerline),
        # widget.UPowerWidget(background=palette.crust, **powerline_left),
        MyBattery(
            background=palette.rosewater,
            foreground=palette.base,
            font="Font Awesome",
            # format=f"{icons['battery']}" + '{percent:2.0%}',
            format="lol",
            padding=5,
            low_foreground="red",
            **powerline_left
        ),
        widget.TextBox(" ", name="default", **powerline),

        MyVolume(
            foreground=palette.base,
            background=palette.blue,
            emoji=True,
            mute_command=[
                'pactl set-sink-mute 0 toggle'
            ],
            width=5,
            padding=0,
            **powerline_left
        ),
        MyVolume(
            foreground=palette.base,
            background=palette.blue,
            emoji=False,
            mute_command=[
                'pactl set-sink-mute 0 toggle'
            ],
            width=40,
            **powerline_left
        ),
        widget.TextBox(" ", name="default", **powerline),
        widget.Clock(
            fmt=ICONS["clock"],
            foreground=palette.base,
            background=palette.red,
            **powerline_left
        ),
        widget.TextBox(" ", name="default", **powerline),
        widget.QuickExit(
            default_text=ICONS["turnoff"],
            reground=palette.base,
            background=palette.subtext0,
            **powerline_left
        ),
       # widget.TextBox(" ", name="default", **powerline_left),
    ],
    30,
    # opacity=0.8,
    background=background
)

screens = [
    Screen(
        top=bar,
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='stretch',
    ),

    Screen(
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='stretch',
    ),

    Screen(
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='stretch',
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


@hook.subscribe.startup
def dbus_register():
    id = os.environ.get('DESKTOP_AUTOSTART_ID')
    if not id:
        return
    subprocess.Popen(['dbus-send',
                      '--session',
                      '--print-reply',
                      '--dest=org.gnome.SessionManager',
                      '/org/gnome/SessionManager',
                      'org.gnome.SessionManager.RegisterClient',
                      'string:qtile',
                      'string:' + id])
