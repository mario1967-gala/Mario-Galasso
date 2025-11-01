"""
Template prompt per generazione verifiche secondo Rubrica Ministeriale
Struttura 4-2-1-1 conforme al documento "Criteri di Costruzione Verifiche Scritte di Fisica"
"""

def genera_prompt_verifica(materia_nome, argomenti, classe="Terza", indirizzo="Scientifico"):
    """
    Genera il prompt per Claude AI seguendo i criteri del PDF template_verifica.pdf

    Struttura 4-2-1-1:
    - 4 esercizi BASE (4 pt × 4 = 16 pt, 55%)
    - 2 esercizi INTERMEDIO (3 pt × 2 = 6 pt, 21%)
    - 1 esercizio AVANZATO (5 pt, 17%)
    - 1 esercizio DIFFICILE (2 pt, 7%)
    TOTALE: 29 punti | SUFFICIENZA: 17 punti (59%)
    """

    prompt = f"""Sei un esperto docente di {materia_nome} per il Liceo {indirizzo}, Classe {classe}.

# COMPITO
Genera una verifica scritta COMPLETA secondo la **Rubrica Ministeriale di Valutazione** con struttura 4-2-1-1.

# ARGOMENTI DELLA VERIFICA
{argomenti}

# STRUTTURA OBBLIGATORIA 4-2-1-1

La verifica DEVE contenere esattamente:
- **4 esercizi BASE** (4,0 pt ciascuno = 16 pt totali, 55%)
- **2 esercizi INTERMEDIO** (3,0 pt ciascuno = 6 pt totali, 21%)
- **1 esercizio AVANZATO** (5,0 pt = 5 pt totali, 17%)
- **1 esercizio DIFFICILE** (2,0 pt = 2 pt totali, 7%)

**TOTALE: 29 punti | SUFFICIENZA: 17 punti (59%)**

# CRITERI PER LIVELLO

## LIVELLO BASE (4 esercizi × 4 pt)
**Obiettivo:** Verificare acquisizione conoscenze fondamentali e applicazione diretta

**Caratteristiche OBBLIGATORIE:**
✓ Applicazione diretta di formule (max 1-2 passaggi matematici)
✓ Un SOLO concetto per esercizio (NO mescolanza argomenti)
✓ NESSUN distrattore (tutti i dati forniti sono necessari e sufficienti)
✓ Dati ben organizzati (elenchi puntati, unità di misura esplicite)
✓ Procedura risolutiva ovvia e unica
✓ 3 domande (a, b, c) con punteggi: 1,5 + 1,5 + 1,0 pt oppure 1,2 + 1,6 + 1,2 pt
✓ Tempo stimato: 8-10 minuti

**NON FARE nel BASE:**
✗ Distrattori o dati superflui
✗ Formule da ricavare
✗ Multi-step impliciti
✗ Valori numerici complicati

## LIVELLO INTERMEDIO (2 esercizi × 3 pt)
**Obiettivo:** Verificare capacità di selezione critica dei dati

**Caratteristiche OBBLIGATORIE:**
✓ **1-2 DISTRATTORI** esplicitamente inseriti nel testo (dati veri ma NON necessari)
✓ Distrattori plausibili ma riconoscibili con attenzione
✓ Testo più articolato (5-7 righe, informazioni non in ordine logico)
✓ Multi-step moderato (2-3 passaggi matematici)
✓ Possibile conversione unità (es. km/h → m/s)
✓ 2-3 domande che sommano a 3,0 pt
✓ Tempo stimato: 6-8 minuti

**IMPORTANTE:** Nel campo "distrattori" specifica quali dati sono irrilevanti e perché

**Esempi distrattori efficaci:**
- Massa di un corpo in moto rettilineo uniforme (non serve senza dinamica)
- Temperatura ambiente (irrilevante se non ci sono calcoli termici)
- Colore o forma di un oggetto (se non influenza il fenomeno)

## LIVELLO AVANZATO (1 esercizio × 5 pt)
**Obiettivo:** Verificare analisi complessa e ragionamento multi-step

**Caratteristiche OBBLIGATORIE:**
✓ Problema multi-fase (4-6 passaggi matematici)
✓ Integrazione di 2-3 concetti correlati
✓ Concatenazione logica tra domande (l'output di una è input della successiva)
✓ Richiesta di analisi qualitativa (non solo calcoli)
✓ Possibile richiesta grafica (costruzione o interpretazione)
✓ 3-4 domande concatenate (somma 5,0 pt)
✓ Tempo stimato: 10-12 minuti

## LIVELLO DIFFICILE (1 esercizio × 2 pt)
**Obiettivo:** Verificare capacità di valutazione critica

**Caratteristiche OBBLIGATORIE:**
✓ Situazione REALISTICA e riconoscibile (sport, vita quotidiana, tecnologia)
✓ 2 domande:
  - Domanda a) Calcolo quantitativo (1,0-1,3 pt)
  - Domanda b) **VALUTAZIONE CRITICA** con argomentazione richiesta (0,7-1,0 pt)
✓ Domanda b) deve chiedere: "È realistico? È fattibile? Motiva la risposta"
✓ Valutazione basata su confronto con esperienza comune
✓ Tempo stimato: 5-8 minuti

# FORMATO OUTPUT JSON

Rispondi SOLO con JSON valido (senza markdown, senza testo aggiuntivo):

{{
  "titolo": "Verifica di {materia_nome}: [Argomenti]",
  "descrizione": "Verifica strutturata secondo Rubrica Ministeriale 4-2-1-1",
  "argomenti": "{argomenti}",
  "durata_minuti": 60,
  "punteggio_totale": 29.0,
  "soglia_sufficienza": 17.0,
  "domande": [
    {{
      "numero": 1,
      "livello": "BASE",
      "testo": "[Testo esercizio BASE completo con tutti i dati]\\n\\na) [Domanda a] [1,5 pt]\\nb) [Domanda b] [1,5 pt]\\nc) [Domanda c] [1,0 pt]",
      "tipo": "esercizio",
      "punteggio": 4.0,
      "tempo_stimato": 10,
      "distrattori": null,
      "opzioni": null,
      "risposta_corretta": null,
      "righe_risposta": 15,
      "criteri": [
        {{
          "descrizione": "Domanda a) - Impostazione corretta formula",
          "punteggio": 0.7,
          "ordine": 1
        }},
        {{
          "descrizione": "Domanda a) - Svolgimento e risultato corretto",
          "punteggio": 0.8,
          "ordine": 2
        }},
        {{
          "descrizione": "Domanda b) - Calcolo corretto",
          "punteggio": 1.5,
          "ordine": 3
        }},
        {{
          "descrizione": "Domanda c) - Interpretazione corretta",
          "punteggio": 1.0,
          "ordine": 4
        }}
      ],
      "note": "Esercizio BASE: applicazione diretta di formule cinematiche. Tutti i dati forniti sono necessari."
    }},
    {{
      "numero": 5,
      "livello": "INTERMEDIO",
      "testo": "[Testo con 1-2 DISTRATTORI evidenziati]\\n\\na) [Domanda a] [1,0 pt]\\nb) [Domanda b] [1,5 pt]\\nc) [Domanda c] [0,5 pt]",
      "tipo": "esercizio",
      "punteggio": 3.0,
      "tempo_stimato": 8,
      "distrattori": "[Spiegazione: 'Massa del corpo (5 kg)' è un distrattore perché il problema riguarda solo cinematica senza forze. 'Temperatura ambiente (20°C)' è irrilevante senza termodinamica.]",
      "opzioni": null,
      "risposta_corretta": null,
      "righe_risposta": 10,
      "criteri": [
        {{
          "descrizione": "Riconoscimento dati rilevanti (NO uso distrattori)",
          "punteggio": 0.5,
          "ordine": 1
        }},
        {{
          "descrizione": "Domanda a) - Conversione unità corretta",
          "punteggio": 0.5,
          "ordine": 2
        }},
        {{
          "descrizione": "Domanda b) - Calcolo multi-step corretto",
          "punteggio": 1.5,
          "ordine": 3
        }},
        {{
          "descrizione": "Domanda c) - Risposta corretta",
          "punteggio": 0.5,
          "ordine": 4
        }}
      ],
      "note": "Esercizio INTERMEDIO con distrattori. Penalità -0,2 pt se vengono utilizzati i dati irrilevanti."
    }},
    {{
      "numero": 7,
      "livello": "AVANZATO",
      "testo": "[Problema multi-fase complesso]\\n\\na) [Fase 1] [1,5 pt]\\nb) [Fase 2] [1,5 pt]\\nc) [Fase 3] [1,0 pt]\\nd) [Analisi qualitativa + grafico] [1,0 pt]",
      "tipo": "esercizio",
      "punteggio": 5.0,
      "tempo_stimato": 12,
      "distrattori": null,
      "opzioni": null,
      "risposta_corretta": null,
      "righe_risposta": 20,
      "criteri": [
        {{
          "descrizione": "Fase 1 - Impostazione e calcolo corretto",
          "punteggio": 1.5,
          "ordine": 1
        }},
        {{
          "descrizione": "Fase 2 - Uso risultato precedente e calcolo",
          "punteggio": 1.5,
          "ordine": 2
        }},
        {{
          "descrizione": "Fase 3 - Integrazione concetti",
          "punteggio": 1.0,
          "ordine": 3
        }},
        {{
          "descrizione": "Analisi qualitativa e grafico con spiegazione fisica",
          "punteggio": 1.0,
          "ordine": 4
        }}
      ],
      "note": "Esercizio AVANZATO: richiede integrazione di più concetti e ragionamento multi-step concatenato."
    }},
    {{
      "numero": 8,
      "livello": "DIFFICILE",
      "testo": "[Situazione realistica]\\n\\na) Calcola [grandezza fisica] [1,3 pt]\\nb) Valuta criticamente se [situazione] è realistico/fattibile. Motiva la tua risposta considerando sia i calcoli che eventuali fattori che potrebbero influenzare [fenomeno]. [0,7 pt]",
      "tipo": "esercizio",
      "punteggio": 2.0,
      "tempo_stimato": 6,
      "distrattori": null,
      "opzioni": null,
      "risposta_corretta": null,
      "righe_risposta": 10,
      "criteri": [
        {{
          "descrizione": "Domanda a) - Calcolo corretto",
          "punteggio": 1.3,
          "ordine": 1
        }},
        {{
          "descrizione": "Domanda b) - Valutazione critica argomentata con confronto realistico",
          "punteggio": 0.7,
          "ordine": 2
        }}
      ],
      "note": "Esercizio DIFFICILE: la domanda b) richiede giudizio critico motivato. Accettare risposte diverse se ben argomentate."
    }}
  ]
}}

# VERIFICA FINALE
Prima di rispondere, verifica:
✓ Esattamente 8 esercizi (4 BASE + 2 INTERMEDIO + 1 AVANZATO + 1 DIFFICILE)
✓ Punteggi: 16 + 6 + 5 + 2 = 29 punti totali
✓ BASE senza distrattori, INTERMEDIO con 1-2 distrattori
✓ AVANZATO multi-fase, DIFFICILE con valutazione critica
✓ Tutti gli esercizi hanno criteri di valutazione dettagliati
✓ Tempo totale ≈ 60 minuti
"""

    return prompt


def genera_prompt_verifica_custom(materia_nome, argomenti, num_base=4, num_intermedio=2, num_avanzato=1, num_difficile=1):
    """
    Versione personalizzabile del prompt (mantiene comunque i principi del PDF)
    """
    totale_base = num_base * 4.0
    totale_intermedio = num_intermedio * 3.0
    totale_avanzato = num_avanzato * 5.0
    totale_difficile = num_difficile * 2.0
    punteggio_totale = totale_base + totale_intermedio + totale_avanzato + totale_difficile
    soglia_sufficienza = round(punteggio_totale * 0.59, 1)

    # TODO: implementare versione custom
    # Per ora usa la versione standard
    return genera_prompt_verifica(materia_nome, argomenti)
