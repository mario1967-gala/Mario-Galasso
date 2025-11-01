#!/usr/bin/env python3
"""
Script di migrazione database per aggiungere campi Rubrica Ministeriale
Aggiunge i campi: livello, tempo_stimato, distrattori alla tabella domande_verifica
"""

from app import app, db
from sqlalchemy import text

def migrate_db():
    """Esegue la migrazione del database"""

    with app.app_context():
        print("🔄 Inizio migrazione database...")

        try:
            # Controlla se le colonne esistono già
            with db.engine.connect() as conn:
                result = conn.execute(text("PRAGMA table_info(domande_verifica)"))
                columns = [row[1] for row in result]

                print(f"📋 Colonne esistenti: {columns}")

                # Aggiungi colonna 'livello' se non esiste
                if 'livello' not in columns:
                    print("➕ Aggiunta colonna 'livello'...")
                    conn.execute(text(
                        "ALTER TABLE domande_verifica ADD COLUMN livello VARCHAR(20) DEFAULT 'BASE'"
                    ))
                    conn.commit()
                    print("✅ Colonna 'livello' aggiunta")
                else:
                    print("✓ Colonna 'livello' già presente")

                # Aggiungi colonna 'tempo_stimato' se non esiste
                if 'tempo_stimato' not in columns:
                    print("➕ Aggiunta colonna 'tempo_stimato'...")
                    conn.execute(text(
                        "ALTER TABLE domande_verifica ADD COLUMN tempo_stimato INTEGER"
                    ))
                    conn.commit()
                    print("✅ Colonna 'tempo_stimato' aggiunta")
                else:
                    print("✓ Colonna 'tempo_stimato' già presente")

                # Aggiungi colonna 'distrattori' se non esiste
                if 'distrattori' not in columns:
                    print("➕ Aggiunta colonna 'distrattori'...")
                    conn.execute(text(
                        "ALTER TABLE domande_verifica ADD COLUMN distrattori TEXT"
                    ))
                    conn.commit()
                    print("✅ Colonna 'distrattori' aggiunta")
                else:
                    print("✓ Colonna 'distrattori' già presente")

                print("\n✅ Migrazione completata con successo!")
                print("\n📊 Struttura aggiornata:")
                result = conn.execute(text("PRAGMA table_info(domande_verifica)"))
                for row in result:
                    print(f"  - {row[1]}: {row[2]}")

        except Exception as e:
            print(f"\n❌ Errore durante la migrazione: {e}")
            raise

if __name__ == '__main__':
    migrate_db()
