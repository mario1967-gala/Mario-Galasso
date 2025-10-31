// Gestione presenze

let presenze = [];
let studenti = [];
let classi = [];

// Carica tutte le presenze
async function loadPresenze() {
    try {
        const filterStudente = document.getElementById('filterStudente').value;

        let url = '/api/presenze';
        if (filterStudente) {
            url = `/api/presenze/studente/${filterStudente}`;
        }

        const response = await fetch(url);
        presenze = await response.json();
        renderPresenze();
        updatePresenzeCount();
    } catch (error) {
        handleApiError(error);
    }
}

// Carica studenti e classi per i filtri
async function loadStudenti() {
    try {
        const [studentiRes, classiRes] = await Promise.all([
            fetch('/api/studenti'),
            fetch('/api/classi')
        ]);

        studenti = await studentiRes.json();
        classi = await classiRes.json();

        // Popola il filtro classi
        const filterClasse = document.getElementById('filterClasse');
        filterClasse.innerHTML = '<option value="">Tutte le classi</option>' +
            classi.map(c => `<option value="${c.id}">${c.nome} (${c.num_studenti} studenti)</option>`).join('');

        // Popola gli altri filtri
        updateStudenteFilter();

        // Popola il select del form
        const studenteSelect = document.getElementById('studente_id');
        studenteSelect.innerHTML = '<option value="">Seleziona studente</option>' +
            studenti.map(s => `<option value="${s.id}">${s.cognome} ${s.nome}</option>`).join('');
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

    // Ricarica le presenze con il nuovo filtro
    loadPresenze();
}

// Aggiorna il contatore delle presenze
function updatePresenzeCount() {
    const countDiv = document.getElementById('presenze-count');
    if (!countDiv) return;

    const filterClasse = document.getElementById('filterClasse').value;
    const filterStudente = document.getElementById('filterStudente').value;

    let messaggio = `<strong>${presenze.length}</strong> presenze`;

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

    countDiv.innerHTML = messaggio;
}

// Renderizza la tabella delle presenze
function renderPresenze() {
    const tbody = document.getElementById('presenze-tbody');

    if (presenze.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center">Nessuna presenza trovata</td></tr>';
        return;
    }

    tbody.innerHTML = presenze.map(presenza => `
        <tr>
            <td>${formatDate(presenza.data)}</td>
            <td>${presenza.studente_nome}</td>
            <td><span class="badge badge-${presenza.tipo}">${presenza.tipo.replace('_', ' ')}</span></td>
            <td>${presenza.ora_ingresso || '-'}</td>
            <td>${presenza.ora_uscita || '-'}</td>
            <td>${presenza.giustificata ? 'Sì' : 'No'}</td>
            <td>${presenza.note || '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editPresenza(${presenza.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deletePresenza(${presenza.id})">Elimina</button>
            </td>
        </tr>
    `).join('');
}

// Mostra/nascondi campi ora in base al tipo
function toggleTimeFields() {
    const tipo = document.getElementById('tipo').value;
    const oraIngressoGroup = document.getElementById('ora_ingresso_group');
    const oraUscitaGroup = document.getElementById('ora_uscita_group');

    oraIngressoGroup.style.display = tipo === 'ritardo' ? 'block' : 'none';
    oraUscitaGroup.style.display = tipo === 'uscita_anticipata' ? 'block' : 'none';
}

// Mostra modal per aggiungere presenza
function showAddPresenzaModal() {
    document.getElementById('modalTitle').textContent = 'Registra Presenza';
    document.getElementById('presenzaForm').reset();
    document.getElementById('presenzaId').value = '';
    document.getElementById('data').valueAsDate = new Date();
    toggleTimeFields();
    document.getElementById('presenzaModal').classList.add('show');
}

// Modifica presenza
function editPresenza(id) {
    const presenza = presenze.find(p => p.id === id);
    if (!presenza) return;

    document.getElementById('modalTitle').textContent = 'Modifica Presenza';
    document.getElementById('presenzaId').value = presenza.id;
    document.getElementById('studente_id').value = presenza.studente_id;
    document.getElementById('data').value = presenza.data;
    document.getElementById('tipo').value = presenza.tipo;
    document.getElementById('ora_ingresso').value = presenza.ora_ingresso || '';
    document.getElementById('ora_uscita').value = presenza.ora_uscita || '';
    document.getElementById('giustificata').checked = presenza.giustificata;
    document.getElementById('note').value = presenza.note || '';
    toggleTimeFields();
    document.getElementById('presenzaModal').classList.add('show');
}

// Salva presenza
async function savePresenza(event) {
    event.preventDefault();

    const id = document.getElementById('presenzaId').value;
    const data = {
        studente_id: parseInt(document.getElementById('studente_id').value),
        data: document.getElementById('data').value,
        tipo: document.getElementById('tipo').value,
        giustificata: document.getElementById('giustificata').checked,
        note: document.getElementById('note').value
    };

    // Aggiungi ore se presenti
    const oraIngresso = document.getElementById('ora_ingresso').value;
    const oraUscita = document.getElementById('ora_uscita').value;

    if (oraIngresso) data.ora_ingresso = oraIngresso;
    if (oraUscita) data.ora_uscita = oraUscita;

    try {
        const url = id ? `/api/presenze/${id}` : '/api/presenze';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Presenza aggiornata con successo' : 'Presenza registrata con successo');
            closeModal();
            loadPresenze();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina presenza
async function deletePresenza(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questa presenza?')) {
        return;
    }

    try {
        const response = await fetch(`/api/presenze/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Presenza eliminata con successo');
            loadPresenze();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('presenzaModal').classList.remove('show');
}

// Carica dati all'avvio
loadStudenti().then(() => loadPresenze());
