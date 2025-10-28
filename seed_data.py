#!/usr/bin/env python3
"""Script per popolare il database con dati di esempio"""

from datetime import datetime, date, timedelta
from app import create_app, db
from app.models import Studente, Materia, Voto, Presenza, Compito, Materiale

app = create_app()

with app.app_context():
    # Pulisci il database
    db.drop_all()
    db.create_all()

    print("Creazione dati di esempio...")

    # Materie tipiche del terzo anno liceo scientifico
    materie_data = [
        {'nome': 'Matematica', 'ore_settimanali': 4, 'docente': 'Prof. Rossi Mario'},
        {'nome': 'Fisica', 'ore_settimanali': 3, 'docente': 'Prof. Bianchi Laura'},
        {'nome': 'Italiano', 'ore_settimanali': 4, 'docente': 'Prof. Verdi Giovanni'},
        {'nome': 'Latino', 'ore_settimanali': 3, 'docente': 'Prof. Neri Anna'},
        {'nome': 'Inglese', 'ore_settimanali': 3, 'docente': 'Prof. Brown John'},
        {'nome': 'Filosofia', 'ore_settimanali': 3, 'docente': 'Prof. Gialli Pietro'},
        {'nome': 'Storia', 'ore_settimanali': 2, 'docente': 'Prof. Verdi Giovanni'},
        {'nome': 'Scienze Naturali', 'ore_settimanali': 3, 'docente': 'Prof. Blu Maria'},
        {'nome': 'Disegno e Storia dell\'Arte', 'ore_settimanali': 2, 'docente': 'Prof. Viola Luca'},
        {'nome': 'Educazione Fisica', 'ore_settimanali': 2, 'docente': 'Prof. Forti Stefano'}
    ]

    materie = []
    for m_data in materie_data:
        materia = Materia(**m_data)
        db.session.add(materia)
        materie.append(materia)

    db.session.commit()
    print(f"✓ Create {len(materie)} materie")

    # Studenti di esempio
    studenti_data = [
        {'nome': 'Marco', 'cognome': 'Alberti', 'data_nascita': date(2007, 3, 15), 'email': 'marco.alberti@example.com'},
        {'nome': 'Giulia', 'cognome': 'Bernardi', 'data_nascita': date(2007, 5, 22), 'email': 'giulia.bernardi@example.com'},
        {'nome': 'Luca', 'cognome': 'Conti', 'data_nascita': date(2007, 1, 8), 'email': 'luca.conti@example.com'},
        {'nome': 'Sara', 'cognome': 'De Luca', 'data_nascita': date(2007, 9, 30), 'email': 'sara.deluca@example.com'},
        {'nome': 'Alessandro', 'cognome': 'Ferrari', 'data_nascita': date(2007, 7, 12), 'email': 'alessandro.ferrari@example.com'},
        {'nome': 'Martina', 'cognome': 'Gallo', 'data_nascita': date(2007, 4, 25), 'email': 'martina.gallo@example.com'},
        {'nome': 'Davide', 'cognome': 'Marino', 'data_nascita': date(2007, 11, 3), 'email': 'davide.marino@example.com'},
        {'nome': 'Chiara', 'cognome': 'Ricci', 'data_nascita': date(2007, 6, 18), 'email': 'chiara.ricci@example.com'},
        {'nome': 'Matteo', 'cognome': 'Romano', 'data_nascita': date(2007, 2, 9), 'email': 'matteo.romano@example.com'},
        {'nome': 'Sofia', 'cognome': 'Santoro', 'data_nascita': date(2007, 8, 14), 'email': 'sofia.santoro@example.com'}
    ]

    studenti = []
    for s_data in studenti_data:
        studente = Studente(**s_data)
        db.session.add(studente)
        studenti.append(studente)

    db.session.commit()
    print(f"✓ Creati {len(studenti)} studenti")

    # Voti di esempio
    import random
    voti_count = 0
    for studente in studenti:
        for materia in random.sample(materie, 5):  # 5 materie casuali per studente
            for _ in range(random.randint(2, 4)):  # 2-4 voti per materia
                voto = Voto(
                    studente_id=studente.id,
                    materia_id=materia.id,
                    voto=round(random.uniform(5.5, 9.5) * 4) / 4,  # voti da 5.5 a 9.5
                    tipo=random.choice(['scritto', 'orale', 'pratico']),
                    data=date.today() - timedelta(days=random.randint(1, 60))
                )
                db.session.add(voto)
                voti_count += 1

    db.session.commit()
    print(f"✓ Creati {voti_count} voti")

    # Presenze di esempio
    presenze_count = 0
    for studente in studenti:
        for i in range(10):  # ultime 10 giorni
            data_presenza = date.today() - timedelta(days=i)
            tipo = random.choices(
                ['presente', 'assente', 'ritardo', 'uscita_anticipata'],
                weights=[0.85, 0.05, 0.07, 0.03]
            )[0]

            presenza = Presenza(
                studente_id=studente.id,
                data=data_presenza,
                tipo=tipo,
                giustificata=tipo != 'presente' and random.choice([True, False])
            )
            db.session.add(presenza)
            presenze_count += 1

    db.session.commit()
    print(f"✓ Create {presenze_count} presenze")

    # Compiti di esempio
    compiti_data = [
        {'materia': 'Matematica', 'titolo': 'Esercizi su derivate', 'tipo': 'compito', 'giorni': 3},
        {'materia': 'Fisica', 'titolo': 'Verifica su termodinamica', 'tipo': 'verifica_scritta', 'giorni': 7},
        {'materia': 'Italiano', 'titolo': 'Analisi del testo - Divina Commedia', 'tipo': 'compito', 'giorni': 5},
        {'materia': 'Latino', 'titolo': 'Traduzione Cicerone', 'tipo': 'compito', 'giorni': 2},
        {'materia': 'Inglese', 'titolo': 'Verifica scritta Present Perfect', 'tipo': 'verifica_scritta', 'giorni': 10},
        {'materia': 'Filosofia', 'titolo': 'Interrogazione su Kant', 'tipo': 'verifica_orale', 'giorni': 6},
        {'materia': 'Scienze Naturali', 'titolo': 'Progetto sulla fotosintesi', 'tipo': 'progetto', 'giorni': 15}
    ]

    compiti = []
    for c_data in compiti_data:
        materia = next(m for m in materie if m.nome == c_data['materia'])
        compito = Compito(
            materia_id=materia.id,
            titolo=c_data['titolo'],
            tipo=c_data['tipo'],
            data_scadenza=date.today() + timedelta(days=c_data['giorni']),
            completato=False
        )
        db.session.add(compito)
        compiti.append(compito)

    db.session.commit()
    print(f"✓ Creati {len(compiti)} compiti")

    # Materiali di esempio
    materiali_data = [
        {'materia': 'Matematica', 'titolo': 'Dispensa sulle derivate', 'tipo': 'dispensa'},
        {'materia': 'Fisica', 'titolo': 'Slide termodinamica', 'tipo': 'slide'},
        {'materia': 'Italiano', 'titolo': 'Esercizi di analisi del testo', 'tipo': 'esercizi'},
        {'materia': 'Inglese', 'titolo': 'Video Present Perfect', 'tipo': 'video', 'contenuto': 'https://example.com/video'},
        {'materia': 'Filosofia', 'titolo': 'Risorse su Kant', 'tipo': 'link', 'contenuto': 'https://example.com/kant'}
    ]

    materiali = []
    for mat_data in materiali_data:
        materia = next(m for m in materie if m.nome == mat_data['materia'])
        materiale = Materiale(
            materia_id=materia.id,
            titolo=mat_data['titolo'],
            tipo=mat_data['tipo'],
            contenuto=mat_data.get('contenuto', '')
        )
        db.session.add(materiale)
        materiali.append(materiale)

    db.session.commit()
    print(f"✓ Creati {len(materiali)} materiali")

    print("\n✓ Database popolato con successo!")
    print(f"\nRiepilogo:")
    print(f"- {len(materie)} materie")
    print(f"- {len(studenti)} studenti")
    print(f"- {voti_count} voti")
    print(f"- {presenze_count} presenze")
    print(f"- {len(compiti)} compiti")
    print(f"- {len(materiali)} materiali didattici")
