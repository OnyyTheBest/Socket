"""
UDP Client — Ping Pong (educational example)

Author  : Pietro Boccadoro
Email   : pieroboccadoro13[at]gmail[dot]com
Date    : 2024-04-11
Version : 1.0

Key differences from TCP:
  - SOCK_DGRAM instead of SOCK_STREAM  →  UDP, connectionless
  - No connect()                        →  we never "establish" a connection
  - sendto()   instead of sendall()    →  destination address supplied per datagram
  - recvfrom() instead of recv()       →  also returns the sender's address
  - No close() is strictly required    →  but we call it anyway to release the file descriptor
"""

import socket   # standard library module for networking
import time     # used for time.sleep() to pace the pings


HOST = "127.0.0.1"  # address of the server we want to send datagrams to
PORT = 65433        # port the server is bound to — must match udp_server.py

# Maximum number of bytes we expect to receive in a single reply datagram
BUFFER_SIZE = 1024


def main():

    # ── Create the socket ────────────────────────────────────────────────────────
    # AF_INET    → IPv4
    # SOCK_DGRAM → UDP — no connection, no delivery guarantee, no ordering
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout of 2 seconds on blocking socket operations (recvfrom).
    # Without this, recvfrom() would block forever if the server never replies,
    # or if the datagram is lost on the network.
    # After the timeout, recvfrom() raises socket.timeout instead of hanging.
    sock.settimeout(2.0)

    # Confirm that the socket is ready
    print(f"[Client] UDP socket ready. Will send to {HOST}:{PORT}\n")

    # ── Ping-pong loop ───────────────────────────────────────────────────────────
    for i in range(1, 6):   # send 5 pings

        message = "PING"    # payload we want to send

        # Log what we are about to send
        print(f"[Client] Send #{i}: {message!r}")

        # sendto() transmits one datagram.
        # Arguments:
        #   1. The payload encoded as bytes (the network cannot carry Python strings).
        #   2. The destination as a (host, port) tuple — required every time
        #      because UDP has no persistent connection to remember the destination.
        sock.sendto(message.encode("utf-8"), (HOST, PORT))

        # Try to receive the server's reply
        try:
            # recvfrom() blocks until a datagram arrives or the timeout expires.
            # Returns:
            #   data        → the bytes of the reply datagram
            #   server_addr → (ip, port) of the sender (useful to verify it's our server)
            data, server_addr = sock.recvfrom(BUFFER_SIZE)

            # Decode the reply bytes to a string
            reply = data.decode("utf-8")

            # Log the reply and where it came from
            print(f"[Client] Reply from {server_addr}: {reply!r}")

        except socket.timeout:
            # The server did not reply within 2 seconds.
            # This can happen because UDP offers NO delivery guarantee:
            #   - the datagram may have been lost in transit (unlikely on localhost)
            #   - the server may be down or not yet running
            print(f"[Client] Timeout — no reply received for ping #{i}")

        # Small pause between pings so the output is easy to read
        time.sleep(0.5)

    # ── Teardown ─────────────────────────────────────────────────────────────────
    print("\n[Client] Done. Closing socket.")

    # Release the OS file descriptor associated with this socket.
    # For UDP there is no FIN/ACK exchange — the socket simply disappears locally.
    sock.close()


# Only execute main() when the script is run directly
if __name__ == "__main__":
    main()