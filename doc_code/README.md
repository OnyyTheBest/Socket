# Python Socket Examples — TCP & UDP

A set of educational scripts that demonstrate how network communication works at the socket level in Python. The examples implement a simple **ping-pong** protocol: the client sends `"PING"`, the server replies `"PONG"`.

---

## Diagrams

This repository is accompanied by a set of diagrams whose purpose is to give a detailed visual explanation of how each protocol works internally. Rather than reading a wall of text, you can follow the communication flow step by step: which party speaks first, what happens at each stage of a TCP handshake, how a UDP datagram travels independently from sender to receiver, and why the two models behave so differently in practice.

Each diagram maps directly onto the corresponding source file. The TCP flow diagram shows the full sequence from `bind()` through `accept()` down to the `close()` / FIN teardown, so you can read the code and the diagram side by side. The UDP flow diagram highlights the absence of a handshake and illustrates why `recvfrom()` must return the sender's address — there is no connection object to ask. The TCP vs UDP comparison diagram brings both models onto the same canvas so the structural differences are immediately obvious at a glance.

Use the diagrams as a reference while studying the code, not as a replacement for reading it. Every detail shown visually has a corresponding line in the source with a comment that explains it.

---

## Files

| File | Protocol | Role |
|---|---|---|
| `tcp_server.py` | TCP | Waits for a connection, then echoes `PONG` to every `PING` |
| `tcp_client.py` | TCP | Connects and sends `PING` five times |
| `udp_server.py` | UDP | Waits for datagrams, replies `PONG` to each `PING` |
| `udp_client.py` | UDP | Sends `PING` five times as independent datagrams |

---

## Requirements

- Python 3.6 or later
- No third-party packages — only the standard library (`socket`, `time`)

---

## How to run

Each example requires **two terminals open at the same time**: one for the server and one for the client. Always start the server first.

### TCP

```bash
# Terminal 1 — start the server first
python tcp_server.py

# Terminal 2 — then run the client
python tcp_client.py
```

### UDP

```bash
# Terminal 1
python udp_server.py

# Terminal 2
python udp_client.py
```

The TCP server exits automatically after the client disconnects. The UDP server runs until you press `Ctrl+C`.

---

## TCP vs UDP — key differences

This table summarises what the code makes concrete.

| | TCP (`SOCK_STREAM`) | UDP (`SOCK_DGRAM`) |
|---|---|---|
| Connection | Three-way handshake required | None — fire and forget |
| Server setup | `bind` → `listen` → `accept` | `bind` only |
| Client setup | `connect` | None |
| Send | `sendall(data)` | `sendto(data, address)` |
| Receive | `recv(n)` | `recvfrom(n)` → returns data + sender address |
| Delivery guarantee | Yes — TCP retransmits lost packets | No — datagrams may be lost or reordered |
| Teardown | `close()` sends FIN/ACK | `close()` releases the local file descriptor only |
| Typical use cases | HTTP, SSH, databases | DNS, video streaming, online games |

### Why `recvfrom` instead of `recv`?

In UDP there is no persistent connection, so the socket has no memory of who sent the last datagram. `recvfrom()` solves this by returning the sender's `(ip, port)` address alongside the data. The server then passes that address to `sendto()` to know where to direct the reply.

### Why `settimeout` in the UDP client?

TCP guarantees delivery, so `recv()` will only return once data has arrived. UDP offers no such guarantee: a datagram can be lost silently. Without a timeout, `recvfrom()` would block forever if the server is unreachable or the packet is dropped. The two-second timeout converts an infinite hang into a catchable `socket.timeout` exception.

---

## Exercises

### Exercise 0 - rewrite the code

Modify the proposed code by using functions as much as possible.
Optimize the code as much as possible, explaining the rationale of any modifications.

### Exercise 1 — message counter

Extend the UDP server so that it keeps a running count of how many `PING` datagrams it has received. Each `PONG` reply should include that count, for example `"PONG #3"`. Update the client to print the full reply string so the counter is visible.

Things to think about: where do you store the counter variable? What happens to the count if you restart the server while the client is still running?

### Exercise 2 — multi-client TCP server

The current TCP server handles exactly one client and then exits. Modify it so that it can serve multiple clients **one after another** (sequential, not parallel): after a client disconnects, the server should go back to calling `accept()` and wait for the next one. Add a `server_running` flag or a maximum number of clients so the server still has a clean way to stop.

As a bonus challenge, use Python's `threading` module to handle multiple clients **at the same time**: each call to `accept()` should spawn a new `Thread` that handles that client, while the main thread immediately goes back to `accept()`.

### Exercise 3 — unreliable channel simulation

UDP gives you no delivery guarantee, but on localhost packets are almost never lost. Simulate an unreliable network by adding a `DROP_PROBABILITY` constant (e.g. `0.3` for 30%) to the UDP server. Before sending each `PONG`, draw a random number with `random.random()`; if it is below `DROP_PROBABILITY`, skip the `sendto()` call and print `"[Server] Dropped reply (simulated loss)"` instead.

On the client side, make sure the `socket.timeout` handler prints a meaningful message and that the client continues to the next ping rather than crashing. Observe how the timeout mechanism becomes essential once packet loss is introduced.

### Exercise 4 - custom messages exchange implementation

Choose any real-world interaction that involves two parties sending data back and forth and implement it as a socket program. The choice is entirely yours: a simple calculator where the client sends an arithmetic expression and the server evaluates it and returns the result, a guessing game where the server picks a secret number and the client sends guesses until it wins, a key-value store where the client can send `SET name Alice` and `GET name` commands, a mini chat where two terminals exchange free-form text messages, or anything else you find interesting.
 
Before writing any code, answer these questions in a comment block at the top of each file: what is the protocol — TCP or UDP, and why did you choose it for this exchange? What is the exact format of the messages (plain text, comma-separated fields, JSON)? What happens if the client sends a malformed message? Is there a termination condition, and if so, who initiates it?
 
The goal is not to build something complex, but to go through the full design loop — defining a mini-protocol, implementing both sides from scratch, and handling at least one error case — without a template to follow.

---

## Further reading

- [Python `socket` module documentation](https://docs.python.org/3/library/socket.html)
- [RFC 793 — Transmission Control Protocol](https://www.rfc-editor.org/rfc/rfc793)
- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768)