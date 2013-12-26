#!/usr/bin/env python
#coding:utf-8

"""
author: Felix021
date: 2013-12-26

This useless library is written to be included in a long running process,
thus to get a python shell and probe into the process in a pythonic way...

Here's another useless script, which executes a python script as if it's run
in an interactive interpreter:
    MagicPython @ https://gist.github.com/felix021/8021106

"""

import sys
import compiler
import thread

def thread_interpreter(globals_dict, locals_dict):
    thread.start_new_thread(interpreter, (globals_dict, locals_dict))

def interpreter(globals_dict, locals_dict):
    while True:
        block = []
        first_line = True
        while True:
            if first_line:
                sys.stdout.write('>>> ')
                first_line = False
            else:
                sys.stdout.write('... ')
            line = sys.stdin.readline()
            block.append(line)
            line = line.rstrip()
            if line.startswith('\t') or line.startswith(' ') \
               or line.endswith(':') or line.endswith('\\'):
                continue
            else:
                break
        code = ''.join(block)
        if code == '':
            break
        try:
            stmt = compiler.parse(code).getChildNodes()[0].getChildNodes()[0]
        except:
            stmt = None
        if isinstance(stmt, compiler.ast.Discard):
            code = '____ret = ' + code
        try:
            exec(code, globals_dict, locals_dict)
            if isinstance(stmt, compiler.ast.Discard):
                print locals_dict['____ret']
        except Exception, e:
            print """Traceback (most recent call last): \n  File "<stdin>", line 1, in <module>"""
            print '%s: %s' % (e.__class__.__name__, e)

if __name__ == "__main__":
    interpreter(globals(), locals())
