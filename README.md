# Sistema di Gestione Didattica - Terza Liceo Scientifico

Applicazione web completa per la gestione della didattica di una classe terza del liceo scientifico.

## Caratteristiche

### Funzionalità Principali

- **Gestione Studenti**: Anagrafica completa degli studenti della classe
- **Gestione Materie**: Database delle materie del liceo scientifico con docenti e ore settimanali
- **Registro Voti**: Sistema completo per la registrazione e consultazione dei voti
- **Registro Presenze**: Tracciamento di presenze, assenze, ritardi e uscite anticipate
- **Compiti e Verifiche**: Calendario e gestione di compiti, verifiche scritte e orali
- **Materiale Didattico**: Repository di materiali didattici organizzati per materia

### Materie Tipiche del Terzo Anno

- Matematica
- Fisica
- Italiano
- Latino
- Inglese
- Filosofia
- Storia
- Scienze Naturali
- Disegno e Storia dell'Arte
- Educazione Fisica

## Tecnologie Utilizzate

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **ORM**: SQLAlchemy

## Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip (package installer per Python)

### Passi per l'Installazione

1. Clona il repository:
```bash
git clone <repository-url>
cd Mario-Galasso
```

2. Crea un ambiente virtuale (consigliato):
```bash
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione:
```bash
python run.py
```

5. Apri il browser e vai su:
```
http://localhost:5000
```

## Struttura del Progetto

```
Mario-Galasso/
├── app/
│   ├── __init__.py          # Inizializzazione applicazione Flask
│   ├── models.py            # Modelli del database
│   ├── routes.py            # Route API e pagine
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Stili dell'applicazione
│   │   ├── js/
│   │   │   ├── main.js      # Funzioni JavaScript comuni
│   │   │   ├── studenti.js  # Gestione studenti
│   │   │   ├── materie.js   # Gestione materie
│   │   │   ├── voti.js      # Gestione voti
│   │   │   ├── presenze.js  # Gestione presenze
│   │   │   ├── compiti.js   # Gestione compiti
│   │   │   └── materiali.js # Gestione materiali
│   │   └── uploads/         # File caricati
│   └── templates/           # Template HTML
│       ├── base.html        # Template base
│       ├── index.html       # Dashboard
│       ├── studenti.html    # Gestione studenti
│       ├── materie.html     # Gestione materie
│       ├── voti.html        # Registro voti
│       ├── presenze.html    # Registro presenze
│       ├── compiti.html     # Compiti e verifiche
│       └── materiali.html   # Materiale didattico
├── instance/
│   └── didattica.db         # Database SQLite (creato automaticamente)
├── config.py                # Configurazione
├── run.py                   # Script di avvio
├── requirements.txt         # Dipendenze Python
└── README.md               # Documentazione

```

## Utilizzo

### Dashboard

La dashboard mostra una panoramica generale con:
- Numero totale di studenti
- Numero di materie
- Voti registrati
- Compiti da fare
- Media della classe

### Gestione Studenti

- Aggiungi nuovi studenti con informazioni complete
- Modifica dati anagrafici
- Visualizza elenco completo degli studenti
- Elimina studenti (con rimozione di tutti i dati associati)

### Gestione Materie

- Crea materie con nome, descrizione, ore settimanali e docente
- Modifica informazioni delle materie
- Visualizza elenco completo delle materie

### Registro Voti

- Registra voti per studente e materia
- Specifica tipo di valutazione (scritto, orale, pratico, progetto)
- Filtra voti per studente o materia
- Aggiungi note alle valutazioni

### Registro Presenze

- Registra presenza, assenza, ritardo o uscita anticipata
- Specifica se giustificata
- Visualizza storico presenze per studente
- Filtra per data e studente

### Compiti e Verifiche

- Crea compiti, verifiche scritte, verifiche orali o progetti
- Imposta data di scadenza
- Marca compiti come completati
- Visualizza compiti in scadenza con avvisi
- Filtra per materia

### Materiale Didattico

- Carica materiali (dispense, slide, esercizi, link, video)
- Organizza per materia
- Filtra per tipo di materiale
- Aggiungi descrizioni e contenuti

## API REST

L'applicazione espone API REST per tutte le operazioni CRUD:

### Studenti
- `GET /api/studenti` - Lista studenti
- `POST /api/studenti` - Crea studente
- `PUT /api/studenti/<id>` - Aggiorna studente
- `DELETE /api/studenti/<id>` - Elimina studente

### Materie
- `GET /api/materie` - Lista materie
- `POST /api/materie` - Crea materia
- `PUT /api/materie/<id>` - Aggiorna materia
- `DELETE /api/materie/<id>` - Elimina materia

### Voti
- `GET /api/voti` - Lista voti
- `GET /api/voti/studente/<id>` - Voti di uno studente
- `GET /api/voti/materia/<id>` - Voti di una materia
- `POST /api/voti` - Crea voto
- `PUT /api/voti/<id>` - Aggiorna voto
- `DELETE /api/voti/<id>` - Elimina voto

### Presenze
- `GET /api/presenze` - Lista presenze
- `GET /api/presenze/studente/<id>` - Presenze di uno studente
- `POST /api/presenze` - Registra presenza
- `PUT /api/presenze/<id>` - Aggiorna presenza
- `DELETE /api/presenze/<id>` - Elimina presenza

### Compiti
- `GET /api/compiti` - Lista compiti
- `GET /api/compiti/materia/<id>` - Compiti di una materia
- `POST /api/compiti` - Crea compito
- `PUT /api/compiti/<id>` - Aggiorna compito
- `DELETE /api/compiti/<id>` - Elimina compito

### Materiali
- `GET /api/materiali` - Lista materiali
- `GET /api/materiali/materia/<id>` - Materiali di una materia
- `POST /api/materiali` - Crea materiale
- `PUT /api/materiali/<id>` - Aggiorna materiale
- `DELETE /api/materiali/<id>` - Elimina materiale

### Statistiche
- `GET /api/statistiche` - Statistiche generali

## Sicurezza

**IMPORTANTE**: Questa è un'applicazione di esempio per uso didattico. Per l'uso in produzione, considera:

- Implementare autenticazione e autorizzazione
- Utilizzare HTTPS
- Validare e sanitizzare tutti gli input
- Implementare rate limiting
- Gestire backup regolari del database
- Configurare correttamente le variabili d'ambiente

## Contributi

Sentiti libero di contribuire al progetto:

1. Fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## Licenza

Questo progetto è distribuito sotto licenza MIT.

## Autore

Mario Galasso

## Supporto

Per domande o problemi, apri una issue nel repository.
