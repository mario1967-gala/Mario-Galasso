// Gestione voti

let voti = [];
let studenti = [];
let classi = [];
let materie = [];

// Carica tutti i voti
async function loadVoti() {
    try {
        const filterStudente = document.getElementById('filterStudente').value;
        const filterMateria = document.getElementById('filterMateria').value;

        let url = '/api/voti';
        if (filterStudente) {
            url = `/api/voti/studente/${filterStudente}`;
        } else if (filterMateria) {
            url = `/api/voti/materia/${filterMateria}`;
        }

        const response = await fetch(url);
        voti = await response.json();
        renderVoti();
        updateVotiCount();
    } catch (error) {
        handleApiError(error);
    }
}

// Carica studenti, classi e materie per i filtri e il form
async function loadStudentiMaterie() {
    try {
        const [studentiRes, classiRes, materieRes] = await Promise.all([
            fetch('/api/studenti'),
            fetch('/api/classi'),
            fetch('/api/materie')
        ]);

        studenti = await studentiRes.json();
        classi = await classiRes.json();
        materie = await materieRes.json();

        // Popola il filtro classi
        const filterClasse = document.getElementById('filterClasse');
        filterClasse.innerHTML = '<option value="">Tutte le classi</option>' +
            classi.map(c => `<option value="${c.id}">${c.nome} (${c.num_studenti} studenti)</option>`).join('');

        // Popola gli altri filtri
        updateStudenteFilter();

        const filterMateria = document.getElementById('filterMateria');
        filterMateria.innerHTML = '<option value="">Tutte le materie</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');

        // Popola i select del form
        populateFormSelects();
    } catch (error) {
        handleApiError(error);
    }
}

// Aggiorna il filtro studenti in base alla classe selezionata
function updateStudenteFilter() {
    const filterClasse = document.getElementById('filterClasse').value;
    const filterStudente = document.getElementById('filterStudente');

    let studentiFiltrati = studenti;
    if (filterClasse) {
        studentiFiltrati = studenti.filter(s => s.classe_id == filterClasse);
    }

    filterStudente.innerHTML = '<option value="">Tutti gli studenti</option>' +
        studentiFiltrati.map(s => `<option value="${s.id}">${s.cognome} ${s.nome}</option>`).join('');

    // Ricarica i voti con il nuovo filtro
    loadVoti();
}

// Aggiorna il contatore dei voti
function updateVotiCount() {
    const countDiv = document.getElementById('voti-count');
    if (!countDiv) return;

    const filterClasse = document.getElementById('filterClasse').value;
    const filterStudente = document.getElementById('filterStudente').value;
    const filterMateria = document.getElementById('filterMateria').value;

    let messaggio = `<strong>${voti.length}</strong> voti`;

    if (filterClasse) {
        const classe = classi.find(c => c.id == filterClasse);
        if (classe) {
            messaggio += ` - Classe <strong>${classe.nome}</strong>`;
        }
    }

    if (filterStudente) {
        const studente = studenti.find(s => s.id == filterStudente);
        if (studente) {
            messaggio += ` - Studente: <strong>${studente.cognome} ${studente.nome}</strong>`;
        }
    }

    if (filterMateria) {
        const materia = materie.find(m => m.id == filterMateria);
        if (materia) {
            messaggio += ` - Materia: <strong>${materia.nome}</strong>`;
        }
    }

    countDiv.innerHTML = messaggio;
}

// Popola i select del form
function populateFormSelects() {
    // Popola studenti considerando il filtro classe
    populateFormStudentiSelect();

    const materiaSelect = document.getElementById('materia_id');
    materiaSelect.innerHTML = '<option value="">Seleziona materia</option>' +
        materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
}

// Popola il select studenti del form filtrando per classe se necessario
function populateFormStudentiSelect() {
    const filterClasse = document.getElementById('filterClasse').value;
    const studenteSelect = document.getElementById('studente_id');

    // Filtra studenti in base alla classe selezionata nei filtri
    let studentiFiltrati = studenti;
    if (filterClasse) {
        studentiFiltrati = studenti.filter(s => s.classe_id == filterClasse);
    }

    studenteSelect.innerHTML = '<option value="">Seleziona studente</option>' +
        studentiFiltrati.map(s => `<option value="${s.id}">${s.cognome} ${s.nome}</option>`).join('');
}

// Renderizza la tabella dei voti
function renderVoti() {
    const tbody = document.getElementById('voti-tbody');

    if (voti.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nessun voto trovato</td></tr>';
        return;
    }

    tbody.innerHTML = voti.map(voto => `
        <tr>
            <td>${formatDate(voto.data)}</td>
            <td>${voto.studente_nome}</td>
            <td>${voto.materia_nome}</td>
            <td><strong>${voto.voto}</strong></td>
            <td>${voto.tipo || '-'}</td>
            <td>${voto.note || '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editVoto(${voto.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deleteVoto(${voto.id})">Elimina</button>
            </td>
        </tr>
    `).join('');
}

// Mostra modal per aggiungere voto
function showAddVotoModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Voto';
    document.getElementById('votoForm').reset();
    document.getElementById('votoId').value = '';
    document.getElementById('data').valueAsDate = new Date();

    // Ripopola il select studenti con il filtro classe corrente
    populateFormStudentiSelect();

    document.getElementById('votoModal').classList.add('show');
}

// Modifica voto
async function editVoto(id) {
    const voto = voti.find(v => v.id === id);
    if (!voto) return;

    document.getElementById('modalTitle').textContent = 'Modifica Voto';
    document.getElementById('votoId').value = voto.id;
    document.getElementById('studente_id').value = voto.studente_id;
    document.getElementById('materia_id').value = voto.materia_id;
    document.getElementById('voto').value = voto.voto;
    document.getElementById('tipo').value = voto.tipo || '';
    document.getElementById('data').value = voto.data;
    document.getElementById('note').value = voto.note || '';
    document.getElementById('votoModal').classList.add('show');
}

// Salva voto
async function saveVoto(event) {
    event.preventDefault();

    const id = document.getElementById('votoId').value;
    const data = {
        studente_id: parseInt(document.getElementById('studente_id').value),
        materia_id: parseInt(document.getElementById('materia_id').value),
        voto: parseFloat(document.getElementById('voto').value),
        tipo: document.getElementById('tipo').value,
        data: document.getElementById('data').value,
        note: document.getElementById('note').value
    };

    try {
        const url = id ? `/api/voti/${id}` : '/api/voti';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Voto aggiornato con successo' : 'Voto aggiunto con successo');
            closeModal();
            loadVoti();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina voto
async function deleteVoto(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questo voto?')) {
        return;
    }

    try {
        const response = await fetch(`/api/voti/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Voto eliminato con successo');
            loadVoti();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('votoModal').classList.remove('show');
}

// Carica dati all'avvio
loadStudentiMaterie().then(() => loadVoti());
