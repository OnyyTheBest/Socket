"""
TCP Client — Ping Pong (educational example)
Connects to the server and sends "PING" five times, printing each "PONG" reply.

Author  : Pietro Boccadoro
Email   : pieroboccadoro13[at]gmail[dot]com
Date    : 2024-04-11
Version : 1.0

Key steps in a TCP client:
    1. Create a socket (socket.socket)
    2. Connect to the server (socket.connect)
    3. Send and receive data (socket.sendall, socket.recv)
    4. Close the connection (socket.close)
Note: Run tcp_server.py in one terminal before running this client in another terminal.
"""

import socket   # standard library module for networking
import time     # standard library module; we use time.sleep() to add pauses


HOST = "127.0.0.1"  # address of the server we want to connect to (same machine here)
PORT = 65432        # port the server is listening on — must match tcp_server.py


def main():

    # ── Create the socket ────────────────────────────────────────────────────────
    # AF_INET     → IPv4
    # SOCK_STREAM → TCP (reliable, ordered, connection-based)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ── Connect ──────────────────────────────────────────────────────────────────
    # Initiate the TCP three-way handshake with the server:
    #   1. Client sends SYN
    #   2. Server replies with SYN-ACK
    #   3. Client sends ACK  → connection is now established
    # This call blocks until the handshake completes (or raises an exception on failure).
    client_sock.connect((HOST, PORT))

    # Confirm that we are connected
    print(f"[Client] Connected to {HOST}:{PORT}")

    # ── Ping-pong loop ───────────────────────────────────────────────────────────
    # Send PING five times and wait for a PONG reply each time
    for i in range(1, 6):   # i goes 1, 2, 3, 4, 5

        message = "PING"    # the message we are going to send

        # Log what we are about to send, including the iteration number
        print(f"\n[Client] Send #{i}: {message!r}")

        # Encode the string to bytes (UTF-8) and send all of them.
        # The network layer only transports raw bytes, never Python strings.
        # sendall() ensures every byte is sent even if the OS buffers them in chunks.
        client_sock.sendall(message.encode("utf-8"))

        # Wait for the server's reply.
        # recv(1024) blocks until data arrives, reading at most 1024 bytes.
        data = client_sock.recv(1024)

        # Decode the received bytes back into a human-readable string
        reply = data.decode("utf-8")

        # Print the server's reply
        print(f"[Client] Reply:    {reply!r}")

        # Pause for half a second before the next iteration.
        # This makes the output easier to follow and simulates a realistic interval.
        time.sleep(0.5)

    # ── Teardown ─────────────────────────────────────────────────────────────────
    # Inform the user that we are done
    print("\n[Client] All pings sent. Closing connection.")

    # Close the socket: sends a FIN packet to the server so it knows we are done,
    # then releases the OS resources (file descriptor) associated with the socket.
    client_sock.close()


# Only execute main() when this file is run directly (e.g. "python tcp_client.py").
if __name__ == "__main__":
    main()