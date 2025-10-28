// Gestione materiali

let materiali = [];
let materie = [];

// Carica tutti i materiali
async function loadMateriali() {
    try {
        const filterMateria = document.getElementById('filterMateria').value;
        const filterTipo = document.getElementById('filterTipo').value;

        let url = '/api/materiali';
        if (filterMateria) {
            url = `/api/materiali/materia/${filterMateria}`;
        }

        const response = await fetch(url);
        let allMateriali = await response.json();

        // Filtra per tipo se necessario
        if (filterTipo) {
            materiali = allMateriali.filter(m => m.tipo === filterTipo);
        } else {
            materiali = allMateriali;
        }

        renderMateriali();
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

// Ottieni icona per tipo materiale
function getIconForTipo(tipo) {
    const icons = {
        'dispensa': '📄',
        'slide': '📊',
        'esercizi': '✏️',
        'link': '🔗',
        'video': '🎥'
    };
    return icons[tipo] || '📁';
}

// Renderizza i materiali
function renderMateriali() {
    const grid = document.getElementById('materiali-grid');

    if (materiali.length === 0) {
        grid.innerHTML = '<div class="loading">Nessun materiale trovato</div>';
        return;
    }

    grid.innerHTML = materiali.map(materiale => `
        <div class="materiale-card">
            <div class="materiale-header">
                <span class="materiale-icon">${getIconForTipo(materiale.tipo)}</span>
                <div>
                    <h3>${materiale.titolo}</h3>
                    <p style="font-size: 0.875rem; color: var(--text-light);">${materiale.materia_nome}</p>
                </div>
            </div>
            <p>${materiale.descrizione || 'Nessuna descrizione'}</p>
            ${materiale.contenuto ? `<p><strong>Contenuto:</strong> <a href="${materiale.contenuto}" target="_blank">${materiale.contenuto.substring(0, 50)}${materiale.contenuto.length > 50 ? '...' : ''}</a></p>` : ''}
            <p style="font-size: 0.75rem; color: var(--text-light); margin-top: 1rem;">Caricato il: ${materiale.data_caricamento}</p>
            <div class="card-actions">
                <button class="btn btn-sm btn-primary" onclick="editMateriale(${materiale.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deleteMateriale(${materiale.id})">Elimina</button>
            </div>
        </div>
    `).join('');
}

// Mostra modal per aggiungere materiale
function showAddMaterialeModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Materiale';
    document.getElementById('materialeForm').reset();
    document.getElementById('materialeId').value = '';
    document.getElementById('materialeModal').classList.add('show');
}

// Modifica materiale
function editMateriale(id) {
    const materiale = materiali.find(m => m.id === id);
    if (!materiale) return;

    document.getElementById('modalTitle').textContent = 'Modifica Materiale';
    document.getElementById('materialeId').value = materiale.id;
    document.getElementById('materia_id').value = materiale.materia_id;
    document.getElementById('titolo').value = materiale.titolo;
    document.getElementById('descrizione').value = materiale.descrizione || '';
    document.getElementById('tipo').value = materiale.tipo;
    document.getElementById('contenuto').value = materiale.contenuto || '';
    document.getElementById('materialeModal').classList.add('show');
}

// Salva materiale
async function saveMateriale(event) {
    event.preventDefault();

    const id = document.getElementById('materialeId').value;
    const data = {
        materia_id: parseInt(document.getElementById('materia_id').value),
        titolo: document.getElementById('titolo').value,
        descrizione: document.getElementById('descrizione').value,
        tipo: document.getElementById('tipo').value,
        contenuto: document.getElementById('contenuto').value
    };

    try {
        const url = id ? `/api/materiali/${id}` : '/api/materiali';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Materiale aggiornato con successo' : 'Materiale creato con successo');
            closeModal();
            loadMateriali();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina materiale
async function deleteMateriale(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questo materiale?')) {
        return;
    }

    try {
        const response = await fetch(`/api/materiali/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Materiale eliminato con successo');
            loadMateriali();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('materialeModal').classList.remove('show');
}

// Carica dati all'avvio
loadMaterie().then(() => loadMateriali());
