#!/usr/bin/env python3
"""Script per inizializzare il database con le nuove tabelle"""

from app import create_app, db

def init_database():
    """Crea tutte le tabelle del database"""
    app = create_app()

    with app.app_context():
        print("Creazione database...")
        db.create_all()
        print("✅ Database creato con successo!")

        # Mostra le tabelle create
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print("\nTabelle create:")
        for table in sorted(tables):
            print(f"  - {table}")

if __name__ == '__main__':
    init_database()
