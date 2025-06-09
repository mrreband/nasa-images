#!/bin/bash

WALLPAPER1="/Users/mr/repos/nasa-images/python/images/spanned/wallpaper_monitor_1.png"
WALLPAPER2="/Users/mr/repos/nasa-images/python/images/spanned/wallpaper_monitor_2.png"

osascript -e 'tell application "System Events" to tell desktop 1 to set picture to "'"$WALLPAPER1"'"'
osascript -e 'tell application "System Events" to tell desktop 2 to set picture to "'"$WALLPAPER2"'"'

