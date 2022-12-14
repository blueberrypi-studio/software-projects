import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

HOST = "0.0.0.0"
PORT = 2000
SOCKETS = []

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    # print(CONNECTIONS)
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if sock not in SOCKETS:
        SOCKETS.append(sock)
        print(len(SOCKETS))
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            SOCKETS.remove(sock)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            for socket in SOCKETS:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = socket.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]

        
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
    for s in SOCKETS:
        s.close()
finally:
    sel.close()

    

