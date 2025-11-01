#!/usr/bin/env python3
"""
Script per configurare la chiave API di Anthropic (Claude AI)
Questo script salva la chiave nel file .env per uso permanente.
"""

import os
import sys

def setup_api_key():
    """Configura la chiave API di Anthropic"""

    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║   Configurazione Chiave API Anthropic (Claude AI)            ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    print("🔑 Questa chiave è OPZIONALE. Serve solo per:")
    print("   - Generare verifiche automaticamente con l'AI")
    print("   - Importare studenti da screenshot")
    print()
    print("   Se non hai una chiave, puoi:")
    print("   1. Premere INVIO per saltare (userai l'app senza AI)")
    print("   2. Ottenere una chiave su: https://console.anthropic.com/")
    print()
    print("─" * 65)
    print()

    # Controlla se esiste già un file .env
    env_file = '.env'
    env_exists = os.path.exists(env_file)

    if env_exists:
        # Leggi il file esistente
        with open(env_file, 'r') as f:
            existing_content = f.read()

        # Controlla se c'è già una chiave
        if 'ANTHROPIC_API_KEY=' in existing_content and \
           not existing_content.split('ANTHROPIC_API_KEY=')[1].split('\n')[0].strip() == '':
            print("✅ Trovata chiave API esistente nel file .env")
            print()
            response = input("Vuoi sostituirla con una nuova chiave? (s/n): ").lower().strip()

            if response != 's':
                print("⏭️  Configurazione saltata. Chiave esistente mantenuta.")
                return

    # Richiedi la chiave all'utente
    print("Inserisci la tua chiave API Anthropic:")
    print("(Inizia con 'sk-ant-...')")
    print()
    api_key = input("API Key: ").strip()

    if not api_key:
        print()
        print("⏭️  Nessuna chiave inserita.")
        print("   L'applicazione funzionerà senza il generatore AI.")
        print("   Potrai sempre configurarla in seguito eseguendo:")
        print("   python3 setup_api_key.py")
        return

    # Valida il formato della chiave
    if not api_key.startswith('sk-ant-'):
        print()
        print("⚠️  ATTENZIONE: La chiave non sembra valida.")
        print("   Le chiavi Anthropic iniziano con 'sk-ant-'")
        print()
        response = input("Vuoi salvarla comunque? (s/n): ").lower().strip()

        if response != 's':
            print("❌ Configurazione annullata.")
            return

    # Crea o aggiorna il file .env
    if env_exists:
        # Leggi il contenuto esistente
        with open(env_file, 'r') as f:
            lines = f.readlines()

        # Aggiorna o aggiungi la chiave
        key_found = False
        new_lines = []

        for line in lines:
            if line.startswith('ANTHROPIC_API_KEY='):
                new_lines.append(f'ANTHROPIC_API_KEY={api_key}\n')
                key_found = True
            else:
                new_lines.append(line)

        if not key_found:
            new_lines.append(f'\n# Chiave API Anthropic (Claude AI)\n')
            new_lines.append(f'ANTHROPIC_API_KEY={api_key}\n')

        # Scrivi il file aggiornato
        with open(env_file, 'w') as f:
            f.writelines(new_lines)
    else:
        # Crea un nuovo file .env
        with open(env_file, 'w') as f:
            f.write('# File di configurazione variabili d\'ambiente\n')
            f.write('# Generato automaticamente da setup_api_key.py\n\n')
            f.write('# Chiave API Anthropic (Claude AI)\n')
            f.write(f'ANTHROPIC_API_KEY={api_key}\n\n')
            f.write('# Chiave segreta Flask (per sessioni e sicurezza)\n')
            f.write('SECRET_KEY=dev-secret-key-change-in-production\n')

    print()
    print("✅ Configurazione completata!")
    print()
    print(f"   La chiave è stata salvata in: {os.path.abspath(env_file)}")
    print("   La chiave verrà caricata automaticamente all'avvio dell'app.")
    print()
    print("🚀 Ora puoi avviare l'applicazione con:")
    print("   python3 run.py")
    print()
    print("🤖 Potrai usare il generatore AI di verifiche!")
    print()


if __name__ == '__main__':
    try:
        setup_api_key()
    except KeyboardInterrupt:
        print("\n\n❌ Configurazione annullata dall'utente.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore durante la configurazione: {e}")
        sys.exit(1)
