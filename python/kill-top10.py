#!/usr/bin/python
#coding: utf-8

import os
import time
import subprocess

ps = subprocess.check_output(["ps", "-axo", "pid,rss,user,cmd", "-k-rss", "--no-headers"])

kill_list = []

for line in ps.split("\n"):
    pid, rss, user, cmd = line.strip().split(None, 3)

    if user in ["root"]:
        continue

    if int(rss) <= 2 * 1024 * 1024: # 2GB
        continue

    kill_list.append([pid, rss, user, cmd])
    if len(kill_list) == 10:
        break

kill_log = open("/tmp/killed-%s.txt" % time.strftime("%Y%m%d"), "w")
print >>kill_log, ["pid", "rss", "user", "cmd"]
for row in kill_list:
    print >>kill_log, row
    cmd = "kill -int %s" % (row[0])
    os.system(cmd)