#!/usr/bin/env sh

# Systemd-managed stuff for niri

systemctl --user add-wants niri.service dunst.service
systemctl --user add-wants niri.service waybar.service
systemctl --user add-wants niri.service swaybg.service
systemctl --user add-wants niri.service swayidle.service
