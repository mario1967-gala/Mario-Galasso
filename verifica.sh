#!/bin/bash
# Script di verifica installazione

echo "========================================="
echo "🔍 Verifica Installazione"
echo "========================================="
echo ""

# Verifica directory
echo "📁 Directory corrente:"
pwd
echo ""

# Verifica Python
echo "🐍 Versione Python:"
if command -v python3 &> /dev/null; then
    python3 --version
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    python --version
    PYTHON_CMD="python"
else
    echo "❌ Python non trovato! Installa Python 3.8+"
    exit 1
fi
echo ""

# Verifica pip
echo "📦 Versione pip:"
if command -v pip3 &> /dev/null; then
    pip3 --version
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    pip --version
    PIP_CMD="pip"
else
    echo "❌ pip non trovato!"
    exit 1
fi
echo ""

# Verifica file principali
echo "📄 File principali:"
files=("run.py" "requirements.txt" "config.py" "README.md")
all_files_exist=true

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MANCANTE"
        all_files_exist=false
    fi
done
echo ""

# Verifica cartella app
echo "📂 Cartella app/:"
if [ -d "app" ]; then
    echo "  ✅ app/"
    app_files=("__init__.py" "models.py" "routes.py" "utils.py")
    for file in "${app_files[@]}"; do
        if [ -f "app/$file" ]; then
            echo "  ✅ app/$file"
        else
            echo "  ❌ app/$file MANCANTE"
            all_files_exist=false
        fi
    done
else
    echo "  ❌ Cartella app/ MANCANTE"
    all_files_exist=false
fi
echo ""

# Verifica branch git
echo "🌿 Branch Git:"
if [ -d ".git" ]; then
    git branch --show-current
else
    echo "  ⚠️  Non è un repository git"
fi
echo ""

# Risultato finale
echo "========================================="
if [ "$all_files_exist" = true ]; then
    echo "✅ TUTTO OK! Puoi procedere con:"
    echo ""
    echo "1. Installa dipendenze:"
    echo "   $PIP_CMD install -r requirements.txt"
    echo ""
    echo "2. (Opzionale) Popola database:"
    echo "   $PYTHON_CMD seed_data.py"
    echo ""
    echo "3. Avvia applicazione:"
    echo "   $PYTHON_CMD run.py"
    echo ""
    echo "4. Apri browser su: http://localhost:5001"
else
    echo "❌ ALCUNI FILE MANCANO"
    echo ""
    echo "Possibili soluzioni:"
    echo "1. Sei nella directory sbagliata? Vai in Mario-Galasso/"
    echo "2. Repository non clonato? Esegui:"
    echo "   git clone https://github.com/mario1967-gala/Mario-Galasso.git"
    echo "   cd Mario-Galasso"
    echo "   git checkout claude/high-school-class-management-011CUZ8aJ7hnNBgABX1RahdM"
fi
echo "========================================="
