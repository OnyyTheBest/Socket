# Esercizio 1 - Contatore messaggi su UDP

In questo esercizio il protocollo UDP viene esteso aggiungendo un contatore lato server: ogni `PING` ricevuto incrementa il numero progressivo riportato nella risposta.

## Obiettivo

Implementare la traccia "message counter":

- il server mantiene un conteggio dei `PING` ricevuti;
- la risposta diventa `PONG #N`;
- il client stampa la risposta completa.

## File presenti

- `utils.py`: funzioni di logging.
- `udp_server.py`: server UDP con contatore progressivo.
- `udp_client.py`: client UDP con timeout e stampa risposta.

## Logica server (`udp_server.py`)

1. Inizializza socket UDP su `127.0.0.1:65432`.
2. Imposta timeout (`settimeout(1.0)`) per non bloccare il ciclo.
3. In `handle_connection()` definisce `cnt = 0`.
4. Ad ogni datagramma:
   - decodifica il messaggio;
   - se il testo e `PING`, incrementa `cnt` e imposta reply `PONG #<cnt>`;
   - altrimenti usa reply `Unknown message: ...`.
5. Invia la risposta al mittente con `sendto(reply, client_addr)`.

Nota importante: il contatore vive in memoria del processo. Se il server viene riavviato, `cnt` riparte da zero.

## Logica client (`udp_client.py`)

1. Crea socket UDP e timeout a 2 secondi.
2. Invia 5 volte `PING`.
3. Per ogni invio:
   - attende `recvfrom`;
   - stampa la stringa ricevuta (es. `PONG #3`);
   - se va in timeout, mostra errore ma continua.
4. Attende `0.5s` tra i tentativi e poi chiude la socket.

## Come eseguire

Aprire due terminali nella cartella `ex1`.

Terminale 1 (server):

```bash
python udp_server.py
```

Terminale 2 (client):

```bash
python udp_client.py
```

## Output atteso

Con server attivo e rete locale stabile:

- invio 1 -> `PONG #1`
- invio 2 -> `PONG #2`
- ...
- invio 5 -> `PONG #5`

## Limiti / osservazioni

- Nessuna persistenza del contatore su file o database.
- Nessuna autenticazione o validazione avanzata del payload.
- Protocollo testuale minimale, sufficiente per lo scopo didattico.
