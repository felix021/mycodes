#!/usr/bin/env python
#coding: cp936
# -- on Unix/Linux, change cp936 to utf-8 -- #
# -- Python 2.7+ -- #

import os
import sys
import hashlib

def hashfile(hash_class, f):
    hasher = hash_class()
    while True:
        buf = f.read(4096)
        hasher.update(buf)
        if len(buf) < 4096:
            break
    for line in f:
        hasher.update(line)
    return hasher.hexdigest()

def process(hash_result, dirname, fnames):
    print >>sys.stderr, "Processing %s..." % dirname
    for fname in fnames:
        fullpath = dirname + '/' + fname
        if os.path.isdir(fullpath):
            continue
        try:
            f = open(fullpath, 'rb')
        except IOError:
            print >>sys.stderr, "can't open %s" % fullpath
            continue
        digest = hashfile(hashlib.sha1, f)
        if digest not in hash_result:
            hash_result[digest] = []
        hash_result[digest].append(fullpath)

hash_result = {}
os.path.walk(sys.argv[1], process, hash_result)

print "\n=== RESULT ===\n"
for digest, fnames in hash_result.iteritems():
    if len(fnames) == 1:
        continue
    print digest
    for f in fnames:
        print '   ', f
