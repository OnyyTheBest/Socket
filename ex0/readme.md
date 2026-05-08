# Esercizio 0 - Refactor del ping-pong TCP/UDP

Questo esercizio contiene una riscrittura del classico esempio socket `PING`/`PONG` usando classi e funzioni dedicate, separando la logica di connessione dalla logica applicativa.

## Obiettivo

Dimostrare la comunicazione client-server con:

- TCP (`tcp_server.py`, `tcp_client.py`)
- UDP (`udp_server.py`, `udp_client.py`)

e organizzare il codice in modo piu ordinato rispetto alla versione base.

## File presenti

- `utils.py`: helper di logging (`generate_info`, `generate_warning`, `generate_error`).
- `tcp_server.py`: server TCP che accetta un client e risponde `PONG` ai `PING`.
- `tcp_client.py`: client TCP che invia 5 `PING` e stampa le risposte.
- `udp_server.py`: server UDP che riceve datagrammi e risponde, con simulazione perdita pacchetti.
- `udp_client.py`: client UDP con timeout che invia 5 `PING`.

## Funzionamento TCP

### Server (`tcp_server.py`)

1. Crea socket `AF_INET` + `SOCK_STREAM`.
2. Imposta `SO_REUSEADDR`.
3. Esegue `bind(127.0.0.1, 65432)`.
4. Entra in ascolto con `listen(1)`.
5. Accetta una connessione con `accept()`.
6. Ciclo di ricezione:
   - `recv(1024)`
   - se il messaggio e `PING`, risponde `PONG`
   - altrimenti risponde `Unknown message: ...`
7. Quando il client chiude, termina e chiude la socket.

### Client (`tcp_client.py`)

1. Crea socket TCP.
2. Esegue `connect(127.0.0.1, 65432)`.
3. Invia 5 volte `PING` con `sendall`.
4. Dopo ogni invio legge la risposta con `recv(1024)`.
5. Attende `0.5s` tra un invio e il successivo.
6. Chiude la connessione.

## Funzionamento UDP

### Server (`udp_server.py`)

1. Crea socket `AF_INET` + `SOCK_DGRAM`.
2. Esegue `bind(127.0.0.1, 65432)`.
3. Imposta timeout della socket a 1 secondo (`settimeout(1.0)`), per poter restare reattivo.
4. Riceve datagrammi con `recvfrom(1024)`.
5. Se riceve `PING`, risponde normalmente `PONG`, ma con probabilita `drop_probability = 0.3` simula perdita e non invia nulla.
6. Per messaggi diversi da `PING`, invia `Unknown message: ...`.

### Client (`udp_client.py`)

1. Crea socket UDP.
2. Imposta timeout ricezione a 2 secondi.
3. Invia 5 datagrammi `PING` con `sendto`.
4. Aspetta risposta con `recvfrom(1024)`.
5. Se non arriva nulla entro timeout, stampa errore ma continua con il ping successivo.
6. Chiude la socket al termine.

## Come eseguire

Aprire due terminali nella cartella `ex0`.

### TCP

Terminale 1:

```bash
python tcp_server.py
```

Terminale 2:

```bash
python tcp_client.py
```

### UDP

Terminale 1:

```bash
python udp_server.py
```

Terminale 2:

```bash
python udp_client.py
```

## Cosa osservare

- In TCP le risposte arrivano sempre (a meno di errori di connessione).
- In UDP alcune risposte possono mancare, qui anche per scelta esplicita del server.
- Il timeout lato client UDP e fondamentale per evitare blocchi infiniti.

## Limiti noti

- Host e porta sono hardcoded (`127.0.0.1:65432`).
- Il server TCP gestisce un solo client e poi termina.
- La gestione eccezioni e basilare e in alcuni punti potrebbe essere resa piu precisa.
