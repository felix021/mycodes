#!/bin/bash

source /etc/profile
source ~/.bashrc

# USAGE: register in crontab with "*/10 0 0 0 0"

which AdjustVolume &>/dev/null
if [ $? -eq 1 ]; then
    echo
    echo Please download device-volume-adjuster, unzip AdjustVolume.zip and put the binary to /usr/local/bin/
    echo "  URL: https://github.com/jonomuller/device-volume-adjuster/releases/tag/v1.0.0"
    echo 
    exit 1
fi

ssid=`/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -I | grep ' SSID:' | awk -FSSID:\  '{print $2}'`

if [ "$ssid" == "YOUR WIFI SSID" ]; then
    AdjustVolume -s 0 -n "MacBook Pro Speakers"
fi
echo [`date +"%Y-%m-%d %H:%M:%S"`] [$ssid] done >> /tmp/mute.log