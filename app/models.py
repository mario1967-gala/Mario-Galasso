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
    """Modello per verifiche scritte strutturate"""
    __tablename__ = 'verifiche'

    id = db.Column(db.Integer, primary_key=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materie.id'), nullable=False)
    titolo = db.Column(db.String(200), nullable=False)
    descrizione = db.Column(db.Text)
    argomenti = db.Column(db.Text)  # Argomenti trattati (separati da virgola)
    data_verifica = db.Column(db.Date, nullable=False)
    durata_minuti = db.Column(db.Integer)  # Durata in minuti
    punteggio_totale = db.Column(db.Float, default=0)  # Calcolato automaticamente dalla somma domande
    data_creazione = db.Column(db.DateTime, default=datetime.utcnow)
    generata_ai = db.Column(db.Boolean, default=False)  # Se generata con AI

    # Relazioni
    domande = db.relationship('DomandaVerifica', backref='verifica', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Verifica {self.titolo}>'

    def calcola_punteggio_totale(self):
        """Calcola il punteggio totale dalla somma delle domande"""
        self.punteggio_totale = sum(d.punteggio for d in self.domande)
        return self.punteggio_totale

    def to_dict(self, include_domande=False):
        result = {
            'id': self.id,
            'materia_id': self.materia_id,
            'materia_nome': self.materia.nome,
            'titolo': self.titolo,
            'descrizione': self.descrizione,
            'argomenti': self.argomenti,
            'data_verifica': self.data_verifica.strftime('%Y-%m-%d'),
            'durata_minuti': self.durata_minuti,
            'punteggio_totale': self.punteggio_totale,
            'num_domande': len(self.domande),
            'generata_ai': self.generata_ai,
            'data_creazione': self.data_creazione.strftime('%Y-%m-%d %H:%M')
        }

        if include_domande:
            result['domande'] = [d.to_dict(include_criteri=True) for d in self.domande]

        return result


class DomandaVerifica(db.Model):
    """Modello per le domande di una verifica"""
    __tablename__ = 'domande_verifica'

    id = db.Column(db.Integer, primary_key=True)
    verifica_id = db.Column(db.Integer, db.ForeignKey('verifiche.id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)  # Numero progressivo domanda
    testo = db.Column(db.Text, nullable=False)  # Testo della domanda
    tipo = db.Column(db.String(50), nullable=False)  # aperta, chiusa, multipla, vero_falso, esercizio
    punteggio = db.Column(db.Float, nullable=False)  # Punteggio massimo

    # Per domande chiuse/multiple
    opzioni = db.Column(db.Text)  # JSON con opzioni per domande a scelta multipla
    risposta_corretta = db.Column(db.Text)  # Risposta corretta per domande chiuse

    # Spazio risposta
    righe_risposta = db.Column(db.Integer, default=5)  # Numero di righe per la risposta

    note = db.Column(db.Text)  # Note aggiuntive per il docente

    # Relazioni
    criteri = db.relationship('CriterioValutazione', backref='domanda', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Domanda {self.numero} - {self.verifica.titolo}>'

    def to_dict(self, include_criteri=False):
        result = {
            'id': self.id,
            'verifica_id': self.verifica_id,
            'numero': self.numero,
            'testo': self.testo,
            'tipo': self.tipo,
            'punteggio': self.punteggio,
            'opzioni': self.opzioni,
            'risposta_corretta': self.risposta_corretta,
            'righe_risposta': self.righe_risposta,
            'note': self.note,
            'num_criteri': len(self.criteri)
        }

        if include_criteri:
            result['criteri'] = [c.to_dict() for c in self.criteri]

        return result


class CriterioValutazione(db.Model):
    """Modello per i criteri di valutazione di una domanda"""
    __tablename__ = 'criteri_valutazione'

    id = db.Column(db.Integer, primary_key=True)
    domanda_id = db.Column(db.Integer, db.ForeignKey('domande_verifica.id'), nullable=False)
    descrizione = db.Column(db.Text, nullable=False)  # Descrizione del criterio
    punteggio = db.Column(db.Float, nullable=False)  # Punteggio assegnato a questo criterio
    ordine = db.Column(db.Integer, default=0)  # Ordine di visualizzazione

    def __repr__(self):
        return f'<Criterio {self.descrizione[:30]}... ({self.punteggio}pt)>'

    def to_dict(self):
        return {
            'id': self.id,
            'domanda_id': self.domanda_id,
            'descrizione': self.descrizione,
            'punteggio': self.punteggio,
            'ordine': self.ordine
        }
