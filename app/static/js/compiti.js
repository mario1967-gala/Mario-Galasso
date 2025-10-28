// Gestione compiti

let compiti = [];
let materie = [];

// Carica tutti i compiti
async function loadCompiti() {
    try {
        const filterMateria = document.getElementById('filterMateria').value;
        const showCompletati = document.getElementById('filterCompletati').checked;

        let url = '/api/compiti';
        if (filterMateria) {
            url = `/api/compiti/materia/${filterMateria}`;
        }

        const response = await fetch(url);
        let allCompiti = await response.json();

        // Filtra compiti completati se necessario
        if (!showCompletati) {
            compiti = allCompiti.filter(c => !c.completato);
        } else {
            compiti = allCompiti;
        }

        renderCompiti();
    } catch (error) {
        handleApiError(error);
    }
}

// Carica materie
async function loadMaterie() {
    try {
        const response = await fetch('/api/materie');
        materie = await response.json();

        // Popola i filtri
        const filterMateria = document.getElementById('filterMateria');
        filterMateria.innerHTML = '<option value="">Tutte le materie</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');

        // Popola il select del form
        const materiaSelect = document.getElementById('materia_id');
        materiaSelect.innerHTML = '<option value="">Seleziona materia</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
    } catch (error) {
        handleApiError(error);
    }
}

// Renderizza i compiti
function renderCompiti() {
    const grid = document.getElementById('compiti-grid');

    if (compiti.length === 0) {
        grid.innerHTML = '<div class="loading">Nessun compito trovato</div>';
        return;
    }

    grid.innerHTML = compiti.map(compito => {
        const dataScadenza = new Date(compito.data_scadenza);
        const oggi = new Date();
        const giorni = Math.ceil((dataScadenza - oggi) / (1000 * 60 * 60 * 24));

        let urgenzaClass = '';
        if (giorni < 0) urgenzaClass = 'scaduto';
        else if (giorni <= 2) urgenzaClass = 'urgente';

        return `
            <div class="compito-card ${compito.completato ? 'completato' : ''} ${urgenzaClass}">
                <h3>${compito.titolo}</h3>
                <p><strong>Materia:</strong> ${compito.materia_nome}</p>
                <p>${compito.descrizione || ''}</p>
                <p><strong>Scadenza:</strong> ${formatDate(compito.data_scadenza)}</p>
                ${giorni >= 0 && !compito.completato ? `<p><em>${giorni === 0 ? 'Scade oggi!' : giorni === 1 ? 'Scade domani' : `Mancano ${giorni} giorni`}</em></p>` : ''}
                ${compito.completato ? '<p><strong>✓ Completato</strong></p>' : ''}
                <span class="compito-badge badge-${compito.tipo}">${compito.tipo.replace('_', ' ')}</span>
                <div class="card-actions">
                    ${!compito.completato ? `<button class="btn btn-sm btn-success" onclick="toggleCompletato(${compito.id}, true)">Completa</button>` : `<button class="btn btn-sm btn-secondary" onclick="toggleCompletato(${compito.id}, false)">Riapri</button>`}
                    <button class="btn btn-sm btn-primary" onclick="editCompito(${compito.id})">Modifica</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCompito(${compito.id})">Elimina</button>
                </div>
            </div>
        `;
    }).join('');
}

// Toggle stato completato
async function toggleCompletato(id, completato) {
    try {
        const response = await fetch(`/api/compiti/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ completato: completato })
        });

        const result = await response.json();

        if (result.success) {
            showNotification(completato ? 'Compito completato!' : 'Compito riaperto');
            loadCompiti();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Mostra modal per aggiungere compito
function showAddCompitoModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Compito';
    document.getElementById('compitoForm').reset();
    document.getElementById('compitoId').value = '';
    document.getElementById('compitoModal').classList.add('show');
}

// Modifica compito
function editCompito(id) {
    const compito = compiti.find(c => c.id === id);
    if (!compito) return;

    document.getElementById('modalTitle').textContent = 'Modifica Compito';
    document.getElementById('compitoId').value = compito.id;
    document.getElementById('materia_id').value = compito.materia_id;
    document.getElementById('titolo').value = compito.titolo;
    document.getElementById('descrizione').value = compito.descrizione || '';
    document.getElementById('tipo').value = compito.tipo;
    document.getElementById('data_scadenza').value = compito.data_scadenza;
    document.getElementById('completato').checked = compito.completato;
    document.getElementById('compitoModal').classList.add('show');
}

// Salva compito
async function saveCompito(event) {
    event.preventDefault();

    const id = document.getElementById('compitoId').value;
    const data = {
        materia_id: parseInt(document.getElementById('materia_id').value),
        titolo: document.getElementById('titolo').value,
        descrizione: document.getElementById('descrizione').value,
        tipo: document.getElementById('tipo').value,
        data_scadenza: document.getElementById('data_scadenza').value,
        completato: document.getElementById('completato').checked
    };

    try {
        const url = id ? `/api/compiti/${id}` : '/api/compiti';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Compito aggiornato con successo' : 'Compito creato con successo');
            closeModal();
            loadCompiti();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina compito
async function deleteCompito(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questo compito?')) {
        return;
    }

    try {
        const response = await fetch(`/api/compiti/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Compito eliminato con successo');
            loadCompiti();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('compitoModal').classList.remove('show');
}

// CSS aggiuntivo per urgenze
const style = document.createElement('style');
style.textContent = `
    .compito-card.urgente {
        border-left-color: var(--warning-color) !important;
    }
    .compito-card.scaduto {
        border-left-color: var(--danger-color) !important;
    }
`;
document.head.appendChild(style);

// Carica dati all'avvio
loadMaterie().then(() => loadCompiti());
