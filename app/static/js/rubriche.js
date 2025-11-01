// Gestione Rubriche di Valutazione

let rubriche = [];
let materie = [];
let currentRubrica = null;
let currentCriterio = null;

// ==================== INIT ====================

document.addEventListener('DOMContentLoaded', function() {
    loadMaterie();
    loadRubriche();
});

// ==================== CARICAMENTO DATI ====================

async function loadRubriche() {
    try {
        const filterMateria = document.getElementById('filterMateria').value;

        let url = '/api/rubriche';
        if (filterMateria) {
            url = `/api/rubriche/materia/${filterMateria}`;
        }

        const response = await fetch(url);
        rubriche = await response.json();

        renderRubriche();
    } catch (error) {
        handleApiError(error);
    }
}

async function loadMaterie() {
    try {
        const response = await fetch('/api/materie');
        materie = await response.json();

        // Popola filtro materie
        const filterMateria = document.getElementById('filterMateria');
        filterMateria.innerHTML = '<option value="">Tutte le materie</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');

        // Popola select materie nel form
        const materiaSelect = document.getElementById('materia_id');
        materiaSelect.innerHTML = '<option value="">Seleziona materia</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== RENDERING ====================

function renderRubriche() {
    const container = document.getElementById('rubriche-list');

    if (rubriche.length === 0) {
        container.innerHTML = '<div class="empty-state">Nessuna rubrica trovata. Crea la tua prima rubrica di valutazione!</div>';
        return;
    }

    container.innerHTML = rubriche.map(rubrica => `
        <div class="rubrica-card ${rubrica.attiva ? '' : 'inactive'}">
            <div class="rubrica-header">
                <div>
                    <h3>${rubrica.titolo}</h3>
                    <div class="rubrica-meta">
                        <span class="badge">${rubrica.materia_nome}</span>
                        <span class="badge">${rubrica.tipo_verifica}</span>
                        <span class="badge-info">${rubrica.num_criteri} criteri</span>
                        ${!rubrica.attiva ? '<span class="badge-warning">Non attiva</span>' : ''}
                    </div>
                </div>
                <div class="rubrica-actions">
                    <button class="btn btn-sm btn-primary" onclick="openCriteriModal(${rubrica.id})">
                        Gestisci Criteri
                    </button>
                    <button class="btn btn-sm btn-secondary" onclick="editRubrica(${rubrica.id})">
                        <i class="icon-edit"></i> Modifica
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteRubrica(${rubrica.id})">
                        <i class="icon-delete"></i> Elimina
                    </button>
                </div>
            </div>
            ${rubrica.descrizione ? `<p class="rubrica-description">${rubrica.descrizione}</p>` : ''}
        </div>
    `).join('');
}

// ==================== MODAL RUBRICA ====================

function showAddRubricaModal() {
    document.getElementById('modalTitle').textContent = 'Nuova Rubrica di Valutazione';
    document.getElementById('rubricaForm').reset();
    document.getElementById('rubricaId').value = '';
    document.getElementById('attiva').checked = true;
    document.getElementById('rubricaModal').style.display = 'block';
}

function closeRubricaModal() {
    document.getElementById('rubricaModal').style.display = 'none';
}

async function editRubrica(id) {
    try {
        const response = await fetch(`/api/rubriche/${id}`);
        const rubrica = await response.json();

        document.getElementById('modalTitle').textContent = 'Modifica Rubrica';
        document.getElementById('rubricaId').value = rubrica.id;
        document.getElementById('materia_id').value = rubrica.materia_id;
        document.getElementById('titolo').value = rubrica.titolo;
        document.getElementById('descrizione').value = rubrica.descrizione || '';
        document.getElementById('tipo_verifica').value = rubrica.tipo_verifica || 'scritta';
        document.getElementById('attiva').checked = rubrica.attiva;

        document.getElementById('rubricaModal').style.display = 'block';
    } catch (error) {
        handleApiError(error);
    }
}

async function saveRubrica(event) {
    event.preventDefault();

    const id = document.getElementById('rubricaId').value;
    const data = {
        materia_id: parseInt(document.getElementById('materia_id').value),
        titolo: document.getElementById('titolo').value,
        descrizione: document.getElementById('descrizione').value,
        tipo_verifica: document.getElementById('tipo_verifica').value,
        attiva: document.getElementById('attiva').checked
    };

    try {
        const url = id ? `/api/rubriche/${id}` : '/api/rubriche';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Rubrica aggiornata!' : 'Rubrica creata!', 'success');
            closeRubricaModal();
            loadRubriche();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

async function deleteRubrica(id) {
    if (!confirm('Sei sicuro di voler eliminare questa rubrica? Verranno eliminati anche tutti i criteri associati.')) {
        return;
    }

    try {
        const response = await fetch(`/api/rubriche/${id}`, {method: 'DELETE'});
        const result = await response.json();

        if (result.success) {
            showNotification('Rubrica eliminata!', 'success');
            loadRubriche();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== MODAL CRITERI ====================

async function openCriteriModal(rubricaId) {
    try {
        const response = await fetch(`/api/rubriche/${rubricaId}`);
        currentRubrica = await response.json();

        document.getElementById('criteriModalTitle').textContent = `Criteri - ${currentRubrica.titolo}`;
        document.getElementById('rubricaInfo').innerHTML = `
            <div class="info-box">
                <strong>Materia:</strong> ${currentRubrica.materia_nome} |
                <strong>Tipo:</strong> ${currentRubrica.tipo_verifica} |
                <strong>Criteri definiti:</strong> ${currentRubrica.num_criteri}
            </div>
        `;

        renderCriteri();
        document.getElementById('criteriModal').style.display = 'block';
    } catch (error) {
        handleApiError(error);
    }
}

function closeCriteriModal() {
    document.getElementById('criteriModal').style.display = 'none';
    currentRubrica = null;
    loadRubriche(); // Ricarica per aggiornare il conteggio criteri
}

function renderCriteri() {
    const container = document.getElementById('criteriList');

    if (!currentRubrica.criteri || currentRubrica.criteri.length === 0) {
        container.innerHTML = '<div class="empty-state">Nessun criterio definito. Aggiungi il primo criterio!</div>';
        return;
    }

    container.innerHTML = currentRubrica.criteri.map((criterio, index) => `
        <div class="criterio-card">
            <div class="criterio-header">
                <div class="criterio-info">
                    <h4>${index + 1}. ${criterio.nome}</h4>
                    ${criterio.descrizione ? `<p class="criterio-desc">${criterio.descrizione}</p>` : ''}
                    <span class="badge-info">Peso: ${criterio.peso}</span>
                    <span class="badge-info">${criterio.descrittori.length} livelli definiti</span>
                </div>
                <div class="criterio-actions">
                    <button class="btn btn-sm btn-primary" onclick="openDescrittoriModal(${criterio.id})">
                        Definisci Livelli
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteCriterio(${criterio.id})">
                        Elimina
                    </button>
                </div>
            </div>
            ${criterio.descrittori.length > 0 ? `
                <div class="descrittori-preview">
                    ${criterio.descrittori.map(d => `
                        <div class="desc-preview livello-${d.livello}">
                            <strong>${d.livello_nome}</strong> (${d.punteggio})
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

function showAddCriterioForm() {
    document.getElementById('addCriterioForm').style.display = 'block';
    document.getElementById('newCriterioNome').focus();
}

function cancelAddCriterio() {
    document.getElementById('addCriterioForm').style.display = 'none';
    document.getElementById('newCriterioNome').value = '';
    document.getElementById('newCriterioDescrizione').value = '';
    document.getElementById('newCriterioPeso').value = '1';
}

async function addCriterio() {
    const nome = document.getElementById('newCriterioNome').value.trim();
    if (!nome) {
        showNotification('Inserisci il nome del criterio', 'error');
        return;
    }

    const data = {
        rubrica_id: currentRubrica.id,
        nome: nome,
        descrizione: document.getElementById('newCriterioDescrizione').value,
        peso: parseFloat(document.getElementById('newCriterioPeso').value),
        ordine: currentRubrica.criteri ? currentRubrica.criteri.length : 0
    };

    try {
        const response = await fetch('/api/criteri', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification('Criterio aggiunto!', 'success');
            cancelAddCriterio();
            // Ricarica rubrica corrente
            const rubricaResponse = await fetch(`/api/rubriche/${currentRubrica.id}`);
            currentRubrica = await rubricaResponse.json();
            renderCriteri();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

async function deleteCriterio(id) {
    if (!confirm('Eliminare questo criterio?')) return;

    try {
        const response = await fetch(`/api/criteri/${id}`, {method: 'DELETE'});
        const result = await response.json();

        if (result.success) {
            showNotification('Criterio eliminato!', 'success');
            // Ricarica rubrica corrente
            const rubricaResponse = await fetch(`/api/rubriche/${currentRubrica.id}`);
            currentRubrica = await rubricaResponse.json();
            renderCriteri();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== MODAL DESCRITTORI ====================

async function openDescrittoriModal(criterioId) {
    try {
        // Trova il criterio nella rubrica corrente
        currentCriterio = currentRubrica.criteri.find(c => c.id === criterioId);

        document.getElementById('descrittoriModalTitle').textContent = `Livelli di Competenza - ${currentCriterio.nome}`;
        document.getElementById('criterioInfo').innerHTML = `
            <div class="info-box">
                <strong>Criterio:</strong> ${currentCriterio.nome}<br>
                ${currentCriterio.descrizione ? `<em>${currentCriterio.descrizione}</em>` : ''}
            </div>
        `;

        // Carica descrittori esistenti
        if (currentCriterio.descrittori && currentCriterio.descrittori.length > 0) {
            currentCriterio.descrittori.forEach(desc => {
                document.getElementById(`desc_${desc.livello}`).value = desc.descrizione;
                document.getElementById(`desc_${desc.livello}_id`).value = desc.id;
                document.getElementById(`punt_${desc.livello}`).value = desc.punteggio;
            });
        } else {
            // Reset form
            for (let i = 1; i <= 4; i++) {
                document.getElementById(`desc_${i}`).value = '';
                document.getElementById(`desc_${i}_id`).value = '';
            }
            // Valori default
            document.getElementById('punt_4').value = 10;
            document.getElementById('punt_3').value = 8;
            document.getElementById('punt_2').value = 6;
            document.getElementById('punt_1').value = 4;
        }

        document.getElementById('descrittoriModal').style.display = 'block';
    } catch (error) {
        handleApiError(error);
    }
}

function closeDescrittoriModal() {
    document.getElementById('descrittoriModal').style.display = 'none';
    currentCriterio = null;
}

async function saveDescrittori() {
    const livelli = [
        {livello: 4, nome: 'Avanzato'},
        {livello: 3, nome: 'Intermedio'},
        {livello: 2, nome: 'Base'},
        {livello: 1, nome: 'Iniziale'}
    ];

    try {
        for (const liv of livelli) {
            const descrizione = document.getElementById(`desc_${liv.livello}`).value.trim();
            if (!descrizione) {
                showNotification(`Compila il livello ${liv.nome}`, 'error');
                return;
            }

            const id = document.getElementById(`desc_${liv.livello}_id`).value;
            const data = {
                criterio_id: currentCriterio.id,
                livello: liv.livello,
                livello_nome: liv.nome,
                descrizione: descrizione,
                punteggio: parseFloat(document.getElementById(`punt_${liv.livello}`).value)
            };

            const url = id ? `/api/descrittori/${id}` : '/api/descrittori';
            const method = id ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (!result.success) {
                throw new Error(result.error);
            }
        }

        showNotification('Descrittori salvati!', 'success');
        closeDescrittoriModal();

        // Ricarica rubrica corrente per aggiornare i descrittori
        const rubricaResponse = await fetch(`/api/rubriche/${currentRubrica.id}`);
        currentRubrica = await rubricaResponse.json();
        renderCriteri();
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== UTILITIES ====================

function handleApiError(error) {
    console.error('API Error:', error);
    showNotification('Errore di connessione al server', 'error');
}

function showNotification(message, type = 'info') {
    // Rimuovi notifiche esistenti
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add('show'), 10);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Chiudi modal cliccando fuori
window.onclick = function(event) {
    const modals = ['rubricaModal', 'criteriModal', 'descrittoriModal'];
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}
