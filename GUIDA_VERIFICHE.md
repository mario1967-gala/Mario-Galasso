# Guida al Sistema di Registro Verifiche

## Panoramica

Il nuovo sistema di registro verifiche permette di gestire verifiche con esercizi multipli, assegnare pesi diversi agli esercizi e calcolare automaticamente la media pesata finale per ogni studente.

## Caratteristiche Principali

### 1. Verifiche con Esercizi Multipli
- Ogni verifica può contenere più esercizi
- Ogni esercizio ha:
  - **Numero**: identificativo progressivo (Es. 1, 2, 3...)
  - **Titolo**: nome dell'esercizio
  - **Punteggio massimo**: il punteggio massimo ottenibile
  - **Peso**: importanza dell'esercizio (da 1 a 10)

### 2. Registro Completo
- Visualizzazione a tabella con:
  - Studenti ordinati alfabeticamente per cognome
  - Colonne per ogni esercizio
  - Voto finale calcolato automaticamente

### 3. Calcolo Media Pesata
Il voto finale viene calcolato automaticamente con la formula:

```
Voto Finale = Σ(Voto Normalizzato × Peso) / Σ(Pesi)
```

Dove:
- **Voto Normalizzato** = (Punteggio ottenuto / Punteggio max) × 10

## Come Usare il Sistema

### Passo 1: Creare una Nuova Verifica

1. Vai alla pagina **Verifiche** dal menu
2. Clicca su **"Nuova Verifica"**
3. Compila i campi:
   - **Titolo**: es. "Verifica di Fisica - Dinamica"
   - **Classe**: seleziona la classe
   - **Materia**: seleziona la materia
   - **Data**: data della verifica
   - **Descrizione** (opzionale): note aggiuntive
4. Clicca **"Salva"**

### Passo 2: Aggiungere Esercizi

1. Dalla lista verifiche, clicca **"Registro"** sulla verifica desiderata
2. Clicca **"Aggiungi Esercizio"**
3. Compila i campi:
   - **Numero**: 1, 2, 3... (progressivo)
   - **Titolo**: es. "Problema sul moto uniformemente accelerato"
   - **Punteggio Massimo**: es. 10 (punti massimi per l'esercizio)
   - **Peso**: da 1 a 10 (importanza dell'esercizio)
   - **Descrizione** (opzionale)
4. Clicca **"Salva"**
5. Ripeti per tutti gli esercizi della verifica

### Passo 3: Inserire i Voti

1. Nel registro, vedrai una tabella con:
   - Colonna per studente
   - Colonne per ogni esercizio
   - Colonna finale con il voto calcolato

2. Per inserire un voto:
   - Clicca sul campo di input nella cella studente/esercizio
   - Inserisci il punteggio ottenuto (da 0 al punteggio max)
   - Il voto si salva automaticamente quando cambi campo

3. Il **Voto Finale** si aggiorna automaticamente dopo ogni inserimento

## Esempio Pratico

### Configurazione Verifica
**Verifica: "Dinamica"**

| Esercizio | Titolo | Punti Max | Peso |
|-----------|--------|-----------|------|
| 1 | Forza e accelerazione | 10 | 3 |
| 2 | Moto parabolico | 15 | 5 |
| 3 | Energia cinetica | 8 | 2 |

### Voti Studente: Mario Rossi

| Esercizio | Punteggio | Normalizzato | Contributo |
|-----------|-----------|--------------|------------|
| Es. 1 | 8/10 | 8.0 | 8.0 × 3 = 24 |
| Es. 2 | 12/15 | 8.0 | 8.0 × 5 = 40 |
| Es. 3 | 6/8 | 7.5 | 7.5 × 2 = 15 |

**Voto Finale** = (24 + 40 + 15) / (3 + 5 + 2) = 79 / 10 = **7.9**

## Suggerimenti

### Assegnazione dei Pesi

- **Peso 1-3**: Esercizi semplici o introduttivi
- **Peso 4-6**: Esercizi standard
- **Peso 7-10**: Esercizi complessi o fondamentali

### Best Practices

1. **Pianifica prima**: Decidi esercizi, punteggi e pesi prima di creare la verifica
2. **Usa pesi bilanciati**: Non tutti gli esercizi devono avere peso 10
3. **Salva progressivamente**: I voti si salvano automaticamente, non perdere i dati
4. **Controlla i totali**: Verifica che i voti finali siano coerenti

## API Disponibili

Se vuoi integrare il sistema con altri strumenti:

### Creare Verifica
```
POST /api/verifiche
{
  "titolo": "...",
  "classe_id": 1,
  "materia_id": 1,
  "data": "2025-11-15",
  "descrizione": "..."
}
```

### Aggiungere Esercizio
```
POST /api/verifiche/{verifica_id}/esercizi
{
  "numero": 1,
  "titolo": "...",
  "punteggio_max": 10,
  "peso": 5,
  "descrizione": "..."
}
```

### Salvare Voto Esercizio
```
POST /api/voti-esercizi
{
  "esercizio_id": 1,
  "studente_id": 1,
  "punteggio": 8.5
}
```

### Visualizzare Registro
```
GET /api/verifiche/{verifica_id}/registro
```

Restituisce il registro completo con tutti gli studenti, voti per esercizio e voti finali calcolati.

## Risoluzione Problemi

### Il voto finale non si calcola
- Verifica che almeno un esercizio abbia un voto inserito
- Controlla che i pesi siano configurati correttamente (1-10)

### Non vedo gli studenti nel registro
- Verifica che la classe abbia studenti assegnati
- Controlla che la verifica sia associata alla classe corretta

### I voti non si salvano
- Controlla la connessione al server
- Verifica che il punteggio sia tra 0 e il punteggio massimo dell'esercizio

## Supporto

Per qualsiasi problema o suggerimento, consulta la documentazione completa nel file README.md del progetto.

---

**Sistema di Gestione Didattica - Liceo Scientifico**
*Versione con Registro Verifiche Automatizzato*
