"""
TCP Server — Ping Pong (educational example)
Waits for a client to connect, then replies "PONG" to every "PING" received.

Author  : Pietro Boccadoro
Email   : pieroboccadoro13[at]gmail[dot]com
Date    : 2024-04-11
Version : 1.0

Key steps in a TCP client:
    1. Create a socket (socket.socket)
    2. Connect to the server (socket.connect)
    3. Send and receive data (socket.sendall, socket.recv)
    4. Close the connection (socket.close)
Note: Run tcp_server.py in one terminal before running tcp_client.py in another terminal.
"""

import socket   # standard library module that provides low-level networking interfaces


HOST = "127.0.0.1"  # loopback address — only accepts connections from this same machine
PORT = 65432        # port number to listen on; values > 1024 don't need root/admin rights


def main():

    # ── Create the socket ────────────────────────────────────────────────────────
    # AF_INET     → use IPv4 addresses (use AF_INET6 for IPv6)
    # SOCK_STREAM → use TCP, which is connection-oriented and guarantees delivery
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tell the OS to reuse this port immediately after the program exits.
    # Without this option, you would get "Address already in use" on quick restarts
    # because the OS keeps the port in TIME_WAIT state for ~60 seconds.
    # SOL_SOCKET  → the option applies to the socket layer itself
    # SO_REUSEADDR → allow reuse of a local address/port that is still in TIME_WAIT
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # ── Bind ─────────────────────────────────────────────────────────────────────
    # Associate the socket with a specific network interface (HOST) and port (PORT).
    # After this call the OS knows to deliver incoming packets on PORT to this socket.
    server_sock.bind((HOST, PORT))

    # ── Listen ───────────────────────────────────────────────────────────────────
    # Switch the socket to "passive" mode so it can accept incoming connections.
    # The argument (1) is the backlog — max number of connections waiting in the
    # kernel queue before new ones are refused with "Connection refused".
    server_sock.listen(1)

    # Confirm that the server started and is ready
    print(f"[Server] Listening on {HOST}:{PORT} ...")

    # ── Accept ───────────────────────────────────────────────────────────────────
    # Block here until a client completes the TCP three-way handshake (SYN / SYN-ACK / ACK).
    # Returns two objects:
    #   conn → a brand-new socket object dedicated to THIS single client connection
    #   addr → a (ip_address, port_number) tuple that identifies the remote client
    conn, addr = server_sock.accept()

    # Log the client's address so we know who connected
    print(f"[Server] Connection accepted from {addr}")

    # ── Communication loop ───────────────────────────────────────────────────────
    # Keep reading messages until the client closes the connection
    while True:

        # Read up to 1024 bytes from the client.
        # recv() blocks (pauses execution) until data arrives or the connection closes.
        # 1024 is the maximum number of bytes we want to read in one call.
        data = conn.recv(1024)

        # recv() returns an empty bytes object b"" when the remote side
        # closes the connection — that is our signal to stop the loop
        if not data:
            print("[Server] Client closed the connection.")
            break   # exit the while loop

        # Convert the raw bytes to a Python string using the UTF-8 encoding.
        # strip() removes any leading/trailing whitespace or newline characters.
        message = data.decode("utf-8").strip()

        # Print the received message for inspection
        print(f"[Server] Received: {message!r}")

        # Decide what reply to send based on the message content
        if message == "PING":
            reply = "PONG"                      # correct response to a PING
        else:
            reply = f"Unknown message: {message!r}"  # anything else gets an informative error

        # Encode the reply string back to bytes (the network only transports bytes)
        # and send every single byte to the client.
        # sendall() retries internally if the OS only accepts part of the data at once,
        # unlike send() which may silently send fewer bytes than requested.
        conn.sendall(reply.encode("utf-8"))

        # Log what we sent
        print(f"[Server] Sent:     {reply!r}")

    # ── Teardown ─────────────────────────────────────────────────────────────────
    # Close the per-client connection socket (sends a FIN packet, releases OS resources)
    conn.close()

    # Close the main listening socket (the server will no longer accept new connections)
    server_sock.close()


# Only execute main() when this file is run directly (e.g. "python tcp_server.py").
# If another script imports this file, main() will NOT run automatically.
if __name__ == "__main__":
    main()