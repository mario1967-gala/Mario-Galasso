# 🧪 Guida Testing Sistema Rubrica Ministeriale

## ✅ Stato Attuale del Sistema

### Database
- ✅ Database creato: `instance/didattica.db`
- ✅ Nuove colonne aggiunte a `domande_verifica`:
  - `livello` (BASE | INTERMEDIO | AVANZATO | DIFFICILE)
  - `tempo_stimato` (INTEGER - minuti)
  - `distrattori` (TEXT - JSON)

### Server
- ✅ Server Flask in esecuzione su `http://localhost:5001`
- ✅ Debug mode attivo
- ✅ API REST funzionanti

### Dati
- ✅ Materia "Fisica" creata (ID: 1)

---

## 🚀 Come Testare la Generazione Verifiche

### Opzione A: Con API Key Anthropic (Generazione AI)

**1. Configura API Key:**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**2. Riavvia il server:**
```bash
# Ferma il server attuale
pkill -f "python run.py"

# Riavvia con la nuova variabile
source venv/bin/activate
python run.py
```

**3. Genera verifica con AI:**
```bash
curl -X POST http://localhost:5001/api/verifiche/genera-ai \
  -H "Content-Type: application/json" \
  -d '{
    "materia_id": 1,
    "argomenti": "Cinematica e Dinamica: moto rettilineo uniforme e uniformemente accelerato, leggi di Newton",
    "classe": "Terza",
    "indirizzo": "Scientifico"
  }' | python3 -m json.tool > verifica_generata.json

# Visualizza risultato
cat verifica_generata.json
```

**Output atteso:**
```json
{
  "success": true,
  "message": "Verifica generata secondo Rubrica Ministeriale 4-2-1-1",
  "struttura": {
    "BASE": 4,
    "INTERMEDIO": 2,
    "AVANZATO": 1,
    "DIFFICILE": 1
  },
  "verifica_data": {
    "titolo": "Verifica di Fisica: Cinematica e Dinamica",
    "punteggio_totale": 29.0,
    "soglia_sufficienza": 17.0,
    "domande": [...]
  }
}
```

---

### Opzione B: Senza API Key (Verifica Manuale)

Puoi creare una verifica manualmente per testare il sistema:

```bash
curl -X POST http://localhost:5001/api/verifiche \
  -H "Content-Type: application/json" \
  -d '{
    "materia_id": 1,
    "titolo": "Verifica di Fisica: Cinematica",
    "descrizione": "Verifica strutturata 4-2-1-1",
    "argomenti": "Cinematica",
    "data_verifica": "2025-11-15",
    "durata_minuti": 60,
    "generata_ai": false,
    "domande": [
      {
        "numero": 1,
        "livello": "BASE",
        "testo": "Un corpo si muove di moto rettilineo uniforme...",
        "tipo": "esercizio",
        "punteggio": 4.0,
        "tempo_stimato": 10,
        "distrattori": null,
        "righe_risposta": 15,
        "criteri": [
          {
            "descrizione": "Impostazione corretta",
            "punteggio": 2.0,
            "ordine": 1
          },
          {
            "descrizione": "Calcolo corretto",
            "punteggio": 2.0,
            "ordine": 2
          }
        ]
      }
    ]
  }' | python3 -m json.tool
```

---

## 📊 Endpoint Disponibili

### 1. Genera Verifica con AI
```
POST /api/verifiche/genera-ai
Body: {
  "materia_id": 1,
  "argomenti": "...",
  "classe": "Terza",
  "indirizzo": "Scientifico"
}
```

### 2. Salva Verifica
```
POST /api/verifiche
Body: { verifica_data... }
```

### 3. Lista Verifiche
```
GET /api/verifiche
```

### 4. Dettaglio Verifica
```
GET /api/verifiche/{id}
```

---

## 🔍 Verifica Struttura Generata

Dopo aver generato una verifica, verifica che:

