// Gestione studenti

let studenti = [];

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

// Renderizza la tabella degli studenti
function renderStudenti() {
    const tbody = document.getElementById('studenti-tbody');

    if (studenti.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nessuno studente trovato</td></tr>';
        return;
    }

    tbody.innerHTML = studenti.map(studente => `
        <tr>
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

// Mostra modal per aggiungere studente
function showAddStudentModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Studente';
    document.getElementById('studentForm').reset();
    document.getElementById('studentId').value = '';
    document.getElementById('studentModal').classList.add('show');
}

// Modifica studente
function editStudente(id) {
    const studente = studenti.find(s => s.id === id);
    if (!studente) return;

    document.getElementById('modalTitle').textContent = 'Modifica Studente';
    document.getElementById('studentId').value = studente.id;
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
    const data = {
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
            loadStudenti();
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
            loadStudenti();
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

// Carica studenti all'avvio
loadStudenti();
