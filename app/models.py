from datetime import datetime
from app import db

class Classe(db.Model):
    """Modello per le classi del liceo"""
    __tablename__ = 'classi'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)  # es: "3A Scientifico"
    anno = db.Column(db.Integer, nullable=False)  # es: 3
    sezione = db.Column(db.String(10), nullable=False)  # es: "A"
    indirizzo = db.Column(db.String(100))  # es: "Scientifico"
    anno_scolastico = db.Column(db.String(20), nullable=False)  # es: "2024/2025"
    note = db.Column(db.Text)

    # Relazioni
    studenti = db.relationship('Studente', backref='classe', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Classe {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'anno': self.anno,
            'sezione': self.sezione,
            'indirizzo': self.indirizzo,
            'anno_scolastico': self.anno_scolastico,
            'note': self.note,
            'num_studenti': len(self.studenti)
        }


class Studente(db.Model):
    """Modello per gli studenti della classe"""
    __tablename__ = 'studenti'

    id = db.Column(db.Integer, primary_key=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classi.id'), nullable=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    data_nascita = db.Column(db.Date, nullable=True)
    codice_fiscale = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(120), unique=True)
    telefono = db.Column(db.String(20))
    indirizzo = db.Column(db.String(200))
    data_iscrizione = db.Column(db.DateTime, default=datetime.utcnow)

    # Relazioni
    voti = db.relationship('Voto', backref='studente', lazy=True, cascade='all, delete-orphan')
    presenze = db.relationship('Presenza', backref='studente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Studente {self.cognome} {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'classe_id': self.classe_id,
            'classe_nome': self.classe.nome if self.classe else None,
            'nome': self.nome,
            'cognome': self.cognome,
            'data_nascita': self.data_nascita.strftime('%Y-%m-%d') if self.data_nascita else None,
            'codice_fiscale': self.codice_fiscale,
            'email': self.email,
            'telefono': self.telefono,
            'indirizzo': self.indirizzo
        }


class Materia(db.Model):
    """Modello per le materie del liceo scientifico"""
    __tablename__ = 'materie'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descrizione = db.Column(db.Text)
    ore_settimanali = db.Column(db.Integer)
    docente = db.Column(db.String(100))

    # Relazioni
    voti = db.relationship('Voto', backref='materia', lazy=True, cascade='all, delete-orphan')
    compiti = db.relationship('Compito', backref='materia', lazy=True, cascade='all, delete-orphan')
    materiali = db.relationship('Materiale', backref='materia', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Materia {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descrizione': self.descrizione,
            'ore_settimanali': self.ore_settimanali,
            'docente': self.docente
        }


class Voto(db.Model):
    """Modello per i voti degli studenti"""
    __tablename__ = 'voti'

    id = db.Column(db.Integer, primary_key=True)
    studente_id = db.Column(db.Integer, db.ForeignKey('studenti.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    voto = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50))  # scritto, orale, pratico, ecc.
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    note = db.Column(db.Text)

    def __repr__(self):
        return f'<Voto {self.voto} - {self.studente.cognome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'studente_id': self.studente_id,
            'studente_nome': f"{self.studente.cognome} {self.studente.nome}",
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'voto': self.voto,
            'tipo': self.tipo,
            'data': self.data.strftime('%Y-%m-%d'),
            'note': self.note
        }


class Presenza(db.Model):
    """Modello per le presenze/assenze degli studenti"""
    __tablename__ = 'presenze'

    id = db.Column(db.Integer, primary_key=True)
    studente_id = db.Column(db.Integer, db.ForeignKey('studenti.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # presente, assente, ritardo, uscita_anticipata
    ora_ingresso = db.Column(db.Time)  # per i ritardi
    ora_uscita = db.Column(db.Time)  # per le uscite anticipate
    giustificata = db.Column(db.Boolean, default=False)
    note = db.Column(db.Text)

    def __repr__(self):
        return f'<Presenza {self.studente.cognome} - {self.data} - {self.tipo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'studente_id': self.studente_id,
            'studente_nome': f"{self.studente.cognome} {self.studente.nome}",
            'data': self.data.strftime('%Y-%m-%d'),
            'tipo': self.tipo,
            'ora_ingresso': self.ora_ingresso.strftime('%H:%M') if self.ora_ingresso else None,
            'ora_uscita': self.ora_uscita.strftime('%H:%M') if self.ora_uscita else None,
            'giustificata': self.giustificata,
            'note': self.note
        }


class Compito(db.Model):
    """Modello per compiti e verifiche"""
    __tablename__ = 'compiti'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # compito, verifica_scritta, verifica_orale, progetto
    data_assegnazione = db.Column(db.Date, default=datetime.utcnow)
    data_scadenza = db.Column(db.Date, nullable=False)
    completato = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Compito {self.titolo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'tipo': self.tipo,
            'data_assegnazione': self.data_assegnazione.strftime('%Y-%m-%d'),
            'data_scadenza': self.data_scadenza.strftime('%Y-%m-%d'),
            'completato': self.completato
        }


class Materiale(db.Model):
    """Modello per materiale didattico"""
    __tablename__ = 'materiali'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    tipo = db.Column(db.String(50))  # dispensa, slide, esercizi, link, video
    contenuto = db.Column(db.Text)  # URL o testo
    file_path = db.Column(db.String(300))  # percorso file caricato
    data_caricamento = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Materiale {self.titolo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'tipo': self.tipo,
            'contenuto': self.contenuto,
            'file_path': self.file_path,
            'data_caricamento': self.data_caricamento.strftime('%Y-%m-%d %H:%M')
        }


class Domanda(db.Model):
    """Modello per domande riutilizzabili nel banco domande"""
    __tablename__ = 'domande'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    testo = db.Column(db.Text, nullable=False)  # Testo domanda (può contenere LaTeX)
    argomento = db.Column(db.String(200))  # es: "Equazioni di secondo grado"
    difficolta = db.Column(db.String(20))  # facile, media, difficile
    tipo = db.Column(db.String(50), default='aperta')  # aperta, multipla, vero_falso, etc
    opzioni_json = db.Column(db.Text)  # JSON con opzioni per scelta multipla
    soluzione = db.Column(db.Text)  # Soluzione/risposta corretta (può contenere LaTeX)
    punteggio_default = db.Column(db.Float, default=1.0)
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)

    def __repr__(self):
        return f'<Domanda {self.id} - {self.argomento}>'

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome if self.materia else None,
            'testo': self.testo,
            'argomento': self.argomento,
            'difficolta': self.difficolta,
            'tipo': self.tipo,
            'opzioni_json': self.opzioni_json,
            'soluzione': self.soluzione,
            'punteggio_default': self.punteggio_default,
            'data_creazione': self.data_creazione.strftime('%Y-%m-%d') if self.data_creazione else None,
            'note': self.note
        }


class Verifica(db.Model):
    """Modello per verifiche/test"""
    __tablename__ = 'verifiche'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    argomento = db.Column(db.String(200))
    descrizione = db.Column(db.Text)
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    data_verifica = db.Column(db.Date)  # Data prevista per somministrazione
    durata_minuti = db.Column(db.Integer)  # Durata in minuti
    punteggio_totale = db.Column(db.Float)  # Calcolato automaticamente
    num_versioni = db.Column(db.Integer, default=1)  # Numero di versioni da generare
    mescola_domande = db.Column(db.Boolean, default=False)  # Randomizza ordine domande
    note = db.Column(db.Text)

    # Relazioni
    domande_verifica = db.relationship('DomandaVerifica', backref='verifica', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Verifica {self.titolo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome if self.materia else None,
            'titolo': self.titolo,
            'argomento': self.argomento,
            'descrizione': self.descrizione,
            'data_creazione': self.data_creazione.strftime('%Y-%m-%d %H:%M') if self.data_creazione else None,
            'data_verifica': self.data_verifica.strftime('%Y-%m-%d') if self.data_verifica else None,
            'durata_minuti': self.durata_minuti,
            'punteggio_totale': self.punteggio_totale,
            'num_versioni': self.num_versioni,
            'mescola_domande': self.mescola_domande,
            'num_domande': len(self.domande_verifica),
            'note': self.note
        }


class DomandaVerifica(db.Model):
    """Modello associativo tra Verifica e Domanda (many-to-many con attributi)"""
    __tablename__ = 'domande_verifiche'

    id = db.Column(db.Integer, primary_key=True)
    verifica_id = db.Column(db.Integer, db.ForeignKey('verifiche.id'), nullable=False)
    domanda_id = db.Column(db.Integer, db.ForeignKey('domande.id'), nullable=False)
    ordine = db.Column(db.Integer)  # Ordine della domanda nella verifica
    punteggio = db.Column(db.Float, nullable=False)  # Punteggio specifico per questa verifica

    # Relazioni
    domanda = db.relationship('Domanda', backref='verifiche_associate')

    def __repr__(self):
        return f'<DomandaVerifica V:{self.verifica_id} D:{self.domanda_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'verifica_id': self.verifica_id,
            'domanda_id': self.domanda_id,
            'domanda': self.domanda.to_dict() if self.domanda else None,
            'ordine': self.ordine,
            'punteggio': self.punteggio
        }


class VotoVerifica(db.Model):
    """Modello per salvare i voti delle verifiche corrette"""
    __tablename__ = 'voti_verifiche'

    id = db.Column(db.Integer, primary_key=True)
    verifica_id = db.Column(db.Integer, db.ForeignKey('verifiche.id'), nullable=False)
    studente_id = db.Column(db.Integer, db.ForeignKey('studenti.id'), nullable=False)
    versione = db.Column(db.String(1))  # A, B, C, etc
    punteggio_ottenuto = db.Column(db.Float)
    voto = db.Column(db.Float)  # Voto in decimi
    data_correzione = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.Text)
    inserito_registro = db.Column(db.Boolean, default=False)  # Se inserito nel registro voti

    # Relazioni
    verifica = db.relationship('Verifica', backref='voti_studenti')
    studente = db.relationship('Studente', backref='voti_verifiche')

    def __repr__(self):
        return f'<VotoVerifica V:{self.verifica_id} S:{self.studente_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'verifica_id': self.verifica_id,
            'verifica_titolo': self.verifica.titolo if self.verifica else None,
            'studente_id': self.studente_id,
            'studente_nome': f"{self.studente.cognome} {self.studente.nome}" if self.studente else None,
            'versione': self.versione,
            'punteggio_ottenuto': self.punteggio_ottenuto,
            'voto': self.voto,
            'data_correzione': self.data_correzione.strftime('%Y-%m-%d %H:%M') if self.data_correzione else None,
            'note': self.note,
            'inserito_registro': self.inserito_registro
        }
