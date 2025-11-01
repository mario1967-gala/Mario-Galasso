#!/usr/bin/env python3
"""Valida la struttura 4-2-1-1 della verifica"""
import json

with open('test_result.json', 'r') as f:
    data = json.load(f)

verifica = data['verifica']
domande = verifica['domande']

# Conta per livello
livelli_count = {'BASE': 0, 'INTERMEDIO': 0, 'AVANZATO': 0, 'DIFFICILE': 0}
punteggi = {'BASE': 0, 'INTERMEDIO': 0, 'AVANZATO': 0, 'DIFFICILE': 0}

for domanda in domande:
    livello = domanda['livello']
    livelli_count[livello] += 1
    punteggi[livello] += domanda['punteggio']

print("✅ VERIFICA STRUTTURA 4-2-1-1")
print("=" * 60)
print(f"📊 Verifica: {verifica['titolo']}")
print(f"📚 Materia: {verifica['materia_nome']}")
print(f"📅 Data: {verifica['data_verifica']}")
print(f"⏱️  Durata: {verifica['durata_minuti']} minuti")
print()
print("🔍 DISTRIBUZIONE DOMANDE:")
print("-" * 60)
print(f"  BASE:       {livelli_count['BASE']} domande × {punteggi['BASE']/livelli_count['BASE']:.0f} pt = {punteggi['BASE']:.0f} pt ({punteggi['BASE']/verifica['punteggio_totale']*100:.0f}%)")
print(f"  INTERMEDIO: {livelli_count['INTERMEDIO']} domande × {punteggi['INTERMEDIO']/livelli_count['INTERMEDIO']:.0f} pt = {punteggi['INTERMEDIO']:.0f} pt ({punteggi['INTERMEDIO']/verifica['punteggio_totale']*100:.0f}%)")
print(f"  AVANZATO:   {livelli_count['AVANZATO']} domanda  × {punteggi['AVANZATO']:.0f} pt = {punteggi['AVANZATO']:.0f} pt ({punteggi['AVANZATO']/verifica['punteggio_totale']*100:.0f}%)")
print(f"  DIFFICILE:  {livelli_count['DIFFICILE']} domanda  × {punteggi['DIFFICILE']:.0f} pt = {punteggi['DIFFICILE']:.0f} pt ({punteggi['DIFFICILE']/verifica['punteggio_totale']*100:.0f}%)")
print("-" * 60)
print(f"  TOTALE:     {len(domande)} domande = {verifica['punteggio_totale']:.0f} pt")
print()

# Verifica conformità
conforme = (
    livelli_count['BASE'] == 4 and
    livelli_count['INTERMEDIO'] == 2 and
    livelli_count['AVANZATO'] == 1 and
    livelli_count['DIFFICILE'] == 1
)

if conforme:
    print("✅ STRUTTURA CONFORME alla Rubrica Ministeriale 4-2-1-1")
else:
    print("❌ STRUTTURA NON CONFORME")
    print(f"   Atteso: BASE=4, INTERMEDIO=2, AVANZATO=1, DIFFICILE=1")
    print(f"   Trovato: BASE={livelli_count['BASE']}, INTERMEDIO={livelli_count['INTERMEDIO']}, AVANZATO={livelli_count['AVANZATO']}, DIFFICILE={livelli_count['DIFFICILE']}")

print()
print("📝 DETTAGLIO NUOVI CAMPI:")
print("-" * 60)

# Verifica distrattori negli INTERMEDI
intermedi_con_distrattori = sum(1 for d in domande if d['livello'] == 'INTERMEDIO' and d['distrattori'])
print(f"  ✓ Domande INTERMEDIE con distrattori: {intermedi_con_distrattori}/{livelli_count['INTERMEDIO']}")

# Verifica tempo stimato
domande_con_tempo = sum(1 for d in domande if d['tempo_stimato'])
print(f"  ✓ Domande con tempo_stimato: {domande_con_tempo}/{len(domande)}")

# Verifica criteri
for i, d in enumerate(domande, 1):
    print(f"  ✓ Domanda {i} ({d['livello']}): {d['num_criteri']} criteri, {d['tempo_stimato']} min")

print()
print("=" * 60)
