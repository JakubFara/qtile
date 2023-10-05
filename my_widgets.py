from qtile_extras import widget
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple
import subprocess
import datetime
import string
import dateutil.parser
from icons import ICONS


class MyVolume(widget.Volume):
    def _update_drawer(self):
        if self.theme_path:
            self.drawer.clear(self.background or self.bar.background)
            if self.volume <= 0:
                img_name = "audio-volume-muted"
            elif self.volume <= 30:
                img_name = "audio-volume-low"
            elif self.volume < 80:
                img_name = "audio-volume-medium"
            else:  # self.volume >= 80:
                img_name = "audio-volume-high"

            self.drawer.ctx.set_source(self.surfaces[img_name])
            self.drawer.ctx.paint()

        elif self.emoji:
            self.emoji_list = [
                ICONS["volume_0"],
                ICONS["volume_1"],
                ICONS["volume_2"],
                ICONS["volume_3"],
            ]
            emoji_offset = [1, 0, 0, 0]
            if self.volume <= 0:
                emoji = self.emoji_list[0]
                offset = emoji_offset[0]
            elif self.volume <= 30:
                emoji = self.emoji_list[1]
                offset = emoji_offset[1]
            elif self.volume < 80:
                emoji = self.emoji_list[2]
                offset = emoji_offset[2]
            elif self.volume >= 80:
                emoji = self.emoji_list[3]
                offset = emoji_offset[3]
            if self.volume == -1:
                text = f"   {ICONS['cross']}  "
            else:
                text = f"{self.volume}%"
            self.text = f"{emoji}"
            self.text = self.text
        else:
            if self.volume == -1:
                self.text = f" {ICONS['cross']}  "
            else:
                self.text = "{}%".format(self.volume)


class MyCalendar(widget.KhalCalendar):
    def poll(self):
        # get today
        now = datetime.datetime.now()
        # icon = "\U0001f4c5"
        # icon = "\U0001f5d3"
        icon = ICONS["calendar"]
        return f"{icon}" + f"{now}".split(" ")[0].replace("-", "/")


@unique
class BatteryState(Enum):
    CHARGING = 1
    DISCHARGING = 2
    FULL = 3
    EMPTY = 4
    UNKNOWN = 5

BatteryStatus = NamedTuple(
    "BatteryStatus",
    [
        ("state", BatteryState),
        ("percent", float),
        ("power", float),
        ("time", int),
    ],
)

class MyBattery(widget.Battery):
    def build_string(self, status: BatteryStatus) -> str:
        if self.hide_threshold is not None and status.percent > self.hide_threshold:
            return ""
        if self.layout is not None:
            if status.state == BatteryState.DISCHARGING and status.percent < self.low_percentage:
                self.layout.colour = self.low_foreground
                self.background = self.low_background
            else:
                self.layout.colour = self.foreground
                self.background = self.normal_background

        if status.state == BatteryState.CHARGING:
            char = self.charge_char
            return " ".format(
                char=char, percent=status.percent, watt=status.power, hour=hour, min=minute
            )
        elif status.state == BatteryState.DISCHARGING:
            char = self.discharge_char
        # elif status.state == BatteryState.FULL:
            # if self.show_short_text:
            #     return "Full"
            # char = self.full_char
        elif status.state == BatteryState.EMPTY or (
            status.state == BatteryState.UNKNOWN and status.percent == 0
        ):
            if self.show_short_text:
                return "Empty"
            char = self.empty_char
        else:
            char = self.unknown_char

        hour = status.time // 3600
        minute = (status.time // 60) % 60

        if status.percent < 0.1:
            fmt = ICONS["battery_0"] + " {percent:2.0%}"
        elif status.percent < 0.3:
            fmt = ICONS["battery_1"] + " {percent:2.0%}"
        elif status.percent < 0.6:
            fmt = ICONS["battery_2"] + " {percent:2.0%}"
        elif status.percent < 0.9:
            fmt = ICONS["battery_3"] + " {percent:2.0%}"
        else:
            fmt = ICONS["battery_4"] + " {percent:2.0%}"
        return fmt.format(
            char=char, percent=status.percent, watt=status.power, hour=hour, min=minute
        )
