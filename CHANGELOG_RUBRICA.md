# Changelog - Integrazione Rubrica Ministeriale

## Data: 2025-11-01

### Modifiche Implementate

#### 1. Modello Database (`app/models.py`)
**Aggiornata classe `DomandaVerifica`** con nuovi campi:
- ✅ `livello` (VARCHAR 20): BASE, INTERMEDIO, AVANZATO, DIFFICILE
- ✅ `tempo_stimato` (INTEGER): Tempo stimato in minuti per risolvere la domanda
- ✅ `distrattori` (TEXT): JSON con distrattori (dati irrilevanti ma plausibili) per domande INTERMEDIE

**Metodo `to_dict()` aggiornato** per includere i nuovi campi.

---

#### 2. Nuovo Prompt AI (`app/prompt_template_verifica.py`)
**Creato file dedicato** con prompt dettagliato basato sul PDF `template_verifica.pdf`.

**Struttura 4-2-1-1 obbligatoria:**
- 4 esercizi **BASE** (4 pt × 4 = 16 pt, 55%)
- 2 esercizi **INTERMEDIO** (3 pt × 2 = 6 pt, 21%) con distrattori
- 1 esercizio **AVANZATO** (5 pt, 17%) multi-fase
- 1 esercizio **DIFFICILE** (2 pt, 7%) con valutazione critica

**Totale: 29 punti | Sufficienza: 17 punti (59%)**

**Funzione principale:**
```python
genera_prompt_verifica(materia_nome, argomenti, classe="Terza", indirizzo="Scientifico")
```

**Criteri dettagliati per livello:**
- **BASE**: Applicazione diretta, nessun distrattore, formule standard
- **INTERMEDIO**: 1-2 distrattori plausibili, selezione critica dati
- **AVANZATO**: Multi-fase (4-6 passaggi), integrazione concetti
- **DIFFICILE**: Situazione realistica + valutazione critica argomentata

---

#### 3. API Routes (`app/routes.py`)

**Import aggiunto:**
```python
from app.prompt_template_verifica import genera_prompt_verifica
```

**Endpoint `/api/verifiche/genera-ai` aggiornato:**
- ✅ Usa nuovo prompt template
- ✅ Modello Claude 3.5 Sonnet (più potente)
- ✅ Max tokens aumentato a 8000
- ✅ **Validazione struttura 4-2-1-1** automatica
- ✅ Restituzione info struttura generata

**Endpoint `/api/verifiche` POST aggiornato:**
- ✅ Gestione nuovi campi: `livello`, `tempo_stimato`, `distrattori`
- ✅ Salvataggio corretto nel database

---

#### 4. Script Migrazione Database

**File SQL**: `migrate_rubrica.sql`
```sql
ALTER TABLE domande_verifica ADD COLUMN livello VARCHAR(20) DEFAULT 'BASE';
ALTER TABLE domande_verifica ADD COLUMN tempo_stimato INTEGER;
ALTER TABLE domande_verifica ADD COLUMN distrattori TEXT;
```

**File Python**: `migrate_db_rubrica.py`
Script Python con controlli avanzati e logging.

---

### Come Usare

#### 1. Migrazione Database (prima esecuzione)
```bash
# Se il database esiste già
sqlite3 instance/app.db < migrate_rubrica.sql

# Oppure usa lo script Python (quando Flask è installato)
python migrate_db_rubrica.py
```

#### 2. Generare una Verifica
**Request:**
```json
POST /api/verifiche/genera-ai
{
  "materia_id": 1,
  "argomenti": "Cinematica e Dinamica",
  "classe": "Terza",
  "indirizzo": "Scientifico"
}
```

**Response:**
```json
{
  "success": true,
  "verifica_data": {
    "titolo": "Verifica di Fisica: Cinematica e Dinamica",
    "punteggio_totale": 29.0,
    "soglia_sufficienza": 17.0,
    "domande": [...]
  },
  "struttura": {
    "BASE": 4,
    "INTERMEDIO": 2,
    "AVANZATO": 1,
    "DIFFICILE": 1
  }
}
```

#### 3. Salvare la Verifica
```json
POST /api/verifiche
{
  "materia_id": 1,
  "titolo": "...",
  "data_verifica": "2025-11-15",
  "durata_minuti": 60,
  "generata_ai": true,
  "domande": [...]
}
```

---

### Vantaggi

1. **Conformità Rubrica Ministeriale**
   - Struttura 4-2-1-1 garantita
   - Criteri di valutazione dettagliati
   - Mappatura con indicatori ministeriali

2. **Distrattori Educativi**
   - Insegnano agli studenti a selezionare dati rilevanti
   - Plausibili ma riconoscibili con attenzione
   - Documentati per il docente

3. **Progressione Didattica**
   - Gradualità garantita (BASE → INTERMEDIO → AVANZATO → DIFFICILE)
   - Sufficienza raggiungibile con BASE + parte INTERMEDIO
   - Eccellenza premiata con AVANZATO e DIFFICILE

4. **Validazione Automatica**
   - Il sistema verifica automaticamente la struttura 4-2-1-1
   - Segnala errori se non conforme
   - Output standardizzato

---

### Note Tecniche

- **Database**: Modifiche retrocompatibili (default values)
- **Modello AI**: Aggiornato a Claude 3.5 Sonnet per task complessi
- **Validazione**: Controlli lato server per conformità
- **Frontend**: Da aggiornare per mostrare nuovi campi (TODO)

---

### Prossimi Passi

1. [ ] Aggiornare frontend (`app/static/js/verifiche.js`) per:
   - Mostrare livello delle domande
   - Evidenziare distrattori nelle domande INTERMEDIE
   - Visualizzare tempo stimato
   - Mostrare struttura 4-2-1-1 nel riepilogo

2. [ ] Creare template stampa PDF verifiche
3. [ ] Implementare rubrica valutazione interattiva
4. [ ] Test completo del sistema

---

## Riferimenti

- **Documento**: `template_verifica.pdf` - Criteri di Costruzione Verifiche Scritte di Fisica
- **Struttura**: 4-2-1-1 (4 BASE, 2 INTERMEDIO, 1 AVANZATO, 1 DIFFICILE)
- **Classe target**: Terza - Liceo Scientifico
