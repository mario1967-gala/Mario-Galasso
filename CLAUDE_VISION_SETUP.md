# 🤖 Setup Claude AI Vision per Import Studenti

L'applicazione ora usa **Claude AI Vision** per analizzare gli screenshot e estrarre automaticamente i dati degli studenti. Questo è molto più potente e preciso di OCR tradizionali!

## ✨ Vantaggi di Claude AI Vision

- ✅ **Più accurato**: Claude capisce il contesto e la struttura dei dati
- ✅ **Nessuna installazione locale**: Non serve Tesseract o altre dipendenze complesse
- ✅ **Compatibile con Python 3.13**: Funziona con tutte le versioni moderne di Python
- ✅ **Intelligente**: Riconosce automaticamente nomi, cognomi, date, email, telefoni
- ✅ **Robusto**: Gestisce formati diversi e qualità di immagine variabile

## 🔑 Come Ottenere la Chiave API

### Passo 1: Crea un Account Anthropic

1. Vai su [https://console.anthropic.com](https://console.anthropic.com)
2. Clicca su **"Sign Up"** (Registrati)
3. Inserisci la tua email e segui la procedura di registrazione
4. Verifica la tua email

### Passo 2: Ottieni i Crediti Gratuiti

Anthropic offre **crediti gratuiti iniziali** per provare l'API:
- 💰 **$5 di crediti gratuiti** al momento della registrazione
- 📊 Sufficienti per analizzare **centinaia di screenshot**
- ⏱️ Validi per 3 mesi

### Passo 3: Crea una Chiave API

1. Una volta loggato, vai su [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Clicca su **"Create Key"** (Crea Chiave)
3. Dai un nome alla chiave (es. "Gestione Studenti")
4. Clicca **"Create"**
5. **COPIA LA CHIAVE** (inizia con `sk-ant-api03-...`)

   ⚠️ **IMPORTANTE**: La chiave verrà mostrata **solo una volta**! Salvala in un posto sicuro.

### Passo 4: Usa la Chiave nell'Applicazione

Hai **due opzioni**:

#### Opzione A: Inserisci la chiave nell'interfaccia (Più Facile)

1. Apri l'applicazione su `http://localhost:5001`
2. Vai su **Studenti** → **Import da Screenshot**
3. Nella sezione "Chiave API Anthropic", incolla la tua chiave
4. Carica l'immagine e clicca **"Estrai Dati"**

#### Opzione B: Configura come Variabile d'Ambiente (Più Comodo)

**Mac/Linux:**
```bash
# Aggiungi al file ~/.zshrc o ~/.bashrc
export ANTHROPIC_API_KEY="sk-ant-api03-tua-chiave-qui"

# Ricarica il terminale
source ~/.zshrc
```

**Windows (CMD):**
```cmd
setx ANTHROPIC_API_KEY "sk-ant-api03-tua-chiave-qui"
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-tua-chiave-qui"
```

Poi riavvia l'applicazione:
```bash
python3 run.py
```

Con la variabile d'ambiente configurata, **non dovrai inserire la chiave ogni volta**!

## 💡 Come Usare la Funzionalità

### 1. Prepara uno Screenshot

Fai uno screenshot o una foto che contenga:
- Nomi e cognomi degli studenti
- Date di nascita (formato DD/MM/YYYY)
- (Opzionale) Email
- (Opzionale) Numeri di telefono

**Esempio di formato riconosciuto:**
```
Rossi Mario - 15/03/2007 - mario.rossi@example.com
Bianchi Laura | 22/05/2007 | laura.bianchi@example.com | 3331234567
Verdi Giuseppe (08/01/2007)
```

Claude AI è intelligente e riconosce molti formati diversi!

### 2. Carica l'Immagine

1. Vai su **Studenti** → **Import da Screenshot**
2. Tab **"📷 Upload Screenshot"**
3. Inserisci la tua **Chiave API** (se non configurata come variabile d'ambiente)
4. Clicca nell'area upload o trascina l'immagine
5. Clicca **"Estrai Dati"**

### 3. Verifica e Importa

1. Claude AI analizzerà l'immagine (richiede alcuni secondi)
2. Vedrai una tabella con i dati estratti
3. **Verifica e modifica** eventuali errori direttamente nella tabella
4. Seleziona gli studenti da importare
5. Clicca **"Importa Studenti Selezionati"**

## 💰 Costi e Utilizzo

### Quanto Costa?

Claude AI Vision usa il modello **Claude 3.5 Sonnet** con prezzi:
- 📥 **Input**: $3 per milione di token (~1000 immagini)
- 📤 **Output**: $15 per milione di token

### Costo Reale per Screenshot

Per un tipico screenshot con 10-20 studenti:
- **Costo medio**: $0.02-0.05 per analisi
- Con **$5 di crediti gratuiti** puoi analizzare circa **100-250 screenshot**!

### Monitoraggio Utilizzo

Puoi vedere l'utilizzo su:
[https://console.anthropic.com/settings/usage](https://console.anthropic.com/settings/usage)

## 🔒 Sicurezza della Chiave API

### Buone Pratiche

✅ **FAI:**
- Usa variabili d'ambiente per l'API key
- Mantieni la chiave privata
- Rigenerala se compromessa

❌ **NON FARE:**
- Non condividere la chiave pubblicamente
- Non committarla su Git
- Non inviarla via email/chat

### Se la Chiave Viene Compromessa

1. Vai su [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Elimina la chiave compromessa
3. Crea una nuova chiave
4. Aggiorna la configurazione

## 🆘 Risoluzione Problemi

### "API key di Anthropic non fornita"

**Soluzione**: Inserisci la chiave nell'interfaccia o configurala come variabile d'ambiente.

### "Error: Invalid API key"

**Possibili cause:**
- Chiave copiata male (controlla spazi extra)
- Chiave scaduta o eliminata
- Account sospeso

**Soluzione**: Genera una nuova chiave API.

### "Error: Insufficient credits"

**Causa**: Hai finito i crediti gratuiti.

**Soluzione**:
- Aggiungi un metodo di pagamento su [console.anthropic.com](https://console.anthropic.com)
- Oppure usa la modalità **"Incolla Testo"** che è gratuita

### L'immagine non viene analizzata correttamente

**Suggerimenti:**
- Assicurati che l'immagine sia chiara e leggibile
- Evita immagini troppo piccole o sfocate
- Prova con un formato diverso (PNG, JPG)
- Usa la modalità **"Incolla Testo"** come alternativa

## 🎯 Alternative Gratuite

Se non vuoi usare l'API (o hai finito i crediti), puoi sempre usare:

### Modalità "Incolla Testo"

1. Vai su **Studenti** → **Import da Screenshot**
2. Tab **"📝 Incolla Testo"**
3. Incolla i dati nel formato:
   ```
   Cognome Nome, DD/MM/YYYY, email, telefono
   ```
4. Clicca **"Estrai Dati"**

Questa modalità è:
- ✅ **Completamente gratuita**
- ✅ **Nessuna API key necessaria**
- ✅ **Veloce e affidabile**

## 📚 Link Utili

- **Console Anthropic**: [https://console.anthropic.com](https://console.anthropic.com)
- **Chiavi API**: [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
- **Utilizzo e Crediti**: [https://console.anthropic.com/settings/usage](https://console.anthropic.com/settings/usage)
- **Documentazione API**: [https://docs.anthropic.com](https://docs.anthropic.com)
- **Prezzi**: [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing)

## 🎉 Pronto!

Ora hai tutto quello che serve per usare Claude AI Vision e importare studenti da screenshot in modo intelligente e veloce!

**Domande?** Consulta la documentazione o prova la modalità "Incolla Testo" come alternativa gratuita.
