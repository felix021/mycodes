#!/bin/bash

# crontab: 0 4 * * * /root/kill-top10-process.sh

set -e

file=/tmp/killed-`date +%Y%m%d`.txt

# with header, so should keep 11 lines
ps -axo pid,rss,user,cmd -k-rss | head -n 11 > $file

for pid in `tail -n +2 $file | awk '{print $1}'`; do
        echo $pid

        kill -int $pid
        sleep 30
        kill -kill $pid
done