#!/usr/bin/python

import socket
import os
import thread
import pty

shell = "/bin/bash"
tty = open("/dev/tty", "w")

shell_input_reader, shell_input_writer = os.pipe()
shell_output_reader, shell_output_writer = os.pipe()

def sheller(arg):
    global shell, shell_input_reader, shell_output_writer
    os.dup2(shell_input_reader, 0)
    os.dup2(shell_output_writer, 1)
    os.dup2(shell_output_writer, 2)
    while True:
        pty.spawn('/bin/bash')

def shell_to_sock(conn):
    global shell_output_reader
    while True:
        try:
            conn.send(os.read(shell_output_reader, 1024))
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 4698))

sock.listen(5)

thread.start_new_thread(sheller, (1,))

while True:
    conn, addr = sock.accept()
    print >>tty, "%s:%d connected" % (addr[0], addr[1])
    thread.start_new_thread(shell_to_sock, (conn, ))

    while True:
        try:
            buf = conn.recv(1024)
            if not buf:
                break
            print >>tty, "[%s]" % buf.strip()
            os.write(shell_input_writer, buf)
        except:
            break

    conn.close()

