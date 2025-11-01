#!/usr/bin/env python3
"""Script per avviare l'applicazione di gestione didattica"""

from app import create_app, db
from app.models import Studente, Materia, Voto, Presenza, Compito, Materiale, Rubrica, Criterio, Descrittore, VotoRubrica

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Crea il contesto per la shell Flask"""
    return {
        'db': db,
        'Studente': Studente,
        'Materia': Materia,
        'Voto': Voto,
        'Presenza': Presenza,
        'Compito': Compito,
        'Materiale': Materiale,
        'Rubrica': Rubrica,
        'Criterio': Criterio,
        'Descrittore': Descrittore,
        'VotoRubrica': VotoRubrica
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
