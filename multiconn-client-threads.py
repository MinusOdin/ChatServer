# multiconn-client-threads.py

import sys
import socket
import types
from _thread import *
import threading 


def receive_messages(sock):
    while True:
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                print("\n", recv_data.decode(), "\n")
            else:
                print("connection closed by server")
                break
        except KeyboardInterrupt:
            print("Caught keyboardinterrupt, exiting")
            break
        except:
            print("closing connection")
            sock.close()
            break

def send_messages(sock):
    out = False
    try:
        msg = input("Enter Name: ")
        if msg:
            sock.send(msg.encode())
    except KeyboardInterrupt:
        print("Caught keyboardinterrupt, exiting")
        out = True
    except:
        print("[ERROR] send, closing connection")
        sock.close()
        out = True

    while True and not out:
        try:
            msg = input("\n")
            if msg:
                sock.send(msg.encode())
        except KeyboardInterrupt:
            print("Caught keyboardinterrupt, exiting")
            break
        except:
            print("[ERROR] send, closing connection")
            sock.close()
            break


host, port = sys.argv[1], int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    receive_thread = threading.Thread(target=receive_messages, args=(s,))
    send_thread = threading.Thread(target=send_messages, args=(s,))

    # Start both threads
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()
