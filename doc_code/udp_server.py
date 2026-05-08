"""
UDP Server — Ping Pong (educational example)

Author  : Pietro Boccadoro
Email   : pieroboccadoro13[at]gmail[dot]com
Date    : 2024-04-11
Version : 1.0

Key differences from TCP:
  - SOCK_DGRAM instead of SOCK_STREAM  →  UDP, connectionless
  - No listen() or accept()           →  no connection is ever "established"
  - recvfrom() instead of recv()      →  returns the sender's address with each datagram
  - sendto()   instead of sendall()   →  we must specify the destination every time
  - No close() on a per-client basis  →  there is no per-client socket to close
"""

import socket   # standard library module for networking


HOST = "127.0.0.1"  # loopback address — accept datagrams from this machine only
PORT = 65433        # port to listen on (different from the TCP example to avoid conflicts)


def main():

    # ── Create the socket ────────────────────────────────────────────────────────
    # AF_INET     → IPv4
    # SOCK_DGRAM  → UDP: connectionless, no delivery guarantee, no ordering guarantee.
    #               Each send() produces exactly one independent "datagram" (packet).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ── Bind ─────────────────────────────────────────────────────────────────────
    # Tell the OS to deliver incoming UDP packets on PORT to this socket.
    # Unlike TCP, there is NO listen() call after bind() — UDP has no connection queue.
    sock.bind((HOST, PORT))

    # Confirm the server is ready
    print(f"[Server] Listening for UDP datagrams on {HOST}:{PORT} ...")
    print("[Server] Press Ctrl+C to stop.\n")

    # ── Main receive loop ────────────────────────────────────────────────────────
    while True:

        # recvfrom() blocks until a datagram arrives.
        # It returns TWO values (unlike TCP's recv which returns only bytes):
        #   data        → the raw bytes of the datagram payload
        #   client_addr → a (ip, port) tuple identifying who sent this datagram.
        #                 We MUST save this address so we know where to send the reply.
        # 1024 is the maximum number of bytes we are willing to read from one datagram.
        # If a datagram is larger than 1024 bytes, the excess bytes are silently discarded.
        data, client_addr = sock.recvfrom(1024)

        # Decode the raw bytes to a Python string (UTF-8), stripping whitespace
        message = data.decode("utf-8").strip()

        # Log which client sent the datagram and what it contained
        print(f"[Server] Received {message!r} from {client_addr}")

        # Decide the reply based on the message
        if message == "PING":
            reply = "PONG"
        else:
            reply = f"Unknown: {message!r}"

        # sendto() sends a datagram to a specific address.
        # Unlike TCP's sendall(), we must always provide the destination (client_addr)
        # because UDP is connectionless — the socket has no "current connection" to use.
        # encode() converts the Python string back to bytes for transmission.
        sock.sendto(reply.encode("utf-8"), client_addr)

        # Log the reply
        print(f"[Server] Sent {reply!r} back to {client_addr}\n")


# Run main() only when the file is executed directly
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Catch Ctrl+C so the server exits cleanly without a traceback
        print("\n[Server] Stopped.")