### ✅ Struttura 4-2-1-1
```bash
cat verifica_generata.json | jq '.struttura'
```
Deve mostrare:
```json
{
  "BASE": 4,
  "INTERMEDIO": 2,
  "AVANZATO": 1,
  "DIFFICILE": 1
}
```

### ✅ Punteggi
```bash
cat verifica_generata.json | jq '.verifica_data.punteggio_totale'
```
Deve essere: `29.0`

```bash
cat verifica_generata.json | jq '.verifica_data.soglia_sufficienza'
```
Deve essere: `17.0`

### ✅ Domande BASE (no distrattori)
```bash
cat verifica_generata.json | jq '.verifica_data.domande[] | select(.livello=="BASE") | .distrattori'
```
Deve essere: `null` per tutte

### ✅ Domande INTERMEDIE (con distrattori)
```bash
cat verifica_generata.json | jq '.verifica_data.domande[] | select(.livello=="INTERMEDIO") | .distrattori'
```
Deve contenere testo esplicativo dei distrattori

### ✅ Domanda DIFFICILE (con valutazione critica)
```bash
cat verifica_generata.json | jq '.verifica_data.domande[] | select(.livello=="DIFFICILE") | .testo'
```
Deve contenere richiesta di "valutazione critica" o "motivazione"

---

## 🌐 Interfaccia Web

Apri nel browser:
```
http://localhost:5001/verifiche
```

Dovresti vedere l'interfaccia per gestire le verifiche.

**Nota:** Il frontend potrebbe ancora non mostrare i nuovi campi (livello, distrattori, tempo_stimato). Questo richiede aggiornamento JavaScript (TODO futuro).

---

## 🐛 Troubleshooting

### Errore API Key
```
"error": "ANTHROPIC_API_KEY non configurata"
```
**Soluzione:** Configura la variabile d'ambiente e riavvia

### Errore Struttura 4-2-1-1
```
"error": "Struttura non conforme 4-2-1-1"
```
**Causa:** L'AI non ha rispettato la struttura richiesta
**Soluzione:** Riprova la generazione (il prompt è molto dettagliato, dovrebbe funzionare al 99%)

### Server non risponde
```bash
# Verifica se il server è attivo
pgrep -f "python run.py"

# Controlla i log
tail -f flask.log
```

---

## 📝 Prossimi Passi

1. [ ] **Frontend**: Aggiornare `app/static/js/verifiche.js` per mostrare:
   - Badge livello domanda
   - Distrattori evidenziati
   - Tempo stimato
   - Riepilogo struttura 4-2-1-1

2. [ ] **Export PDF**: Template per stampare verifiche

3. [ ] **Rubrica Interattiva**: Interfaccia per valutare con criteri ministeriali

4. [ ] **Statistiche**: Dashboard con analisi verifiche generate

---

## 📚 Riferimenti

- **Documento**: `template_verifica.pdf`
- **Changelog**: `CHANGELOG_RUBRICA.md`
- **Prompt Template**: `app/prompt_template_verifica.py`
- **Migrazione DB**: `migrate_rubrica.sql`

---

## ✨ Esempio Completo

```bash
# 1. Genera verifica
curl -X POST http://localhost:5001/api/verifiche/genera-ai \
  -H "Content-Type: application/json" \
  -d '{"materia_id": 1, "argomenti": "Cinematica"}' \
  > verifica.json

# 2. Estrai dati
VERIFICA_DATA=$(cat verifica.json | jq '.verifica_data')

# 3. Salva nel database
curl -X POST http://localhost:5001/api/verifiche \
  -H "Content-Type: application/json" \
  -d "{
    \"materia_id\": 1,
    \"titolo\": $(echo $VERIFICA_DATA | jq '.titolo'),
    \"data_verifica\": \"2025-11-15\",
    \"generata_ai\": true,
    ...
  }"

# 4. Visualizza verifiche salvate
curl http://localhost:5001/api/verifiche | python3 -m json.tool
```

---

🎓 **Buon testing!**
