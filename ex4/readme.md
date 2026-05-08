# Esercizio 4 - Scambio messaggi custom: ricerca brani YouTube Music

Questo esercizio realizza un protocollo applicativo personalizzato client-server su TCP.  
Il server riceve richieste JSON dal client, effettua una ricerca su YouTube Music e restituisce metadati del primo risultato.

## Obiettivo della soluzione

Implementare uno scenario reale di richiesta/risposta, con:

- protocollo di trasporto TCP;
- formato messaggi JSON;
- comandi applicativi (`search`, `quit`);
- gestione base di input non validi tramite blocchi `try/except` lato client.

## File presenti

- `utils.py`: logging.
- `tcp_server.py`: server TCP con API testuale JSON.
- `tcp_client.py`: client interattivo da terminale e download con `yt_dlp`.
- `test.py`: script separato per test della ricerca con `innertube`.

## Protocollo applicativo

### Trasporto

- TCP su `127.0.0.1:65432`.

Motivazione: scambio richiesta/risposta dove e preferibile affidabilita della consegna rispetto alla minima latenza.

### Formato messaggi

JSON UTF-8, esempio:

- Richiesta ricerca:
  - `{"activity": "search", "query": "nome canzone"}`
- Chiusura:
  - `{"activity": "quit"}`
- Risposta successo:
  - `{"status": "success", "result": {"song_name": "...", "song_author": "...", "song_video_id": "..."}}`

## Funzionamento server (`tcp_server.py`)

1. Avvio socket TCP (`bind`, `listen`, `accept`).
2. Ciclo di ricezione:
   - deserializza il JSON ricevuto;
   - se `activity == "quit"` chiude la sessione client;
   - se `activity == "search"`:
     - usa `InnerTube("WEB_REMIX")` per cercare brani;
     - filtra i risultati e costruisce oggetti metadata;
     - prende il primo elemento della lista e lo invia in risposta JSON.
3. Alla fine chiude la connessione.

## Funzionamento client (`tcp_client.py`)

1. Connessione TCP al server.
2. Menu interattivo:
   - `0`: inserisce query e invia richiesta `search`;
   - `1`: invia `quit` e termina.
3. Dopo la risposta server:
   - mostra nome/autore del brano trovato;
   - chiede conferma utente;
   - se confermato, costruisce URL `https://music.youtube.com/watch?v=<video_id>` e scarica audio con `yt_dlp`.

## Dipendenze

Oltre alla libreria standard Python, questo esercizio usa:

- `innertube`
- `yt_dlp`

Installazione tipica:

```bash
pip install innertube yt-dlp
```

## Come eseguire

Aprire due terminali nella cartella `ex4`.

Server:

```bash
python tcp_server.py
```

Client:

```bash
python tcp_client.py
```

## Gestione errori e limiti attuali

- Il server non valida in modo robusto JSON malformato (un input non valido puo generare eccezioni non gestite).
- Il server assume che la ricerca ritorni almeno un risultato (`[0]`), quindi query senza risultati possono causare errore.
- Il protocollo non prevede codici errore strutturati lato server.
- `tcp_client.py` stampa un messaggio finale ("All pings sent") ereditato dagli esercizi precedenti, non coerente con il dominio attuale.

## Note su `test.py`

`test.py` serve come script sperimentale: interroga YouTube Music via `innertube` e stampa il JSON dei risultati trovati. E utile per capire e verificare il parsing dei metadati usato poi nel server.
