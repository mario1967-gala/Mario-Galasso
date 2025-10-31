# 🚀 Guida Rapida - Avvio Applicazione

## 📍 Dove Si Trovano i File

I file sono nel repository GitHub:
- **Repository**: `mario1967-gala/Mario-Galasso`
- **Branch**: `claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM`

## 💻 Installazione e Avvio

### Opzione 1: Se il Repository è Già Clonato

```bash
# Naviga nella cartella del progetto
cd Mario-Galasso

# Assicurati di essere sul branch corretto
git checkout claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM

# Aggiorna il codice
git pull origin claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM

# Installa le dipendenze Python
pip install -r requirements.txt

# Avvia l'applicazione
python run.py
```

### Opzione 2: Clone da Zero

```bash
# Clona il repository
git clone https://github.com/mario1967-gala/Mario-Galasso.git
cd Mario-Galasso

# Passa al branch corretto
git checkout claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM

# Installa le dipendenze Python
pip install -r requirements.txt

# (Opzionale) Popola il database con dati di esempio
python seed_data.py

# Avvia l'applicazione
python run.py
```

### Opzione 3: Con Virtual Environment (Consigliato)

```bash
# Clona il repository (se non l'hai già fatto)
git clone https://github.com/mario1967-gala/Mario-Galasso.git
cd Mario-Galasso

# Passa al branch corretto
git checkout claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM

# Crea un virtual environment
python3 -m venv venv

# Attiva il virtual environment
# Su Linux/Mac:
source venv/bin/activate
# Su Windows:
# venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# (Opzionale) Popola con dati di esempio
python seed_data.py

# Avvia l'applicazione
python run.py
```

## 🌐 Accesso all'Applicazione

Una volta avviata, apri il browser e vai su:
```
http://localhost:5001
```

o

```
http://127.0.0.1:5001
```

## 📁 Struttura File (Cosa Dovresti Vedere)

```
Mario-Galasso/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── utils.py                    ← NUOVO! (Import studenti)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── studenti.js
│   │   │   ├── materie.js
│   │   │   ├── voti.js
│   │   │   ├── presenze.js
│   │   │   ├── compiti.js
│   │   │   ├── materiali.js
│   │   │   └── import_studenti.js  ← NUOVO!
│   │   └── uploads/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── studenti.html
│       ├── materie.html
│       ├── voti.html
│       ├── presenze.html
│       ├── compiti.html
│       ├── materiali.html
│       └── import_studenti.html     ← NUOVO!
├── instance/
│   └── didattica.db                 (creato automaticamente)
├── config.py
├── run.py                           ← FILE DA ESEGUIRE
├── seed_data.py
├── test_import.py                   ← NUOVO!
├── requirements.txt
├── README.md
├── IMPORT_STUDENTI.md               ← NUOVO!
└── .gitignore
```

## 🔧 Verifica che Tutto Funzioni

```bash
# Verifica che Python sia installato
python --version
# o
python3 --version

# Verifica che i file esistano
ls -la

# Dovresti vedere:
# - run.py
# - requirements.txt
# - app/ (cartella)
# - README.md
```

## ❗ Risoluzione Problemi

### "File non trovati" o "Cartella vuota"

```bash
# Controlla in quale directory sei
pwd

# Dovresti vedere qualcosa come:
# /percorso/Mario-Galasso

# Se non vedi app/, run.py, ecc., sei nella directory sbagliata
# Naviga alla directory corretta
```

### "Comando 'python' non trovato"

Prova con `python3`:
```bash
python3 run.py
```

### "ModuleNotFoundError" o errori di import

Le dipendenze non sono installate:
```bash
pip install -r requirements.txt
# oppure
pip3 install -r requirements.txt
```

### "Porta 5001 già in uso"

Modifica la porta in `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Cambia 5001 in 5002 se necessario
```

## 🎯 Test Veloce

Per verificare che tutto funzioni senza avviare il server:

```bash
# Test 1: Verifica creazione app
python3 -c "from app import create_app; app = create_app(); print('✓ App OK!')"

# Test 2: Verifica import studenti
python3 test_import.py
```

## 📞 Hai Ancora Problemi?

1. Verifica di essere sul branch corretto:
   ```bash
   git branch
   # Dovresti vedere: * claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM
   ```

2. Verifica il contenuto della cartella:
   ```bash
   ls -la app/
   # Dovresti vedere models.py, routes.py, utils.py, ecc.
   ```

3. Controlla il README:
   ```bash
   cat README.md | head -20
   ```

## 🎉 Primo Avvio - Checklist

- [ ] Repository clonato
- [ ] Branch corretto selezionato
- [ ] Dipendenze installate (`pip install -r requirements.txt`)
- [ ] Database popolato (opzionale: `python seed_data.py`)
- [ ] Server avviato (`python run.py`)
- [ ] Browser aperto su `http://localhost:5001`
- [ ] Dashboard visibile

## 📱 Accesso alle Funzionalità

Una volta che vedi la dashboard:

1. **Studenti**: Menu → Studenti
2. **Import da Screenshot**: Studenti → Pulsante "📷 Import da Screenshot"
3. **Materie**: Menu → Materie
4. **Voti**: Menu → Voti
5. **Presenze**: Menu → Presenze
6. **Compiti**: Menu → Compiti
7. **Materiali**: Menu → Materiali

---

**Suggerimento**: La prima volta esegui `python seed_data.py` per popolare il database con dati di esempio (10 studenti, 10 materie, voti, presenze, ecc.). Così puoi esplorare subito tutte le funzionalità!
