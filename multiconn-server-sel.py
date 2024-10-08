import socket
import selectors
import sys
import types

sel = selectors.DefaultSelector()
clients = []

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, handle_client)
    clients.append(conn)

def broadcast_message(sender_socket, message):
    for client in clients:
        if client != sender_socket:  # Don't send the message to the sender itself
            try:
                client.send(message.encode('utf-8'))
            except:
                # Handle broken connections by removing the client
                selector.unregister(client)
                clients.remove(client)
                client.close()

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)  # Receive data from the client
        if data:
            print(f"[CLIENT] {data.decode('utf-8')}")
            broadcast_message(client_socket, data.decode('utf-8'))  # Broadcast the message to all clients
        else:
            print("[DISCONNECTED] Client disconnected.")
            sel.unregister(client_socket)
            clients.remove(client_socket)  # Remove the client from the list
            client_socket.close()
    except:
        print("[ERROR] Issue with client connection.")
        sel.unregister(client_socket)
        clients.remove(client_socket)
        client_socket.close()

host, port = sys.argv[1], int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, accept_wrapper)
    print("[SERVER STARTED] Waiting for connections...")
    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)
    except KeyboardInterrupt:
        print("Caught keyboardinterrupt, exiting")
    finally:
        sel.close()

