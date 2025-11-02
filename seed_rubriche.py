#!/usr/bin/env python3
"""
Script per popolare il database con rubriche di valutazione ministeriali
Basato su template_verifica.pdf - Struttura 4-2-1-1
"""

from app import create_app, db
from app.models import Materia, Rubrica, Criterio, Descrittore

app = create_app()

def crea_rubriche_ministeriali():
    """Crea rubriche di valutazione ministeriali per Fisica"""

    with app.app_context():
        print("🎯 Creazione rubriche ministeriali di valutazione...")

        # Trova la materia Fisica
        fisica = Materia.query.filter_by(nome='Fisica').first()
        if not fisica:
            print("❌ Materia 'Fisica' non trovata! Creo...")
            fisica = Materia(
                nome='Fisica',
                descrizione='Fisica per Liceo Scientifico',
                ore_settimanali=3,
                docente='Prof. Galasso'
            )
            db.session.add(fisica)
            db.session.commit()
            print("✅ Materia Fisica creata")

        # Elimina rubriche esistenti per Fisica per ricrearle
        rubriche_esistenti = Rubrica.query.filter_by(materia_id=fisica.id).all()
        for r in rubriche_esistenti:
            db.session.delete(r)
        db.session.commit()
        print(f"🗑️  Eliminate {len(rubriche_esistenti)} rubriche esistenti")

        # ==================== RUBRICA 1: CINEMATICA ====================
        print("\n📋 Creando Rubrica: Cinematica e Dinamica")
        rubrica_cinematica = Rubrica(
            materia_id=fisica.id,
            titolo='Rubrica: Cinematica e Dinamica',
            descrizione='Rubrica ministeriale per verifiche su cinematica e dinamica. Struttura 4-2-1-1 con 4 livelli di competenza.',
            tipo_verifica='scritta',
            attiva=True
        )
        db.session.add(rubrica_cinematica)
        db.session.commit()

        # CRITERI per Cinematica
        criteri_cinematica = [
            {
                'nome': 'IND. 1 - Acquisizione Contenuti',
                'descrizione': 'Padronanza teorica: conoscenza di formule, leggi e principi fondamentali',
                'peso': 0.40,  # 40% (4/10 punti)
                'ordine': 1
            },
            {
                'nome': 'IND. 2 - Competenze Operative',
                'descrizione': 'Qualità esecuzione: correttezza calcoli, chiarezza procedimento, efficacia strategia',
                'peso': 0.20,  # 20% (2/10 punti)
                'ordine': 2
            },
            {
                'nome': 'IND. 3 - Abilità Logiche e Critiche',
                'descrizione': 'Capacità critica: riconoscimento distrattori, ragionamento multi-step, valutazione',
                'peso': 0.20,  # 20% (2/10 punti)
                'ordine': 3
            },
            {
                'nome': 'IND. 4 - Completezza',
                'descrizione': 'Quantità di lavoro svolto indipendentemente dalla correttezza',
                'peso': 0.20,  # 20% (2/10 punti)
                'ordine': 4
            }
        ]

        for criterio_data in criteri_cinematica:
            criterio = Criterio(
                rubrica_id=rubrica_cinematica.id,
                nome=criterio_data['nome'],
                descrizione=criterio_data['descrizione'],
                peso=criterio_data['peso'],
                ordine=criterio_data['ordine']
            )
            db.session.add(criterio)
            db.session.commit()

            # DESCRITTORI per ogni criterio
            if 'Contenuti' in criterio.nome:
                descrittori = [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Conoscenza ricca e approfondita: risolve 4 BASE + 2 INTERMEDIO + AVANZATO (27 pt). Padronanza profonda di formule complesse e loro applicazione integrata.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Conoscenza completa: risolve 4 BASE + 1-2 INTERMEDIO (19-22 pt). Applica consapevolmente le formule in contesti diversi.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Conoscenza ampia: risolve 4 BASE + parte INTERMEDIO (14-15 pt). Conosce formule fondamentali e le applica in contesti standard.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Conoscenza essenziale: risolve 3 BASE su 4 (12 pt). Conosce solo le formule base con applicazione meccanica.',
                        'punteggio': 4.0
                    }
                ]
            elif 'Competenze' in criterio.nome:
                descrittori = [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Esecuzione impeccabile: calcoli sempre corretti, procedimento chiaro e ben organizzato, strategia efficace e ottimale. Unità di misura corrette.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Esecuzione buona: calcoli generalmente corretti, procedimento comprensibile, strategia adeguata con minimi errori di distrazione.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Esecuzione accettabile: alcuni errori di calcolo, procedimento poco organizzato ma comprensibile, strategia elementare ma funzionale.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Esecuzione incerta: frequenti errori di calcolo, procedimento confuso, strategia poco efficace. Difficoltà con unità di misura.',
                        'punteggio': 4.0
                    }
                ]
            elif 'Abilità Logiche' in criterio.nome:
                descrittori = [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Capacità critica eccellente: riconosce tutti i distrattori, effettua valutazioni critiche argomentate, ragiona su problemi multi-step complessi.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Capacità critica buona: riconosce la maggior parte dei distrattori, valuta criticamente con motivazioni sufficienti, gestisce problemi multi-step.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Capacità critica elementare: riconosce alcuni distrattori, valutazioni parziali o poco approfondite, difficoltà con problemi multi-step.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Capacità critica limitata: non riconosce distrattori, valutazioni assenti o non motivate, non gestisce problemi multi-step.',
                        'punteggio': 4.0
                    }
                ]
            else:  # Completezza
                descrittori = [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Completezza massima: affronta tutti gli esercizi fino al DIFFICILE, anche se non sempre correttamente. Dimostra impegno su tutta la verifica.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Completezza buona: completa BASE, INTERMEDIO e tenta AVANZATO. Lavoro quantitativamente adeguato.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Completezza sufficiente: completa gli esercizi BASE e tenta gli INTERMEDI. Quantità minima accettabile.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Completezza scarsa: completa solo alcuni esercizi BASE. Quantità di lavoro insufficiente.',
                        'punteggio': 4.0
                    }
                ]

            for desc_data in descrittori:
                descrittore = Descrittore(
                    criterio_id=criterio.id,
                    livello=desc_data['livello'],
                    livello_nome=desc_data['livello_nome'],
                    descrizione=desc_data['descrizione'],
                    punteggio=desc_data['punteggio']
                )
                db.session.add(descrittore)

            db.session.commit()
            print(f"  ✅ Criterio: {criterio.nome} (4 livelli)")

        # ==================== RUBRICA 2: ENERGIA E LAVORO ====================
        print("\n📋 Creando Rubrica: Energia, Lavoro e Conservazione")
        rubrica_energia = Rubrica(
            materia_id=fisica.id,
            titolo='Rubrica: Energia, Lavoro e Conservazione',
            descrizione='Rubrica ministeriale per verifiche su energia meccanica, lavoro e principio di conservazione.',
            tipo_verifica='scritta',
            attiva=True
        )
        db.session.add(rubrica_energia)
        db.session.commit()

        # CRITERI per Energia (stessi indicatori, descrittori adattati)
        criteri_energia = [
            {
                'nome': 'IND. 1 - Acquisizione Contenuti',
                'descrizione': 'Conoscenza di formule energetiche (Ek, Ep, L=Fs, conservazione) e loro applicazione',
                'peso': 0.40,
                'ordine': 1,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Padronanza completa: applica conservazione energia in problemi complessi multi-fase. Riconosce quando usare Ek, Ep, L in contesti integrati.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Conoscenza solida: applica correttamente conservazione energia e formule Ek, Ep, L in situazioni standard con 2-3 trasformazioni.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Conoscenza base: calcola Ek e Ep singolarmente, applica L=Fs in situazioni semplici. Difficoltà con conservazione complessa.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Conoscenza frammentaria: confonde Ek e Ep, applica formule in modo meccanico senza comprendere conservazione.',
                        'punteggio': 4.0
                    }
                ]
            },
            {
                'nome': 'IND. 2 - Competenze Operative',
                'descrizione': 'Correttezza nei calcoli energetici e chiarezza nel procedimento',
                'peso': 0.20,
                'ordine': 2,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Calcoli energetici precisi, bilanci corretti, conversioni unità impeccabili. Procedimento chiaro con passaggi giustificati.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Calcoli generalmente corretti, bilanci energetici adeguati, lievi imprecisioni nelle conversioni.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Calcoli con alcuni errori, bilanci incompleti ma comprensibili, difficoltà occasionali con conversioni.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Calcoli spesso errati, bilanci energetici scorretti, confusione con unità di misura (J, W, etc.).',
                        'punteggio': 4.0
                    }
                ]
            },
            {
                'nome': 'IND. 3 - Abilità Logiche',
                'descrizione': 'Ragionamento su trasformazioni energetiche e riconoscimento forze conservative',
                'peso': 0.20,
                'ordine': 3,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Identifica tutte le trasformazioni energetiche, riconosce forze conservative/non conservative, valuta perdite energetiche.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Identifica le principali trasformazioni, distingue forze conservative in contesti standard.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Riconosce trasformazioni energetiche semplici (Ep→Ek), difficoltà con forze non conservative.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Non riconosce trasformazioni energetiche, confusione tra tipi di energia e forze.',
                        'punteggio': 4.0
                    }
                ]
            },
            {
                'nome': 'IND. 4 - Completezza',
                'descrizione': 'Quantità di lavoro svolto sulla verifica',
                'peso': 0.20,
                'ordine': 4,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Completa tutti i livelli (BASE, INTERMEDIO, AVANZATO, DIFFICILE).',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Completa BASE, INTERMEDIO e tenta AVANZATO.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Completa BASE e tenta INTERMEDIO.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Completa solo parte degli esercizi BASE.',
                        'punteggio': 4.0
                    }
                ]
            }
        ]

        for criterio_data in criteri_energia:
            criterio = Criterio(
                rubrica_id=rubrica_energia.id,
                nome=criterio_data['nome'],
                descrizione=criterio_data['descrizione'],
                peso=criterio_data['peso'],
                ordine=criterio_data['ordine']
            )
            db.session.add(criterio)
            db.session.commit()

            for desc_data in criterio_data['descrittori']:
                descrittore = Descrittore(
                    criterio_id=criterio.id,
                    livello=desc_data['livello'],
                    livello_nome=desc_data['livello_nome'],
                    descrizione=desc_data['descrizione'],
                    punteggio=desc_data['punteggio']
                )
                db.session.add(descrittore)

            db.session.commit()
            print(f"  ✅ Criterio: {criterio.nome} (4 livelli)")

        # ==================== RUBRICA 3: TERMODINAMICA ====================
        print("\n📋 Creando Rubrica: Termodinamica")
        rubrica_termo = Rubrica(
            materia_id=fisica.id,
            titolo='Rubrica: Termodinamica',
            descrizione='Rubrica per verifiche su calore, temperatura, gas ideali e primo principio della termodinamica.',
            tipo_verifica='scritta',
            attiva=True
        )
        db.session.add(rubrica_termo)
        db.session.commit()

        criteri_termo = [
            {
                'nome': 'Conoscenza Leggi Termodinamiche',
                'descrizione': 'Conoscenza Q=mcΔT, equazione gas ideali PV=nRT, primo principio ΔU=Q-L',
                'peso': 1.0,
                'ordine': 1,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Applica primo principio in cicli termodinamici completi, risolve problemi con trasformazioni multiple (isobara, isocora, isoterma).',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Applica Q=mcΔT e PV=nRT in problemi standard, calcola Q, L, ΔU in singole trasformazioni.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Calcola calore con Q=mcΔT in calorimetro semplice, usa PV=nRT in applicazioni dirette.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Confonde calore e temperatura, applica formule in modo mnemonico senza comprendere significato fisico.',
                        'punteggio': 4.0
                    }
                ]
            },
            {
                'nome': 'Ragionamento Termodinamico',
                'descrizione': 'Capacità di ragionare su trasformazioni, rendimento, segno di Q e L',
                'peso': 1.0,
                'ordine': 2,
                'descrittori': [
                    {
                        'livello': 4,
                        'livello_nome': 'Avanzato',
                        'descrizione': 'Identifica tipo di trasformazione, determina segno Q e L correttamente, calcola rendimento, analizza cicli.',
                        'punteggio': 10.0
                    },
                    {
                        'livello': 3,
                        'livello_nome': 'Intermedio',
                        'descrizione': 'Riconosce trasformazioni principali, determina segno Q e L in casi standard.',
                        'punteggio': 8.0
                    },
                    {
                        'livello': 2,
                        'livello_nome': 'Base',
                        'descrizione': 'Distingue espansione/compressione, riscaldamento/raffreddamento in situazioni semplici.',
                        'punteggio': 6.0
                    },
                    {
                        'livello': 1,
                        'livello_nome': 'Iniziale',
                        'descrizione': 'Confusione tra Q, L e ΔU. Non riconosce tipi di trasformazioni.',
                        'punteggio': 4.0
                    }
                ]
            }
        ]

        for criterio_data in criteri_termo:
            criterio = Criterio(
                rubrica_id=rubrica_termo.id,
                nome=criterio_data['nome'],
                descrizione=criterio_data['descrizione'],
                peso=criterio_data['peso'],
                ordine=criterio_data['ordine']
            )
            db.session.add(criterio)
            db.session.commit()

            for desc_data in criterio_data['descrittori']:
                descrittore = Descrittore(
                    criterio_id=criterio.id,
                    livello=desc_data['livello'],
                    livello_nome=desc_data['livello_nome'],
                    descrizione=desc_data['descrizione'],
                    punteggio=desc_data['punteggio']
                )
                db.session.add(descrittore)

            db.session.commit()
            print(f"  ✅ Criterio: {criterio.nome} (4 livelli)")

        print("\n" + "="*60)
        print("✅ RUBRICHE MINISTERIALI CREATE CON SUCCESSO!")
        print("="*60)
        print(f"\n📊 Riepilogo:")
        print(f"  • Rubriche create: 3")
        print(f"  • Materia: {fisica.nome}")
        print(f"  • Struttura: 4-2-1-1 (BASE-INTERMEDIO-AVANZATO-DIFFICILE)")
        print(f"  • Livelli competenza: 4 (Avanzato, Intermedio, Base, Iniziale)")
        print(f"\n📋 Rubriche disponibili:")
        print(f"  1. {rubrica_cinematica.titolo}")
        print(f"  2. {rubrica_energia.titolo}")
        print(f"  3. {rubrica_termo.titolo}")
        print("\n🎯 Ora puoi:")
        print("  • Visualizzarle su http://localhost:5001/rubriche")
        print("  • Modificarle tramite l'interfaccia web")
        print("  • Usarle per valutare le verifiche degli studenti")
        print()

if __name__ == '__main__':
    crea_rubriche_ministeriali()
