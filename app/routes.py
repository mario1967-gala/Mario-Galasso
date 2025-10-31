from flask import current_app as app, render_template, request, jsonify, send_from_directory
from app import db
from app.models import (Classe, Studente, Materia, Voto, Presenza, Compito, Materiale,
                        Verifica, DomandaVerifica, CriterioValutazione)
from app.utils import StudentExtractor
from datetime import datetime
import os
import json
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

# ==================== IMPORT DA SCREENSHOT ====================

@app.route('/studenti/import')
def import_studenti():
    """Pagina per import studenti da screenshot"""
    return render_template('import_studenti.html')

@app.route('/api/studenti/upload-screenshot', methods=['POST'])
def upload_screenshot():
    """API per caricare e processare uno screenshot usando Claude AI Vision"""
    if 'screenshot' not in request.files:
        return jsonify({'success': False, 'error': 'Nessun file caricato'}), 400

    file = request.files['screenshot']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nessun file selezionato'}), 400

    # Verifica che sia un'immagine
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        return jsonify({'success': False, 'error': 'Formato file non supportato'}), 400

    try:
        # Ottieni API key dal form data o dalla variabile d'ambiente
        api_key = request.form.get('api_key') or os.environ.get('ANTHROPIC_API_KEY')

        if not api_key:
            return jsonify({
                'success': False,
                'error': 'Chiave API di Anthropic non fornita. Inserisci la chiave API o configurala come variabile d\'ambiente ANTHROPIC_API_KEY.'
            }), 400

        # Salva il file temporaneamente
        filename = secure_filename(file.filename)
        upload_folder = app.config.get('UPLOAD_FOLDER')
        temp_path = os.path.join(upload_folder, f'temp_{filename}')

        # Assicurati che la cartella esista
        os.makedirs(upload_folder, exist_ok=True)

        file.save(temp_path)

        # Estrai i dati dall'immagine usando Claude AI Vision
        try:
            students_data = StudentExtractor.extract_from_image(temp_path, api_key=api_key)
        except ValueError as e:
            # Errore di configurazione API key
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        except Exception as e:
            # Altri errori
            return jsonify({
                'success': False,
                'error': f'Errore nell\'analisi dell\'immagine con Claude AI: {str(e)}'
            }), 500

        # Rimuovi il file temporaneo
        try:
            os.remove(temp_path)
        except:
            pass

        return jsonify({
            'success': True,
            'students': students_data,
            'count': len(students_data),
            'message': f'Claude AI ha estratto {len(students_data)} studenti dall\'immagine'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/studenti/parse-text', methods=['POST'])
def parse_text():
    """API per estrarre studenti da testo strutturato"""
    data = request.get_json()

    if 'text' not in data:
        return jsonify({'success': False, 'error': 'Nessun testo fornito'}), 400

    try:
        students_data = StudentExtractor.extract_from_structured_text(data['text'])

        return jsonify({
            'success': True,
            'students': students_data,
            'count': len(students_data)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/studenti/batch-import', methods=['POST'])
def batch_import_studenti():
    """API per importare multipli studenti in una volta"""
    data = request.get_json()

    if 'students' not in data or not isinstance(data['students'], list):
        return jsonify({'success': False, 'error': 'Dati non validi'}), 400

    try:
        imported_count = 0
        errors = []

        # Classe_id predefinita per tutti gli studenti (opzionale)
        default_classe_id = data.get('classe_id')

        for student_data in data['students']:
            try:
                # Valida i dati obbligatori
                if not student_data.get('nome') or not student_data.get('cognome'):
                    errors.append(f"Studente saltato: nome e cognome obbligatori")
                    continue

                # Usa classe_id specifico dello studente, altrimenti usa quello predefinito
                classe_id = student_data.get('classe_id', default_classe_id)

                # Crea lo studente
                studente = Studente(
                    classe_id=classe_id,
                    nome=student_data['nome'],
                    cognome=student_data['cognome'],
                    data_nascita=datetime.strptime(student_data['data_nascita'], '%Y-%m-%d').date() if student_data.get('data_nascita') else None,
                    codice_fiscale=student_data.get('codice_fiscale'),
                    email=student_data.get('email'),
                    telefono=student_data.get('telefono'),
                    indirizzo=student_data.get('indirizzo')
                )

                db.session.add(studente)
                imported_count += 1

            except Exception as e:
                errors.append(f"Errore con {student_data.get('cognome', 'studente')}: {str(e)}")

        db.session.commit()

        return jsonify({
            'success': True,
            'imported': imported_count,
            'errors': errors
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== CLASSI ====================

@app.route('/classi')
def classi():
    """Pagina gestione classi"""
    return render_template('classi.html')

@app.route('/api/classi', methods=['GET'])
def get_classi():
    """API per ottenere tutte le classi"""
    classi_list = Classe.query.order_by(Classe.anno, Classe.sezione).all()
    return jsonify([classe.to_dict() for classe in classi_list])

@app.route('/api/classi/<int:classe_id>', methods=['GET'])
def get_classe(classe_id):
    """API per ottenere una classe specifica"""
    classe = Classe.query.get_or_404(classe_id)
    return jsonify(classe.to_dict())

@app.route('/api/classi', methods=['POST'])
def create_classe():
    """API per creare una nuova classe"""
    data = request.get_json()

    try:
        classe = Classe(
            nome=data['nome'],
            anno=data['anno'],
            sezione=data['sezione'],
            indirizzo=data.get('indirizzo'),
            anno_scolastico=data['anno_scolastico'],
            note=data.get('note')
        )

        db.session.add(classe)
        db.session.commit()

        return jsonify(classe.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/classi/<int:classe_id>', methods=['PUT'])
def update_classe(classe_id):
    """API per aggiornare una classe"""
    classe = Classe.query.get_or_404(classe_id)
    data = request.get_json()

    try:
        classe.nome = data.get('nome', classe.nome)
        classe.anno = data.get('anno', classe.anno)
        classe.sezione = data.get('sezione', classe.sezione)
        classe.indirizzo = data.get('indirizzo', classe.indirizzo)
        classe.anno_scolastico = data.get('anno_scolastico', classe.anno_scolastico)
        classe.note = data.get('note', classe.note)

        db.session.commit()

        return jsonify(classe.to_dict())

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/classi/<int:classe_id>', methods=['DELETE'])
def delete_classe(classe_id):
    """API per eliminare una classe"""
    classe = Classe.query.get_or_404(classe_id)

    try:
        db.session.delete(classe)
        db.session.commit()
        return jsonify({'message': 'Classe eliminata con successo'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/classi/<int:classe_id>/studenti', methods=['GET'])
def get_studenti_classe(classe_id):
    """API per ottenere tutti gli studenti di una classe"""
    classe = Classe.query.get_or_404(classe_id)
    studenti = Studente.query.filter_by(classe_id=classe_id).order_by(Studente.cognome, Studente.nome).all()
    return jsonify([studente.to_dict() for studente in studenti])

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


# ==================== VERIFICHE ====================

@app.route('/verifiche')
def verifiche():
    """Pagina gestione verifiche scritte"""
    return render_template('verifiche.html')

@app.route('/api/verifiche', methods=['GET'])
def get_verifiche():
    """API per ottenere tutte le verifiche"""
    verifiche = Verifica.query.order_by(Verifica.data_verifica.desc()).all()
    return jsonify([v.to_dict() for v in verifiche])

@app.route('/api/verifiche/<int:id>', methods=['GET'])
def get_verifica(id):
    """API per ottenere una verifica con tutte le domande e criteri"""
    verifica = Verifica.query.get_or_404(id)
    return jsonify(verifica.to_dict(include_domande=True))

@app.route('/api/verifiche/materia/<int:materia_id>', methods=['GET'])
def get_verifiche_materia(materia_id):
    """API per ottenere le verifiche di una materia"""
    verifiche = Verifica.query.filter_by(materia_id=materia_id).order_by(Verifica.data_verifica.desc()).all()
    return jsonify([v.to_dict() for v in verifiche])

@app.route('/api/verifiche', methods=['POST'])
def create_verifica():
    """API per creare una nuova verifica con domande e criteri"""
    data = request.get_json()

    try:
        # Crea la verifica
        verifica = Verifica(
            materia_id=data['materia_id'],
            titolo=data['titolo'],
            descrizione=data.get('descrizione'),
            argomenti=data.get('argomenti'),
            data_verifica=datetime.strptime(data['data_verifica'], '%Y-%m-%d').date(),
            durata_minuti=data.get('durata_minuti'),
            generata_ai=data.get('generata_ai', False)
        )

        db.session.add(verifica)
        db.session.flush()  # Per ottenere l'ID della verifica

        # Aggiungi le domande se presenti
        if 'domande' in data and data['domande']:
            for idx, domanda_data in enumerate(data['domande'], start=1):
                domanda = DomandaVerifica(
                    verifica_id=verifica.id,
                    numero=domanda_data.get('numero', idx),
                    testo=domanda_data['testo'],
                    tipo=domanda_data.get('tipo', 'aperta'),
                    punteggio=float(domanda_data['punteggio']),
                    opzioni=domanda_data.get('opzioni'),
                    risposta_corretta=domanda_data.get('risposta_corretta'),
                    righe_risposta=domanda_data.get('righe_risposta', 5),
                    note=domanda_data.get('note')
                )

                db.session.add(domanda)
                db.session.flush()  # Per ottenere l'ID della domanda

                # Aggiungi i criteri di valutazione se presenti
                if 'criteri' in domanda_data and domanda_data['criteri']:
                    for ordine, criterio_data in enumerate(domanda_data['criteri']):
                        criterio = CriterioValutazione(
                            domanda_id=domanda.id,
                            descrizione=criterio_data['descrizione'],
                            punteggio=float(criterio_data['punteggio']),
                            ordine=criterio_data.get('ordine', ordine)
                        )
                        db.session.add(criterio)

        # Calcola il punteggio totale
        verifica.calcola_punteggio_totale()

        db.session.commit()

        return jsonify({'success': True, 'verifica': verifica.to_dict(include_domande=True)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/verifiche/<int:id>', methods=['PUT'])
def update_verifica(id):
    """API per aggiornare una verifica (solo metadati, non domande)"""
    verifica = Verifica.query.get_or_404(id)
    data = request.get_json()

    try:
        verifica.titolo = data.get('titolo', verifica.titolo)
        verifica.descrizione = data.get('descrizione', verifica.descrizione)
        verifica.argomenti = data.get('argomenti', verifica.argomenti)

        if 'data_verifica' in data:
            verifica.data_verifica = datetime.strptime(data['data_verifica'], '%Y-%m-%d').date()

        verifica.durata_minuti = data.get('durata_minuti', verifica.durata_minuti)

        db.session.commit()

        return jsonify({'success': True, 'verifica': verifica.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/verifiche/<int:id>', methods=['DELETE'])
def delete_verifica(id):
    """API per eliminare una verifica (cancella anche domande e criteri per cascade)"""
    verifica = Verifica.query.get_or_404(id)

    try:
        db.session.delete(verifica)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== DOMANDE VERIFICA ====================

@app.route('/api/verifiche/<int:verifica_id>/domande', methods=['POST'])
def create_domanda(verifica_id):
    """API per aggiungere una domanda a una verifica esistente"""
    verifica = Verifica.query.get_or_404(verifica_id)
    data = request.get_json()

    try:
        # Calcola il numero progressivo
        max_numero = db.session.query(db.func.max(DomandaVerifica.numero)).filter_by(verifica_id=verifica_id).scalar() or 0

        domanda = DomandaVerifica(
            verifica_id=verifica_id,
            numero=data.get('numero', max_numero + 1),
            testo=data['testo'],
            tipo=data.get('tipo', 'aperta'),
            punteggio=float(data['punteggio']),
            opzioni=data.get('opzioni'),
            risposta_corretta=data.get('risposta_corretta'),
            righe_risposta=data.get('righe_risposta', 5),
            note=data.get('note')
        )

        db.session.add(domanda)
        db.session.flush()

        # Aggiungi i criteri se presenti
        if 'criteri' in data and data['criteri']:
            for ordine, criterio_data in enumerate(data['criteri']):
                criterio = CriterioValutazione(
                    domanda_id=domanda.id,
                    descrizione=criterio_data['descrizione'],
                    punteggio=float(criterio_data['punteggio']),
                    ordine=criterio_data.get('ordine', ordine)
                )
                db.session.add(criterio)

        # Ricalcola punteggio totale
        verifica.calcola_punteggio_totale()

        db.session.commit()

        return jsonify({'success': True, 'domanda': domanda.to_dict(include_criteri=True)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/domande/<int:id>', methods=['PUT'])
def update_domanda(id):
    """API per aggiornare una domanda"""
    domanda = DomandaVerifica.query.get_or_404(id)
    data = request.get_json()

    try:
        domanda.testo = data.get('testo', domanda.testo)
        domanda.tipo = data.get('tipo', domanda.tipo)
        domanda.punteggio = float(data.get('punteggio', domanda.punteggio))
        domanda.opzioni = data.get('opzioni', domanda.opzioni)
        domanda.risposta_corretta = data.get('risposta_corretta', domanda.risposta_corretta)
        domanda.righe_risposta = data.get('righe_risposta', domanda.righe_risposta)
        domanda.note = data.get('note', domanda.note)

        # Ricalcola punteggio totale della verifica
        domanda.verifica.calcola_punteggio_totale()

        db.session.commit()

        return jsonify({'success': True, 'domanda': domanda.to_dict(include_criteri=True)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/domande/<int:id>', methods=['DELETE'])
def delete_domanda(id):
    """API per eliminare una domanda"""
    domanda = DomandaVerifica.query.get_or_404(id)
    verifica = domanda.verifica

    try:
        db.session.delete(domanda)

        # Ricalcola punteggio totale
        verifica.calcola_punteggio_totale()

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== CRITERI VALUTAZIONE ====================

@app.route('/api/domande/<int:domanda_id>/criteri', methods=['POST'])
def create_criterio(domanda_id):
    """API per aggiungere un criterio di valutazione a una domanda"""
    domanda = DomandaVerifica.query.get_or_404(domanda_id)
    data = request.get_json()

    try:
        # Calcola l'ordine
        max_ordine = db.session.query(db.func.max(CriterioValutazione.ordine)).filter_by(domanda_id=domanda_id).scalar() or -1

        criterio = CriterioValutazione(
            domanda_id=domanda_id,
            descrizione=data['descrizione'],
            punteggio=float(data['punteggio']),
            ordine=data.get('ordine', max_ordine + 1)
        )

        db.session.add(criterio)
        db.session.commit()

        return jsonify({'success': True, 'criterio': criterio.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/criteri/<int:id>', methods=['PUT'])
def update_criterio(id):
    """API per aggiornare un criterio di valutazione"""
    criterio = CriterioValutazione.query.get_or_404(id)
    data = request.get_json()

    try:
        criterio.descrizione = data.get('descrizione', criterio.descrizione)
        criterio.punteggio = float(data.get('punteggio', criterio.punteggio))
        criterio.ordine = data.get('ordine', criterio.ordine)

        db.session.commit()

        return jsonify({'success': True, 'criterio': criterio.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/criteri/<int:id>', methods=['DELETE'])
def delete_criterio(id):
    """API per eliminare un criterio di valutazione"""
    criterio = CriterioValutazione.query.get_or_404(id)

    try:
        db.session.delete(criterio)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


# ==================== GENERATORE AI VERIFICHE ====================

@app.route('/api/verifiche/genera-ai', methods=['POST'])
def genera_verifica_ai():
    """API per generare una verifica con Claude AI"""
    data = request.get_json()

    try:
        import anthropic

        # Ottieni API key (dovrebbe essere in variabile d'ambiente o config)
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({'success': False, 'error': 'ANTHROPIC_API_KEY non configurata'}), 400

        client = anthropic.Anthropic(api_key=api_key)

        # Parametri per la generazione
        materia_id = data['materia_id']
        materia = Materia.query.get_or_404(materia_id)

        argomenti = data.get('argomenti', '')
        num_domande = data.get('num_domande', 5)
        difficolta = data.get('difficolta', 'media')  # bassa, media, alta
        tipo_domande = data.get('tipo_domande', 'misto')  # aperta, multipla, misto
        punteggio_totale = data.get('punteggio_totale', 10)

        # Crea il prompt per Claude
        prompt = f"""Genera una verifica scritta per la materia {materia.nome}.

PARAMETRI:
- Argomenti: {argomenti}
- Numero domande: {num_domande}
- Difficoltà: {difficolta}
- Tipo domande: {tipo_domande}
- Punteggio totale: {punteggio_totale}

Genera la verifica in formato JSON con questa struttura:
{{
  "titolo": "Titolo della verifica",
  "descrizione": "Breve descrizione della verifica",
  "domande": [
    {{
      "numero": 1,
      "testo": "Testo della domanda",
      "tipo": "aperta|multipla|vero_falso|esercizio",
      "punteggio": 2.0,
      "opzioni": "A) ... B) ... C) ...",
      "risposta_corretta": "Risposta corretta se domanda chiusa",
      "righe_risposta": 5,
      "criteri": [
        {{
          "descrizione": "Criterio di valutazione 1",
          "punteggio": 1.0
        }},
        {{
          "descrizione": "Criterio di valutazione 2",
          "punteggio": 1.0
        }}
      ]
    }}
  ]
}}

IMPORTANTE:
- Per domande aperte, crea sempre criteri di valutazione dettagliati
- La somma dei punteggi delle domande deve essere {punteggio_totale}
- Per domande multiple choice, specifica le opzioni e la risposta corretta
- Rendi le domande appropriate per il livello di difficoltà richiesto
- Rispondi SOLO con il JSON, senza testo aggiuntivo"""

        # Chiamata a Claude
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Estrai il JSON dalla risposta
        response_text = message.content[0].text

        # Trova il JSON nella risposta (potrebbe essere wrappato in ```json)
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        verifica_data = json.loads(response_text)

        # Restituisci i dati generati (NON salvarli ancora nel DB)
        return jsonify({
            'success': True,
            'verifica_data': verifica_data,
            'message': 'Verifica generata con successo. Rivedi e salva.'
        })

    except anthropic.APIError as e:
        return jsonify({'success': False, 'error': f'Errore API Claude: {str(e)}'}), 400
    except json.JSONDecodeError as e:
        return jsonify({'success': False, 'error': f'Errore parsing JSON: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
