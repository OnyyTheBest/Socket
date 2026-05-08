# Esercizio 2 - Server TCP multi-client (sequenziale e con thread)

Questo esercizio estende il server TCP base per supportare piu client. Sono incluse due varianti:

- gestione sequenziale (`tcp_server.py`);
- gestione concorrente tramite thread (`tcp_server_threads.py`).

## Obiettivo

Rispettare la traccia "multi-client TCP server":

- dopo la disconnessione di un client, il server torna in `accept()`;
- il server resta in esecuzione fino a interruzione manuale;
- bonus: versione parallelizzata con `threading`.

## File presenti

- `utils.py`: logging comune.
- `tcp_client.py`: client che invia molti `PING` (49 iterazioni nel codice attuale).
- `tcp_server.py`: server multi-client sequenziale.
- `tcp_server_threads.py`: server multi-client concorrente con thread.

## Versione sequenziale (`tcp_server.py`)

### Avvio

1. Crea socket TCP e abilita `SO_REUSEADDR`.
2. `bind` su `127.0.0.1:65432`.
3. `listen(1)` e `settimeout(1.0)`.

### Gestione client

- Il `main` contiene un `while True` che richiama continuamente `handle_connection()`.
- `handle_connection()` tenta `accept()`:
  - su timeout ritorna al chiamante;
  - su connessione attiva entra nel ciclo `recv/send`.
- Per ogni messaggio:
  - `PING` -> `PONG`
  - altro testo -> `Unknown message: ...`
- Alla disconnessione del client (`recv` vuoto) chiude `conn` e il server torna ad accettare nuovi client.

Questa modalita gestisce un client per volta.

## Versione con thread (`tcp_server_threads.py`)

Stesso setup socket iniziale, ma cambia la strategia di gestione:

1. Ogni `accept()` crea un `Thread` con target `handle_q_a(conn)`.
2. Il thread gestisce il ciclo `recv/send` del singolo client.
3. Il thread viene aggiunto a `threadList`.
4. Il thread principale torna subito in `accept()` e puo accettare altri client contemporaneamente.

Alla chiusura (`Ctrl+C`), il programma fa `join()` sui thread raccolti e poi chiude la socket server.

## Client (`tcp_client.py`)

- Connessione TCP a `127.0.0.1:65432`.
- Invio di `PING` in loop da 1 a 49 con pausa `0.5s`.
- Ricezione e stampa di ogni risposta.
- Chiusura della connessione al termine.

Per testare concorrenza reale della versione threaded, avviare piu processi client in parallelo.

## Come eseguire

Aprire due o piu terminali nella cartella `ex2`.

### Test server sequenziale

Terminale 1:

```bash
python tcp_server.py
```

Terminale 2:

```bash
python tcp_client.py
```

### Test server con thread

Terminale 1:

```bash
python tcp_server_threads.py
```

Terminale 2, 3, ...:

```bash
python tcp_client.py
```

## Cosa osservare

- Con `tcp_server.py` i client vengono serviti uno alla volta.
- Con `tcp_server_threads.py` i client possono essere serviti in contemporanea.
- In entrambe le versioni la logica applicativa del protocollo resta invariata (`PING` -> `PONG`).
