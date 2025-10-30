"""Helper per l'elaborazione di screenshot e estrazione dati studenti"""

import re
from datetime import datetime
from typing import List, Dict, Optional
import pytesseract
from PIL import Image

class StudentExtractor:
    """Estrae dati degli studenti da uno screenshot"""

    @staticmethod
    def extract_from_image(image_path: str) -> List[Dict]:
        """
        Estrae dati degli studenti da un'immagine usando OCR

        Args:
            image_path: Path all'immagine da processare

        Returns:
            Lista di dizionari con i dati degli studenti
        """
        try:
            # Carica l'immagine
            image = Image.open(image_path)

            # Estrai il testo usando OCR
            text = pytesseract.image_to_string(image, lang='ita')

            # Parsa il testo per estrarre i dati
            students = StudentExtractor._parse_text(text)

            return students
        except Exception as e:
            print(f"Errore nell'estrazione: {str(e)}")
            return []

    @staticmethod
    def _parse_text(text: str) -> List[Dict]:
        """
        Parsa il testo estratto per trovare i dati degli studenti

        Formati supportati:
        - "Cognome Nome, Data di nascita"
        - "Cognome Nome - DD/MM/YYYY"
        - "Nome Cognome (DD/MM/YYYY)"
        - Righe con nome, cognome e data
        """
        students = []
        lines = text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue

            student_data = StudentExtractor._extract_student_from_line(line)
            if student_data:
                students.append(student_data)

        return students

    @staticmethod
    def _extract_student_from_line(line: str) -> Optional[Dict]:
        """Estrae i dati di uno studente da una riga di testo"""

        # Pattern per date: DD/MM/YYYY o DD-MM-YYYY
        date_pattern = r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})'
        date_match = re.search(date_pattern, line)

        data_nascita = None
        if date_match:
            date_str = date_match.group(1)
            data_nascita = StudentExtractor._parse_date(date_str)
            # Rimuovi la data dalla riga per facilitare l'estrazione del nome
            line = line.replace(date_match.group(0), '').strip()

        # Rimuovi caratteri speciali comuni
        line = re.sub(r'[,\(\)\-\:]', ' ', line)
        line = ' '.join(line.split())  # Normalizza spazi

        # Dividi in parole
        parts = line.split()

        if len(parts) < 2:
            return None

        # Assumi che il primo elemento sia il cognome e il secondo il nome
        # oppure il contrario
        # Prova a identificare quale è quale (i cognomi tendono ad essere in maiuscolo)

        if len(parts) == 2:
            # Caso semplice: due parole
            if parts[0].isupper() or parts[0][0].isupper():
                cognome = parts[0].title()
                nome = parts[1].title()
            else:
                nome = parts[0].title()
                cognome = parts[1].title()
        else:
            # Più di due parole: prendi le prime due
            cognome = parts[0].title()
            nome = parts[1].title()

        return {
            'nome': nome,
            'cognome': cognome,
            'data_nascita': data_nascita
        }

    @staticmethod
    def _parse_date(date_str: str) -> Optional[str]:
        """Converte una stringa data in formato YYYY-MM-DD"""
        # Sostituisci - con /
        date_str = date_str.replace('-', '/')

        try:
            # Prova formato DD/MM/YYYY
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                # Prova formato D/M/YYYY
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                return None

    @staticmethod
    def extract_from_structured_text(text: str) -> List[Dict]:
        """
        Estrae studenti da testo strutturato fornito manualmente

        Formato atteso (uno per riga):
        Cognome Nome, DD/MM/YYYY
        oppure
        Cognome Nome, DD/MM/YYYY, email@example.com
        oppure
        Cognome Nome, DD/MM/YYYY, email@example.com, telefono
        """
        students = []
        lines = text.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = [p.strip() for p in line.split(',')]

            if len(parts) < 2:
                continue

            # Prima parte: Cognome Nome
            name_parts = parts[0].split()
            if len(name_parts) < 2:
                continue

            student = {
                'cognome': name_parts[0].title(),
                'nome': ' '.join(name_parts[1:]).title(),
                'data_nascita': StudentExtractor._parse_date(parts[1]) if len(parts) > 1 else None,
                'email': parts[2] if len(parts) > 2 else None,
                'telefono': parts[3] if len(parts) > 3 else None
            }

            students.append(student)

        return students
