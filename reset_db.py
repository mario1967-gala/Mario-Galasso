#!/usr/bin/env python3
"""
Script per resettare il database dell'applicazione scolastica.
Cancella il database esistente e ne crea uno nuovo con lo schema aggiornato.
"""

import os
import sys

def reset_database():
    """Cancella e ricrea il database"""

    # Percorso del database
    db_path = 'instance/scuola.db'

    print("=" * 60)
    print("RESET DATABASE - Applicazione Gestione Didattica")
    print("=" * 60)
    print()

    # Controlla se il database esiste
    if os.path.exists(db_path):
        print(f"✓ Database trovato: {db_path}")

        # Chiedi conferma
        risposta = input("\n⚠️  ATTENZIONE: Tutti i dati saranno cancellati!\n   Vuoi continuare? (si/no): ")

        if risposta.lower() not in ['si', 'sì', 's', 'yes', 'y']:
            print("\n❌ Operazione annullata.")
            return False

        # Cancella il database
        try:
            os.remove(db_path)
            print(f"\n✓ Database cancellato: {db_path}")
        except Exception as e:
            print(f"\n❌ Errore nella cancellazione: {e}")
            print("\n💡 Suggerimento: Assicurati che l'applicazione NON sia in esecuzione!")
            return False
    else:
        print(f"ℹ️  Database non trovato (verrà creato al primo avvio)")

    # Crea la directory instance se non esiste
    os.makedirs('instance', exist_ok=True)
    print("✓ Directory instance pronta")

    # Importa l'app e crea il database
    print("\n🔄 Creazione nuovo database con schema aggiornato...")

    try:
        from app import create_app, db

        app = create_app()
        with app.app_context():
            db.create_all()
            print("✓ Database creato con successo!")
            print("\n📋 Schema database:")
            print("   - Studenti (data_nascita OPZIONALE)")
            print("   - Classi")
            print("   - Materie")
            print("   - Voti")
            print("   - Presenze")
            print("   - Compiti")
            print("   - Materiali")
            print("   - Verifiche (con esercizi multipli)")
            print("   - Esercizi (con peso e punteggio max)")
            print("   - Voti Esercizi (voti per singolo esercizio)")

        print("\n" + "=" * 60)
        print("✅ RESET COMPLETATO!")
        print("=" * 60)
        print("\n💡 Ora puoi avviare l'applicazione con: python3 run.py")
        print("   E importare gli studenti da screenshot!")
        print()

        return True

    except Exception as e:
        print(f"\n❌ Errore nella creazione del database: {e}")
        return False

if __name__ == '__main__':
    success = reset_database()
    sys.exit(0 if success else 1)
