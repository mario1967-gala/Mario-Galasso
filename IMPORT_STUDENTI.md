# Guida: Import Studenti da Screenshot

## Panoramica

La nuova funzionalità permette di importare rapidamente multipli studenti in due modalità:
1. **Upload Screenshot** - Carica un'immagine e il sistema estrae i dati con OCR
2. **Incolla Testo** - Incolla una lista di studenti in formato testuale

## Come Accedere

1. Vai alla pagina **Studenti** (`/studenti`)
2. Clicca sul pulsante **"📷 Import da Screenshot"**
3. Verrai reindirizzato alla pagina di import (`/studenti/import`)

## Modalità 1: Upload Screenshot

### Requisiti
- Tesseract OCR deve essere installato sul sistema
- Su Ubuntu/Debian: `sudo apt-get install tesseract-ocr tesseract-ocr-ita`
- Su macOS: `brew install tesseract tesseract-lang`
- Su Windows: Scarica da [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

### Come Usare
1. Clicca sulla tab **"📷 Upload Screenshot"**
2. Clicca nell'area upload o trascina un'immagine
3. Formati supportati: PNG, JPG, JPEG, GIF, BMP
4. Clicca **"Estrai Dati"**
5. Il sistema analizzerà l'immagine e estrarrà i dati degli studenti
6. Verifica e modifica i dati se necessario
7. Seleziona gli studenti da importare
8. Clicca **"Importa Studenti Selezionati"**

### Formato Screenshot Consigliato

L'immagine dovrebbe contenere una lista chiara con:
- Nome e cognome dello studente
- Data di nascita (formato DD/MM/YYYY)

Esempi di formati riconosciuti:
```
Rossi Mario - 15/03/2007
Bianchi Laura, 22/05/2007
Verdi Giuseppe (08/01/2007)
```

## Modalità 2: Incolla Testo

### Formato Testo

Il formato più semplice e affidabile è:
```
Cognome Nome, DD/MM/YYYY
```

Puoi anche includere email e telefono:
```
Cognome Nome, DD/MM/YYYY, email@example.com
Cognome Nome, DD/MM/YYYY, email@example.com, 3331234567
```

### Come Usare
1. Clicca sulla tab **"📝 Incolla Testo"**
2. Incolla i dati degli studenti nel formato indicato
3. Un studente per riga
4. Clicca **"Estrai Dati"**
5. Verifica i dati estratti nella tabella
6. Modifica se necessario
7. Seleziona gli studenti da importare
8. Clicca **"Importa Studenti Selezionati"**

### Esempio Completo

```
Rossi Mario, 15/03/2007, mario.rossi@example.com
Bianchi Laura, 22/05/2007, laura.bianchi@example.com, 3331234567
Verdi Giuseppe, 08/01/2007
Neri Anna, 30/09/2007, anna.neri@example.com
Ferrari Luca, 12/06/2007, luca.ferrari@example.com, 3339876543
```

## Funzionalità della Tabella di Anteprima

Dopo l'estrazione, vedrai una tabella con tutti gli studenti trovati:

### Modifica Dati
- Ogni campo è modificabile direttamente nella tabella
- Clicca nel campo e modifica il valore
- I cambiamenti sono salvati automaticamente

### Selezione Studenti
- Usa la checkbox per selezionare/deselezionare studenti
- La checkbox nell'header seleziona/deseleziona tutti
- Vengono importati solo gli studenti selezionati

### Rimuovi Studente
- Clicca il pulsante **"Rimuovi"** per eliminare uno studente dalla lista
- Questo non influisce sul database, rimuove solo dalla lista di import

## Validazione

### Campi Obbligatori
- **Nome** - obbligatorio
- **Cognome** - obbligatorio
- **Data di nascita** - opzionale ma consigliato

### Campi Opzionali
- Email
- Telefono
- Codice Fiscale
- Indirizzo

## Gestione Errori

### Se OCR non è disponibile
Se vedi un errore tipo "tesseract not found" o "OCR non disponibile":
1. Usa la modalità **"Incolla Testo"** invece dello screenshot
2. Oppure installa Tesseract OCR sul sistema

### Se i dati non vengono estratti correttamente
1. Verifica che l'immagine sia chiara e leggibile
2. Prova a migliorare il contrasto dell'immagine
3. Assicurati che il testo non sia troppo piccolo
4. Come alternativa, usa la modalità "Incolla Testo"

### Se alcuni studenti non vengono importati
- Controlla i messaggi di errore nella console del browser (F12)
- Verifica che nome e cognome siano presenti
- Controlla il formato della data (deve essere YYYY-MM-DD nella tabella)

## Vantaggi

✅ **Veloce**: Importa decine di studenti in pochi secondi
✅ **Flessibile**: Supporta diversi formati di input
✅ **Verificabile**: Controlla e modifica i dati prima dell'import
✅ **Sicuro**: Puoi selezionare solo gli studenti corretti

## Esempi Pratici

### Scenario 1: Lista da Registro Cartaceo

Hai una lista cartacea di studenti?
1. Fotografa la lista con il telefono
2. Carica la foto nell'applicazione
3. Verifica i dati estratti
4. Importa!

### Scenario 2: Lista da Email o Documento

Ricevuta una lista via email?
1. Copia il testo
2. Vai alla tab "Incolla Testo"
3. Incolla i dati
4. Importa!

### Scenario 3: Lista da Excel/CSV

Hai i dati in Excel?
1. Formatta le celle come: `Cognome Nome, Data, Email, Telefono`
2. Copia le righe
3. Incolla nella modalità testo
4. Importa!

## Note Importanti

- ⚠️ L'import crea NUOVI studenti, non aggiorna quelli esistenti
- ⚠️ Se uno studente con lo stesso email esiste già, l'import potrebbe fallire
- 💡 Puoi modificare i dati anche dopo l'import dalla pagina Studenti
- 💡 Non è necessario importare tutti gli studenti in una volta

## Supporto

Se hai problemi con l'import:
1. Verifica il formato dei dati
2. Controlla la console del browser per errori
3. Prova la modalità alternativa (screenshot ↔ testo)
4. Contatta il supporto tecnico

## Prossimi Passi

Dopo aver importato gli studenti:
1. Verifica i dati nella pagina **Studenti**
2. Completa eventuali informazioni mancanti
3. Inizia a registrare voti e presenze!
