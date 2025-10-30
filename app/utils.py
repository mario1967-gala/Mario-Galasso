"""Helper per l'elaborazione di screenshot e estrazione dati studenti usando Claude AI Vision"""

import re
import os
import base64
from datetime import datetime
from typing import List, Dict, Optional

class StudentExtractor:
    """Estrae dati degli studenti da uno screenshot usando Claude AI Vision"""

    @staticmethod
    def extract_from_image(image_path: str, api_key: Optional[str] = None) -> List[Dict]:
        """
        Estrae dati degli studenti da un'immagine usando Claude AI Vision

        Args:
            image_path: Path all'immagine da processare
            api_key: Chiave API di Anthropic (opzionale, può essere in env var)

        Returns:
            Lista di dizionari con i dati degli studenti
        """
        try:
            import anthropic

            # Ottieni API key
            if not api_key:
                api_key = os.environ.get('ANTHROPIC_API_KEY')

            if not api_key:
                raise ValueError("API key di Anthropic non fornita. Configura la chiave API nelle impostazioni.")

            # Leggi l'immagine e convertila in base64
            with open(image_path, 'rb') as image_file:
                image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')

            # Determina il tipo di immagine
            extension = image_path.lower().split('.')[-1]
            media_type_map = {
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            media_type = media_type_map.get(extension, 'image/jpeg')

            # Crea client Anthropic
            client = anthropic.Anthropic(api_key=api_key)

            # Prompt per Claude
            prompt = """Analizza questa immagine che contiene una lista di studenti.

La lista può avere diversi formati. Estrai TUTTI gli studenti che trovi.

Per ogni studente, estrai i dati disponibili:
- Cognome (obbligatorio)
- Nome (obbligatorio)
- Data di nascita (se presente, formato DD/MM/YYYY)
- Email (se presente)
- Telefono (se presente)

IMPORTANTE:
- Se vedi numeri progressivi (1, 2, 3...) ignorali, servono solo come numerazione
- Anche se ci sono SOLO cognome e nome, includili comunque
- Se manca la data di nascita, omettila dal JSON

Rispondi SOLO con un JSON array nel formato:
[
  {
    "cognome": "Rossi",
    "nome": "Mario",
    "data_nascita": "15/03/2007",
    "email": "mario.rossi@example.com",
    "telefono": "3331234567"
  },
  {
    "cognome": "Bianchi",
    "nome": "Laura"
  }
]

Esempi di formati riconosciuti:
- "1. Rossi Mario"
- "2  Bianchi Laura"
- "Verdi Giuseppe - 08/01/2007"
- "Neri Anna, anna.neri@example.com"

Rispondi SOLO con il JSON array, nessun altro testo."""

            # Chiamata all'API di Claude
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # Estrai il testo dalla risposta
            response_text = message.content[0].text

            # Cerca il JSON nella risposta
            import json

            # Prova a estrarre solo il JSON se c'è altro testo
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

            # Parse del JSON
            students_data = json.loads(json_str)

            # Converti le date nel formato corretto (se presenti)
            for student in students_data:
                if 'data_nascita' in student and student['data_nascita']:
                    student['data_nascita'] = StudentExtractor._parse_date(student['data_nascita'])
                else:
                    # Se non c'è data di nascita, rimuovi il campo o mettilo a None
                    student['data_nascita'] = None

            return students_data

        except Exception as e:
            print(f"Errore nell'estrazione con Claude Vision: {str(e)}")
            raise

    @staticmethod
    def _parse_date(date_str: str) -> Optional[str]:
        """Converte una stringa data in formato YYYY-MM-DD"""
        if not date_str:
            return None

        # Sostituisci - con /
        date_str = date_str.replace('-', '/')

        try:
            # Prova formato DD/MM/YYYY
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                # Prova formato YYYY/MM/DD
                date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                try:
                    # Prova formato D/M/YYYY (senza zero padding)
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        day, month, year = parts
                        date_obj = datetime(int(year), int(month), int(day))
                        return date_obj.strftime('%Y-%m-%d')
                except:
                    return None
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
