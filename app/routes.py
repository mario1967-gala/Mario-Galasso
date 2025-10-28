from flask import current_app as app, render_template, request, jsonify, send_from_directory
from app import db
from app.models import Studente, Materia, Voto, Presenza, Compito, Materiale
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Route principale
@app.route('/')
def index():
    """Homepage dell'applicazione"""
    return render_template('index.html')

# ==================== STUDENTI ====================

@app.route('/studenti')
def studenti():
    """Pagina gestione studenti"""
    return render_template('studenti.html')

@app.route('/api/studenti', methods=['GET'])
def get_studenti():
    """API per ottenere tutti gli studenti"""
    studenti = Studente.query.order_by(Studente.cognome, Studente.nome).all()
    return jsonify([s.to_dict() for s in studenti])

@app.route('/api/studenti/<int:id>', methods=['GET'])
def get_studente(id):
    """API per ottenere un singolo studente"""
    studente = Studente.query.get_or_404(id)
    return jsonify(studente.to_dict())

@app.route('/api/studenti', methods=['POST'])
def create_studente():
    """API per creare un nuovo studente"""
    data = request.get_json()

    try:
        studente = Studente(
            nome=data['nome'],
            cognome=data['cognome'],
            data_nascita=datetime.strptime(data['data_nascita'], '%Y-%m-%d').date(),
            codice_fiscale=data.get('codice_fiscale'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            indirizzo=data.get('indirizzo')
        )

        db.session.add(studente)
        db.session.commit()

        return jsonify({'success': True, 'studente': studente.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/studenti/<int:id>', methods=['PUT'])
def update_studente(id):
    """API per aggiornare uno studente"""
    studente = Studente.query.get_or_404(id)
    data = request.get_json()

    try:
        studente.nome = data.get('nome', studente.nome)
        studente.cognome = data.get('cognome', studente.cognome)
        if 'data_nascita' in data:
            studente.data_nascita = datetime.strptime(data['data_nascita'], '%Y-%m-%d').date()
        studente.codice_fiscale = data.get('codice_fiscale', studente.codice_fiscale)
        studente.email = data.get('email', studente.email)
        studente.telefono = data.get('telefono', studente.telefono)
        studente.indirizzo = data.get('indirizzo', studente.indirizzo)

        db.session.commit()

        return jsonify({'success': True, 'studente': studente.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/studenti/<int:id>', methods=['DELETE'])
def delete_studente(id):
    """API per eliminare uno studente"""
    studente = Studente.query.get_or_404(id)

    try:
        db.session.delete(studente)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== MATERIE ====================

@app.route('/materie')
def materie():
    """Pagina gestione materie"""
    return render_template('materie.html')

@app.route('/api/materie', methods=['GET'])
def get_materie():
    """API per ottenere tutte le materie"""
    materie = Materia.query.order_by(Materia.nome).all()
    return jsonify([m.to_dict() for m in materie])

@app.route('/api/materie/<int:id>', methods=['GET'])
def get_materia(id):
    """API per ottenere una singola materia"""
    materia = Materia.query.get_or_404(id)
    return jsonify(materia.to_dict())

@app.route('/api/materie', methods=['POST'])
def create_materia():
    """API per creare una nuova materia"""
    data = request.get_json()

    try:
        materia = Materia(
            nome=data['nome'],
            descrizione=data.get('descrizione'),
            ore_settimanali=data.get('ore_settimanali'),
            docente=data.get('docente')
        )

        db.session.add(materia)
        db.session.commit()

        return jsonify({'success': True, 'materia': materia.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/materie/<int:id>', methods=['PUT'])
def update_materia(id):
    """API per aggiornare una materia"""
    materia = Materia.query.get_or_404(id)
    data = request.get_json()

    try:
        materia.nome = data.get('nome', materia.nome)
        materia.descrizione = data.get('descrizione', materia.descrizione)
        materia.ore_settimanali = data.get('ore_settimanali', materia.ore_settimanali)
        materia.docente = data.get('docente', materia.docente)

        db.session.commit()

        return jsonify({'success': True, 'materia': materia.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/materie/<int:id>', methods=['DELETE'])
def delete_materia(id):
    """API per eliminare una materia"""
    materia = Materia.query.get_or_404(id)

    try:
        db.session.delete(materia)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== VOTI ====================

@app.route('/voti')
def voti():
    """Pagina gestione voti"""
    return render_template('voti.html')

@app.route('/api/voti', methods=['GET'])
def get_voti():
    """API per ottenere tutti i voti"""
    voti = Voto.query.order_by(Voto.data.desc()).all()
    return jsonify([v.to_dict() for v in voti])

@app.route('/api/voti/studente/<int:studente_id>', methods=['GET'])
def get_voti_studente(studente_id):
    """API per ottenere i voti di uno studente"""
    voti = Voto.query.filter_by(studente_id=studente_id).order_by(Voto.data.desc()).all()
    return jsonify([v.to_dict() for v in voti])

@app.route('/api/voti/materia/<int:materia_id>', methods=['GET'])
def get_voti_materia(materia_id):
    """API per ottenere i voti di una materia"""
    voti = Voto.query.filter_by(materia_id=materia_id).order_by(Voto.data.desc()).all()
    return jsonify([v.to_dict() for v in voti])

@app.route('/api/voti', methods=['POST'])
def create_voto():
    """API per creare un nuovo voto"""
    data = request.get_json()

    try:
        voto = Voto(
            studente_id=data['studente_id'],
            materia_id=data['materia_id'],
            voto=float(data['voto']),
            tipo=data.get('tipo'),
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            note=data.get('note')
        )

        db.session.add(voto)
        db.session.commit()

        return jsonify({'success': True, 'voto': voto.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/voti/<int:id>', methods=['PUT'])
def update_voto(id):
    """API per aggiornare un voto"""
    voto = Voto.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'voto' in data:
            voto.voto = float(data['voto'])
        voto.tipo = data.get('tipo', voto.tipo)
        if 'data' in data:
            voto.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
        voto.note = data.get('note', voto.note)

        db.session.commit()

        return jsonify({'success': True, 'voto': voto.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/voti/<int:id>', methods=['DELETE'])
def delete_voto(id):
    """API per eliminare un voto"""
    voto = Voto.query.get_or_404(id)

    try:
        db.session.delete(voto)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== PRESENZE ====================

@app.route('/presenze')
def presenze():
    """Pagina gestione presenze"""
    return render_template('presenze.html')

@app.route('/api/presenze', methods=['GET'])
def get_presenze():
    """API per ottenere tutte le presenze"""
    presenze = Presenza.query.order_by(Presenza.data.desc()).all()
    return jsonify([p.to_dict() for p in presenze])

@app.route('/api/presenze/studente/<int:studente_id>', methods=['GET'])
def get_presenze_studente(studente_id):
    """API per ottenere le presenze di uno studente"""
    presenze = Presenza.query.filter_by(studente_id=studente_id).order_by(Presenza.data.desc()).all()
    return jsonify([p.to_dict() for p in presenze])

@app.route('/api/presenze', methods=['POST'])
def create_presenza():
    """API per registrare una presenza"""
    data = request.get_json()

    try:
        presenza = Presenza(
            studente_id=data['studente_id'],
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            tipo=data['tipo'],
            giustificata=data.get('giustificata', False),
            note=data.get('note')
        )

        if 'ora_ingresso' in data and data['ora_ingresso']:
            presenza.ora_ingresso = datetime.strptime(data['ora_ingresso'], '%H:%M').time()
        if 'ora_uscita' in data and data['ora_uscita']:
            presenza.ora_uscita = datetime.strptime(data['ora_uscita'], '%H:%M').time()

        db.session.add(presenza)
        db.session.commit()

        return jsonify({'success': True, 'presenza': presenza.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/presenze/<int:id>', methods=['PUT'])
def update_presenza(id):
    """API per aggiornare una presenza"""
    presenza = Presenza.query.get_or_404(id)
    data = request.get_json()

    try:
        presenza.tipo = data.get('tipo', presenza.tipo)
        presenza.giustificata = data.get('giustificata', presenza.giustificata)
        presenza.note = data.get('note', presenza.note)

        if 'ora_ingresso' in data and data['ora_ingresso']:
            presenza.ora_ingresso = datetime.strptime(data['ora_ingresso'], '%H:%M').time()
        if 'ora_uscita' in data and data['ora_uscita']:
            presenza.ora_uscita = datetime.strptime(data['ora_uscita'], '%H:%M').time()

        db.session.commit()

        return jsonify({'success': True, 'presenza': presenza.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/presenze/<int:id>', methods=['DELETE'])
def delete_presenza(id):
    """API per eliminare una presenza"""
    presenza = Presenza.query.get_or_404(id)

    try:
        db.session.delete(presenza)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== COMPITI ====================

@app.route('/compiti')
def compiti():
    """Pagina gestione compiti"""
    return render_template('compiti.html')

@app.route('/api/compiti', methods=['GET'])
def get_compiti():
    """API per ottenere tutti i compiti"""
    compiti = Compito.query.order_by(Compito.data_scadenza).all()
    return jsonify([c.to_dict() for c in compiti])

@app.route('/api/compiti/materia/<int:materia_id>', methods=['GET'])
def get_compiti_materia(materia_id):
    """API per ottenere i compiti di una materia"""
    compiti = Compito.query.filter_by(materia_id=materia_id).order_by(Compito.data_scadenza).all()
    return jsonify([c.to_dict() for c in compiti])

@app.route('/api/compiti', methods=['POST'])
def create_compito():
    """API per creare un nuovo compito"""
    data = request.get_json()

    try:
        compito = Compito(
            materia_id=data['materia_id'],
            titolo=data['titolo'],
            descrizione=data.get('descrizione'),
            tipo=data.get('tipo'),
            data_scadenza=datetime.strptime(data['data_scadenza'], '%Y-%m-%d').date(),
            completato=data.get('completato', False)
        )

        if 'data_assegnazione' in data:
            compito.data_assegnazione = datetime.strptime(data['data_assegnazione'], '%Y-%m-%d').date()

        db.session.add(compito)
        db.session.commit()

        return jsonify({'success': True, 'compito': compito.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/compiti/<int:id>', methods=['PUT'])
def update_compito(id):
    """API per aggiornare un compito"""
    compito = Compito.query.get_or_404(id)
    data = request.get_json()

    try:
        compito.titolo = data.get('titolo', compito.titolo)
        compito.descrizione = data.get('descrizione', compito.descrizione)
        compito.tipo = data.get('tipo', compito.tipo)
        if 'data_scadenza' in data:
            compito.data_scadenza = datetime.strptime(data['data_scadenza'], '%Y-%m-%d').date()
        compito.completato = data.get('completato', compito.completato)

        db.session.commit()

        return jsonify({'success': True, 'compito': compito.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/compiti/<int:id>', methods=['DELETE'])
def delete_compito(id):
    """API per eliminare un compito"""
    compito = Compito.query.get_or_404(id)

    try:
        db.session.delete(compito)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== MATERIALI ====================

@app.route('/materiali')
def materiali():
    """Pagina gestione materiali"""
    return render_template('materiali.html')

@app.route('/api/materiali', methods=['GET'])
def get_materiali():
    """API per ottenere tutti i materiali"""
    materiali = Materiale.query.order_by(Materiale.data_caricamento.desc()).all()
    return jsonify([m.to_dict() for m in materiali])

@app.route('/api/materiali/materia/<int:materia_id>', methods=['GET'])
def get_materiali_materia(materia_id):
    """API per ottenere i materiali di una materia"""
    materiali = Materiale.query.filter_by(materia_id=materia_id).order_by(Materiale.data_caricamento.desc()).all()
    return jsonify([m.to_dict() for m in materiali])

@app.route('/api/materiali', methods=['POST'])
def create_materiale():
    """API per creare un nuovo materiale"""
    data = request.get_json()

    try:
        materiale = Materiale(
            materia_id=data['materia_id'],
            titolo=data['titolo'],
            descrizione=data.get('descrizione'),
            tipo=data.get('tipo'),
            contenuto=data.get('contenuto')
        )

        db.session.add(materiale)
        db.session.commit()

        return jsonify({'success': True, 'materiale': materiale.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/materiali/<int:id>', methods=['PUT'])
def update_materiale(id):
    """API per aggiornare un materiale"""
    materiale = Materiale.query.get_or_404(id)
    data = request.get_json()

    try:
        materiale.titolo = data.get('titolo', materiale.titolo)
        materiale.descrizione = data.get('descrizione', materiale.descrizione)
        materiale.tipo = data.get('tipo', materiale.tipo)
        materiale.contenuto = data.get('contenuto', materiale.contenuto)

        db.session.commit()

        return jsonify({'success': True, 'materiale': materiale.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/materiali/<int:id>', methods=['DELETE'])
def delete_materiale(id):
    """API per eliminare un materiale"""
    materiale = Materiale.query.get_or_404(id)

    try:
        db.session.delete(materiale)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

# ==================== STATISTICHE ====================

@app.route('/api/statistiche')
def get_statistiche():
    """API per ottenere statistiche generali"""
    try:
        stats = {
            'totale_studenti': Studente.query.count(),
            'totale_materie': Materia.query.count(),
            'totale_voti': Voto.query.count(),
            'compiti_da_fare': Compito.query.filter_by(completato=False).count(),
            'media_classe': db.session.query(db.func.avg(Voto.voto)).scalar() or 0
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
