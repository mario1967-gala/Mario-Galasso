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


class Verifica(db.Model):
    """Modello per le verifiche con esercizi multipli"""
    __tablename__ = 'verifiche'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    classe_id = db.Column(db.Integer, db.ForeignKey('classi.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    descrizione = db.Column(db.Text)

    # Relazioni
    materia = db.relationship('Materia', backref='verifiche')
    classe = db.relationship('Classe', backref='verifiche')
    esercizi = db.relationship('Esercizio', backref='verifica', lazy=True, cascade='all, delete-orphan', order_by='Esercizio.numero')

    def __repr__(self):
        return f'<Verifica {self.titolo}>'

    def calcola_voto_studente(self, studente_id):
        """Calcola il voto finale pesato per uno studente"""
        somma_pesata = 0
        somma_pesi = 0

        for esercizio in self.esercizi:
            voto_es = VotoEsercizio.query.filter_by(
                esercizio_id=esercizio.id,
                studente_id=studente_id
            ).first()

            if voto_es and voto_es.punteggio is not None:
                # Normalizza il punteggio su 10
                voto_normalizzato = (voto_es.punteggio / esercizio.punteggio_max) * 10
                somma_pesata += voto_normalizzato * esercizio.peso
                somma_pesi += esercizio.peso

        if somma_pesi == 0:
            return None

        return round(somma_pesata / somma_pesi, 2)

    def to_dict(self):
        return {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'classe_id': self.classe_id,
            'classe_nome': self.classe.nome,
            'titolo': self.titolo,
            'data': self.data.strftime('%Y-%m-%d'),
            'descrizione': self.descrizione,
            'num_esercizi': len(self.esercizi)
        }


class Esercizio(db.Model):
    """Modello per gli esercizi di una verifica"""
    __tablename__ = 'esercizi'

    id = db.Column(db.Integer, primary_key=True)
    verifica_id = db.Column(db.Integer, db.ForeignKey('verifiche.id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)  # Numero progressivo dell'esercizio
    titolo = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    punteggio_max = db.Column(db.Float, nullable=False)  # Punteggio massimo per l'esercizio
    peso = db.Column(db.Integer, nullable=False, default=1)  # Peso da 1 a 10

    # Relazioni
    voti_esercizio = db.relationship('VotoEsercizio', backref='esercizio', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Esercizio {self.numero} - {self.titolo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'verifica_id': self.verifica_id,
            'numero': self.numero,
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'punteggio_max': self.punteggio_max,
            'peso': self.peso
        }


class VotoEsercizio(db.Model):
    """Modello per i voti dei singoli esercizi"""
    __tablename__ = 'voti_esercizi'

    id = db.Column(db.Integer, primary_key=True)
    esercizio_id = db.Column(db.Integer, db.ForeignKey('esercizi.id'), nullable=False)
    studente_id = db.Column(db.Integer, db.ForeignKey('studenti.id'), nullable=False)
    punteggio = db.Column(db.Float)  # Punteggio ottenuto
    note = db.Column(db.Text)

    # Relazioni
    studente = db.relationship('Studente', backref='voti_esercizi')

    def __repr__(self):
        return f'<VotoEsercizio {self.studente.cognome} - Es.{self.esercizio.numero}: {self.punteggio}>'

    def to_dict(self):
        return {
            'id': self.id,
            'esercizio_id': self.esercizio_id,
            'studente_id': self.studente_id,
            'studente_nome': f"{self.studente.cognome} {self.studente.nome}",
            'punteggio': self.punteggio,
            'note': self.note
        }
