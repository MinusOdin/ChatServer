# multiconn-client-sel.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

def read(key, mask):
    try:
        sock = key.fileobj
        recv_data = sock.recv(1024)
        if recv_data:
            print("received", repr(recv_data), "from connection")
        else:
            print("closing connection")
            sel.unregister(sock)
            sock.close()
    except:
        print("closing connection")
        sel.unregister(sock)
        sock.close()

def write(sock):
    msg = input("You: ")
    if msg:
        sock.send(msg.encode())

host, port = sys.argv[1], int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, read)
    print("Connected to server")
    write(s)
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            print("key:", key)
            callback = key.data
            callback(key, mask)
        write(s)
