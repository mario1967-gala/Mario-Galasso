#!/bin/bash
# Script di Diagnostica e Risoluzione Problemi
# Esegui questo script sul tuo Mac per verificare cosa manca

echo "╔════════════════════════════════════════════════════════╗"
echo "║  🔍 DIAGNOSTICA SEZIONE VERIFICHE                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 1. Verifica directory corrente
echo "1️⃣  Directory corrente:"
pwd
echo ""

# 2. Verifica branch Git
echo "2️⃣  Branch Git attuale:"
git branch --show-current 2>/dev/null || echo "❌ Non è un repository Git"
echo ""

# 3. Verifica file base.html
echo "3️⃣  Verifica base.html contiene 'Verifiche':"
if grep -q "Verifiche" app/templates/base.html 2>/dev/null; then
    echo "✅ Trovato 'Verifiche' in base.html"
    grep -n "Verifiche" app/templates/base.html
else
    echo "❌ NON trovato 'Verifiche' in base.html"
    echo "   Devi fare git pull!"
fi
echo ""

# 4. Verifica file verifiche.html esiste
echo "4️⃣  Verifica template verifiche.html:"
if [ -f "app/templates/verifiche.html" ]; then
    echo "✅ File verifiche.html esiste ($(wc -l < app/templates/verifiche.html) righe)"
else
    echo "❌ File verifiche.html NON ESISTE"
    echo "   Devi fare git pull!"
fi
echo ""

# 5. Verifica JavaScript verifiche.js
echo "5️⃣  Verifica JavaScript verifiche.js:"
if [ -f "app/static/js/verifiche.js" ]; then
    echo "✅ File verifiche.js esiste ($(wc -l < app/static/js/verifiche.js) righe)"
else
    echo "❌ File verifiche.js NON ESISTE"
    echo "   Devi fare git pull!"
fi
echo ""

# 6. Verifica route in routes.py
echo "6️⃣  Verifica route /verifiche in routes.py:"
if grep -q "@app.route('/verifiche')" app/routes.py 2>/dev/null; then
    echo "✅ Route /verifiche trovata"
    grep -n "@app.route('/verifiche')" app/routes.py
else
    echo "❌ Route /verifiche NON trovata"
    echo "   Devi fare git pull!"
fi
echo ""

# 7. Verifica modelli nel file models.py
echo "7️⃣  Verifica nuovi modelli in models.py:"
if grep -q "class Verifica" app/models.py 2>/dev/null; then
    echo "✅ Modello Verifica trovato"
else
    echo "❌ Modello Verifica NON trovato"
    echo "   Devi fare git pull!"
fi
echo ""

# 8. Verifica porta in run.py
echo "8️⃣  Porta configurata in run.py:"
grep "port=" run.py 2>/dev/null || echo "❌ File run.py non trovato"
echo ""

# 9. Verifica database
echo "9️⃣  Verifica database:"
if [ -f "instance/didattica.db" ]; then
    echo "✅ Database esiste"
    echo "   Dimensione: $(du -h instance/didattica.db | cut -f1)"
else
    echo "⚠️  Database NON esiste"
    echo "   Devi eseguire: python3 init_db.py"
fi
echo ""

# 10. Riepilogo e Soluzioni
echo "╔════════════════════════════════════════════════════════╗"
echo "║  📋 RIEPILOGO E SOLUZIONI                              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Conta quanti problemi ci sono
problems=0
[ ! -f "app/templates/verifiche.html" ] && problems=$((problems+1))
[ ! -f "app/static/js/verifiche.js" ] && problems=$((problems+1))
grep -q "Verifiche" app/templates/base.html 2>/dev/null || problems=$((problems+1))
grep -q "@app.route('/verifiche')" app/routes.py 2>/dev/null || problems=$((problems+1))

if [ $problems -gt 0 ]; then
    echo "❌ PROBLEMI TROVATI: $problems"
    echo ""
    echo "🔧 SOLUZIONE - Esegui questi comandi:"
    echo ""
    echo "   git pull origin claude/setup-educational-app-011CUfVBpyezLUxJdQVXzUPC"
    echo "   python3 init_db.py"
    echo "   python3 run.py"
    echo ""
    echo "Poi apri: http://localhost:5001"
else
    echo "✅ TUTTO OK! I file sono corretti."
    echo ""
    echo "🔧 PROVA QUESTI PASSAGGI:"
    echo ""
    echo "1. Assicurati che l'app sia avviata:"
    echo "   python3 run.py"
    echo ""
    echo "2. Apri il browser su:"
    echo "   http://localhost:5001"
    echo ""
    echo "3. Svuota la cache del browser:"
    echo "   CMD+SHIFT+R (Mac) o CTRL+F5 (Windows)"
    echo ""
    echo "4. Controlla la console del browser per errori"
fi
echo ""
