// Gestione studenti

let studenti = [];
let classi = [];
let currentFilter = ''; // Filtro corrente per classe

// Carica tutti gli studenti
async function loadStudenti() {
    try {
        const response = await fetch('/api/studenti');
        studenti = await response.json();
        renderStudenti();
    } catch (error) {
        handleApiError(error);
    }
}

// Carica tutte le classi
async function loadClassi() {
    try {
        const response = await fetch('/api/classi');
        classi = await response.json();
        populateFiltroClassi();
    } catch (error) {
        console.error('Errore nel caricamento delle classi:', error);
    }
}

// Popola il dropdown del filtro classi
function populateFiltroClassi() {
    const select = document.getElementById('filtro-classe');
    if (!select) return;

    // Mantieni l'opzione "Tutte le classi"
    select.innerHTML = '<option value="">Tutte le classi</option>';

    classi.forEach(classe => {
        const option = document.createElement('option');
        option.value = classe.id;
        option.textContent = `${classe.nome} (${classe.num_studenti} studenti)`;
        select.appendChild(option);
    });

    // Ripristina il filtro corrente se presente
    if (currentFilter) {
        select.value = currentFilter;
    }
}

// Filtra studenti per classe
function filterByClasse() {
    const select = document.getElementById('filtro-classe');
    currentFilter = select.value;
    renderStudenti();
}

// Renderizza la tabella degli studenti
function renderStudenti() {
    const tbody = document.getElementById('studenti-tbody');

    // Filtra studenti in base alla classe selezionata
    let studentiFiltrati = studenti;
    if (currentFilter) {
        studentiFiltrati = studenti.filter(s => s.classe_id == currentFilter);
    }

    // Aggiorna il contatore
    updateStudentiCount(studentiFiltrati.length, studenti.length);

    if (studentiFiltrati.length === 0) {
        const messaggio = currentFilter
            ? 'Nessuno studente trovato in questa classe'
            : 'Nessuno studente trovato';
        tbody.innerHTML = `<tr><td colspan="8" class="text-center">${messaggio}</td></tr>`;
        return;
    }

    tbody.innerHTML = studentiFiltrati.map(studente => `
        <tr>
            <td>${studente.classe_nome || '-'}</td>
            <td>${studente.cognome}</td>
            <td>${studente.nome}</td>
            <td>${formatDate(studente.data_nascita)}</td>
            <td>${studente.codice_fiscale || '-'}</td>
            <td>${studente.email || '-'}</td>
            <td>${studente.telefono || '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editStudente(${studente.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deleteStudente(${studente.id})">Elimina</button>
            </td>
        </tr>
    `).join('');
}

// Aggiorna il contatore degli studenti visualizzati
function updateStudentiCount(filtered, total) {
    const countDiv = document.getElementById('studenti-count');
    if (!countDiv) return;

    if (currentFilter) {
        const classeSelezionata = classi.find(c => c.id == currentFilter);
        const nomeClasse = classeSelezionata ? classeSelezionata.nome : 'classe selezionata';
        countDiv.innerHTML = `<strong>${filtered}</strong> studenti in <strong>${nomeClasse}</strong> (${total} totali)`;
    } else {
        countDiv.innerHTML = `<strong>${total}</strong> studenti totali`;
    }
}

// Mostra modal per aggiungere studente
function showAddStudentModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Studente';
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    populateClassiSelect();
    document.getElementById('studentModal').classList.add('show');
}

// Popola il select delle classi
function populateClassiSelect() {
    const select = document.getElementById('classe_id');
    select.innerHTML = '<option value="">Seleziona classe...</option>';

    classi.forEach(classe => {
        const option = document.createElement('option');
        option.value = classe.id;
        option.textContent = classe.nome;
        select.appendChild(option);
    });
}

// Modifica studente
function editStudente(id) {
    const studente = studenti.find(s => s.id === id);
    if (!studente) return;

    document.getElementById('modalTitle').textContent = 'Modifica Studente';
    document.getElementById('studentId').value = studente.id;
    populateClassiSelect();
    document.getElementById('classe_id').value = studente.classe_id || '';
    document.getElementById('nome').value = studente.nome;
    document.getElementById('cognome').value = studente.cognome;
    document.getElementById('data_nascita').value = studente.data_nascita;
    document.getElementById('codice_fiscale').value = studente.codice_fiscale || '';
    document.getElementById('email').value = studente.email || '';
    document.getElementById('telefono').value = studente.telefono || '';
    document.getElementById('indirizzo').value = studente.indirizzo || '';
    document.getElementById('studentModal').classList.add('show');
}

// Salva studente (crea o aggiorna)
async function saveStudent(event) {
    event.preventDefault();

    const id = document.getElementById('studentId').value;
    const classeId = document.getElementById('classe_id').value;

    const data = {
        classe_id: classeId || null,
        nome: document.getElementById('nome').value,
        cognome: document.getElementById('cognome').value,
        data_nascita: document.getElementById('data_nascita').value,
        codice_fiscale: document.getElementById('codice_fiscale').value,
        email: document.getElementById('email').value,
        telefono: document.getElementById('telefono').value,
        indirizzo: document.getElementById('indirizzo').value
    };

    try {
        const url = id ? `/api/studenti/${id}` : '/api/studenti';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Studente aggiornato con successo' : 'Studente creato con successo');
            closeModal();
            // Ricarica sia studenti che classi per aggiornare i contatori
            Promise.all([loadClassi(), loadStudenti()]);
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina studente
async function deleteStudente(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questo studente? Tutti i dati associati verranno eliminati.')) {
        return;
    }

    try {
        const response = await fetch(`/api/studenti/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Studente eliminato con successo');
            // Ricarica sia studenti che classi per aggiornare i contatori
            Promise.all([loadClassi(), loadStudenti()]);
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('studentModal').classList.remove('show');
}

// Carica studenti e classi all'avvio
Promise.all([loadClassi(), loadStudenti()]);
