#!/usr/bin/python
#coding: utf-8

import os
import sys
import time
import subprocess

kill_log = open("/tmp/killed-%s.txt" % time.strftime("%Y%m%d"), "w")
#kill_log = sys.stdout

ps = subprocess.check_output(["ps", "-axo", "pid,rss,user,cmd", "-k-rss", "--no-headers"])

kill_list = []

i = 0
for line in ps.split("\n"):
    i += 1
    try:
        pid, rss, user, cmd = line.strip().split(None, 3)
    except:
        # ps would produce empty lines
        print >>kill_log, 'Skip line %d: "%s"' % (i, line.strip())
        continue

    pid, rss, user, cmd = line.strip().split(None, 3)

    if user in ["root"]:
        continue

    if int(rss) <= 2 * 1024 * 1024: # 2GB
        continue

    kill_list.append([pid, rss, user, cmd])
    if len(kill_list) == 10:
        break

print >>kill_log, ["pid", "rss", "user", "cmd"]
for row in kill_list:
    print >>kill_log, row

    #cmd = "kill -int %s" % (row[0])
    # some processes like jupyter wouldn't quit on receiving SIGINT
    cmd = "kill %s" % (row[0])
    print >>kill_log, "    > " + cmd

    os.system(cmd)