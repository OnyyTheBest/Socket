# Esercizio 3 - Simulazione canale UDP inaffidabile

Questo esercizio implementa la simulazione di perdita pacchetti in UDP, cosi da rendere visibile un comportamento che in localhost normalmente si nota poco.

## Obiettivo

Applicare la traccia "unreliable channel simulation":

- introdurre una probabilita di drop nel server;
- mantenere il client robusto con timeout;
- continuare l'esecuzione anche quando una risposta manca.

## File presenti

- `utils.py`: utility di stampa.
- `udp_server.py`: server UDP con `drop_probability`.
- `udp_client.py`: client UDP con timeout e retry implicito al ping successivo.

## Server (`udp_server.py`)

### Parametri principali

- `host = "127.0.0.1"`
- `port = 65432`
- `drop_probability = 0.3` (30%)

### Flusso

1. Crea socket UDP e fa `bind`.
2. Imposta timeout `1.0s` per evitare blocchi permanenti nel loop.
3. Per ogni datagramma ricevuto:
   - decodifica il messaggio;
   - se il messaggio e `PING`, estrae un numero casuale:
     - se il numero e maggiore di `0.3`, invia `PONG`;
     - altrimenti logga "Dropped reply (simulated loss)" e non risponde.
   - per messaggi diversi da `PING`, invia `Unknown message: ...`.

Il drop simulato impatta solo la risposta del server, non la ricezione del `PING`.

## Client (`udp_client.py`)

1. Crea socket UDP e imposta timeout a `2.0s`.
2. Invia 5 `PING` con `sendto`.
3. Attende risposta con `recvfrom`:
   - se riceve, stampa il payload;
   - se scatta timeout, segnala l'errore e passa al ping successivo.
4. Pausa `0.5s` tra invii e chiusura finale della socket.

Questo comportamento evita crash anche in presenza di perdita pacchetti simulata.

## Come eseguire

Aprire due terminali nella cartella `ex3`.

Server:

```bash
python udp_server.py
```

Client:

```bash
python udp_client.py
```

## Risultato atteso

In media, con 5 invii e drop al 30%:

- alcune richieste ricevono `PONG`;
- alcune vanno in timeout lato client.

Il pattern esatto cambia ad ogni esecuzione perche basato su random.

## Spunti didattici

- UDP non garantisce consegna, ordine o ritrasmissione.
- Il timeout lato client e essenziale in protocolli non affidabili.
- Simulare la perdita in locale e utile per testare handling errori prima di ambienti reali.
