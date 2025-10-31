# 🚀 Istruzioni per Avviare l'Applicazione e Vedere le Nuove Sezioni

## ⚠️ IMPORTANTE: Seguire questi passaggi in ordine

### 1️⃣ Installare le Dipendenze Python

Apri il terminale nella cartella del progetto ed esegui:

```bash
cd /home/user/Mario-Galasso

# Installa tutte le dipendenze necessarie
pip3 install -r requirements.txt
```

**Dipendenze installate:**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Werkzeug 3.0.1
- python-dateutil 2.8.2
- anthropic >= 0.18.0

---

### 2️⃣ Inizializzare il Database

Il database deve essere creato con le nuove tabelle per le verifiche:

```bash
# Esegui lo script di inizializzazione
python3 init_db.py
```

**Output atteso:**
```
Creazione database...
✅ Database creato con successo!

Tabelle create:
  - classi
  - compiti
  - criteri_valutazione
  - domande_verifica
  - materiali
  - materie
  - presenze
  - studenti
  - verifiche
  - voti
```

Se vedi le tabelle `verifiche`, `domande_verifica` e `criteri_valutazione`, il database è pronto! ✅

---

### 3️⃣ Configurare la API Key di Claude (OPZIONALE)

**Solo se vuoi usare il generatore AI di verifiche**, configura la tua API key:

```bash
# Su Linux/Mac
export ANTHROPIC_API_KEY="la-tua-api-key-qui"

# Su Windows
set ANTHROPIC_API_KEY=la-tua-api-key-qui
```

⚠️ **Nota:** Puoi usare l'applicazione senza API key, ma non potrai generare verifiche automaticamente con l'AI.

---

### 4️⃣ Avviare l'Applicazione

```bash
python3 run.py
```

**Output atteso:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5001
Press CTRL+C to quit
```

---

### 5️⃣ Aprire l'Applicazione nel Browser

1. Apri il tuo browser (Chrome, Firefox, Safari, etc.)
2. Vai all'indirizzo: **http://localhost:5001**
3. Nella barra di navigazione in alto dovresti vedere:

```
Dashboard | Studenti | Materie | Voti | Presenze | Compiti | Verifiche | Materiali
```

4. Clicca su **"Verifiche"** per accedere alla nuova sezione! 🎉

---

## 🎯 Come Usare la Sezione Verifiche

### **Opzione 1: Creare una Verifica Manualmente**

1. Clicca sul pulsante **"+ Nuova Verifica"**
2. Compila i campi:
   - Materia
   - Titolo
   - Data verifica
   - Durata (opzionale)
   - Argomenti
3. Clicca **"+ Aggiungi Domanda"**
4. Per ogni domanda:
   - Scrivi il testo della domanda
   - Scegli il tipo (aperta, multipla, vero/falso, esercizio)
   - Assegna il punteggio
   - Clicca **"+ Criterio"** per aggiungere criteri di valutazione
5. Clicca **"Salva Verifica"**

### **Opzione 2: Generare una Verifica con l'AI** (richiede API key)

1. Clicca sul pulsante **"🤖 Genera con AI"**
2. Compila il form:
   - Seleziona la materia
   - Inserisci gli argomenti (es: "Equazioni di secondo grado")
   - Numero di domande (es: 5)
   - Punteggio totale (es: 10)
   - Difficoltà (bassa/media/alta)
   - Tipo domande (aperte/multiple/misto)
3. Clicca **"🤖 Genera Verifica"**
4. L'AI genererà una verifica completa con domande e criteri
5. **Rivedi e modifica** se necessario
6. Clicca **"Salva Verifica"**

---

## 🔍 Verificare che Tutto Funzioni

### Checklist ✅

- [ ] Dipendenze installate (`pip3 install -r requirements.txt`)
- [ ] Database inizializzato (`python3 init_db.py`)
- [ ] Applicazione avviata (`python3 run.py`)
- [ ] Browser aperto su `http://localhost:5001`
- [ ] Link "Verifiche" visibile nella navbar
- [ ] Pagina verifiche si carica correttamente

---

## ❌ Problemi Comuni e Soluzioni

### **Problema: "ModuleNotFoundError: No module named 'flask'"**

**Soluzione:**
```bash
pip3 install -r requirements.txt
```

### **Problema: "Non vedo il link Verifiche nella navbar"**

**Soluzione:**
1. Assicurati di aver fatto pull delle ultime modifiche: `git pull origin claude/setup-educational-app-011CUfVBpyezLUxJdQVXzUPC`
2. Riavvia l'applicazione (CTRL+C e poi `python3 run.py`)
3. Svuota la cache del browser (CTRL+F5)

### **Problema: "404 Not Found sulla pagina /verifiche"**

**Soluzione:**
1. Verifica che il file `app/templates/verifiche.html` esista
2. Verifica che il file `app/static/js/verifiche.js` esista
3. Riavvia l'applicazione

### **Problema: "Errore database o tabelle non trovate"**

**Soluzione:**
```bash
# Elimina il database esistente e ricrealo
rm -f instance/didattica.db
python3 init_db.py
```

### **Problema: "Il generatore AI non funziona"**

**Soluzione:**
1. Verifica di aver configurato `ANTHROPIC_API_KEY`
2. Verifica che la API key sia valida
3. Puoi sempre creare verifiche manualmente senza usare l'AI

---

## 📞 Ancora Problemi?

Se dopo aver seguito tutti i passaggi non riesci ancora a vedere la sezione "Verifiche":

1. Verifica di essere sul branch corretto:
   ```bash
   git branch
   # Dovresti vedere: * claude/setup-educational-app-011CUfVBpyezLUxJdQVXzUPC
   ```

2. Verifica che i file esistano:
   ```bash
   ls app/templates/verifiche.html
   ls app/static/js/verifiche.js
   ```

3. Controlla i log dell'applicazione per eventuali errori nel terminale

---

## 🎉 Sei Pronto!

Una volta completati i passaggi sopra, dovresti vedere la nuova sezione **"Verifiche"** funzionante con tutte le funzionalità:

- ✅ Creazione verifiche con domande strutturate
- ✅ Criteri di valutazione dettagliati
- ✅ Generatore AI con Claude
- ✅ Visualizzazione completa verifiche
- ✅ Calcolo automatico punteggi

Buon lavoro! 🚀
