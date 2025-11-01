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


class Rubrica(db.Model):
    """Modello per rubrica di valutazione ministeriale"""
    __tablename__ = 'rubriche'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    tipo_verifica = db.Column(db.String(50))  # scritta, orale, pratica, progetto
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    attiva = db.Column(db.Boolean, default=True)

    # Relazioni
    criteri = db.relationship('Criterio', backref='rubrica', lazy=True, cascade='all, delete-orphan')
    voti_rubrica = db.relationship('VotoRubrica', backref='rubrica', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Rubrica {self.titolo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'tipo_verifica': self.tipo_verifica,
            'data_creazione': self.data_creazione.strftime('%Y-%m-%d %H:%M'),
            'attiva': self.attiva,
            'num_criteri': len(self.criteri)
        }


class Criterio(db.Model):
    """Modello per criteri di valutazione della rubrica"""
    __tablename__ = 'criteri'

    id = db.Column(db.Integer, primary_key=True)
    rubrica_id = db.Column(db.Integer, db.ForeignKey('rubriche.id'), nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    peso = db.Column(db.Float, default=1.0)  # peso del criterio (0-1)
    ordine = db.Column(db.Integer, default=0)  # ordine di visualizzazione

    # Relazioni
    descrittori = db.relationship('Descrittore', backref='criterio', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Criterio {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'rubrica_id': self.rubrica_id,
            'nome': self.nome,
            'descrizione': self.descrizione,
            'peso': self.peso,
            'ordine': self.ordine,
            'descrittori': [d.to_dict() for d in sorted(self.descrittori, key=lambda x: x.livello, reverse=True)]
        }


class Descrittore(db.Model):
    """Modello per descrittori di competenza per ogni livello"""
    __tablename__ = 'descrittori'

    id = db.Column(db.Integer, primary_key=True)
    criterio_id = db.Column(db.Integer, db.ForeignKey('criteri.id'), nullable=False)
    livello = db.Column(db.Integer, nullable=False)  # 4=Avanzato, 3=Intermedio, 2=Base, 1=Iniziale
    livello_nome = db.Column(db.String(50), nullable=False)  # Avanzato, Intermedio, Base, Iniziale
    descrizione = db.Column(db.Text, nullable=False)
    punteggio = db.Column(db.Float, nullable=False)  # punteggio associato (es. 10, 8, 6, 4)

    def __repr__(self):
        return f'<Descrittore {self.livello_nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'criterio_id': self.criterio_id,
            'livello': self.livello,
            'livello_nome': self.livello_nome,
            'descrizione': self.descrizione,
            'punteggio': self.punteggio
        }


class VotoRubrica(db.Model):
    """Modello per valutazione con rubrica - collega voti ai criteri"""
    __tablename__ = 'voti_rubrica'

    id = db.Column(db.Integer, primary_key=True)
    voto_id = db.Column(db.Integer, db.ForeignKey('voti.id'), nullable=False)
    rubrica_id = db.Column(db.Integer, db.ForeignKey('rubriche.id'), nullable=False)
    criterio_id = db.Column(db.Integer, db.ForeignKey('criteri.id'), nullable=False)
    descrittore_id = db.Column(db.Integer, db.ForeignKey('descrittori.id'), nullable=False)
    feedback = db.Column(db.Text)  # feedback specifico per questo criterio

    # Relazioni
    voto = db.relationship('Voto', backref='valutazioni_rubrica')
    criterio = db.relationship('Criterio', backref='valutazioni')
    descrittore = db.relationship('Descrittore', backref='valutazioni')

    def __repr__(self):
        return f'<VotoRubrica Voto:{self.voto_id} Criterio:{self.criterio_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'voto_id': self.voto_id,
            'rubrica_id': self.rubrica_id,
            'criterio_id': self.criterio_id,
            'criterio_nome': self.criterio.nome,
            'descrittore_id': self.descrittore_id,
            'livello': self.descrittore.livello_nome,
            'punteggio': self.descrittore.punteggio,
            'feedback': self.feedback
        }
