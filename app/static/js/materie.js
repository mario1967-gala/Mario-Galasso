// Gestione materie

let materie = [];

// Carica tutte le materie
async function loadMaterie() {
    try {
        const response = await fetch('/api/materie');
        materie = await response.json();
        renderMaterie();
    } catch (error) {
        handleApiError(error);
    }
}

// Renderizza le card delle materie
function renderMaterie() {
    const grid = document.getElementById('materie-grid');

    if (materie.length === 0) {
        grid.innerHTML = '<div class="loading">Nessuna materia trovata</div>';
        return;
    }

    grid.innerHTML = materie.map(materia => `
        <div class="card">
            <h3>${materia.nome}</h3>
            <p>${materia.descrizione || 'Nessuna descrizione'}</p>
            <p><strong>Ore settimanali:</strong> ${materia.ore_settimanali || '-'}</p>
            <p><strong>Docente:</strong> ${materia.docente || '-'}</p>
            <div class="card-actions">
                <button class="btn btn-sm btn-primary" onclick="editMateria(${materia.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deleteMateria(${materia.id})">Elimina</button>
            </div>
        </div>
    `).join('');
}

// Mostra modal per aggiungere materia
function showAddMateriaModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Materia';
    document.getElementById('materiaForm').reset();
    document.getElementById('materiaId').value = '';
    document.getElementById('materiaModal').classList.add('show');
}

// Modifica materia
function editMateria(id) {
    const materia = materie.find(m => m.id === id);
    if (!materia) return;

    document.getElementById('modalTitle').textContent = 'Modifica Materia';
    document.getElementById('materiaId').value = materia.id;
    document.getElementById('nome').value = materia.nome;
    document.getElementById('descrizione').value = materia.descrizione || '';
    document.getElementById('ore_settimanali').value = materia.ore_settimanali || '';
    document.getElementById('docente').value = materia.docente || '';
    document.getElementById('materiaModal').classList.add('show');
}

// Salva materia
async function saveMateria(event) {
    event.preventDefault();

    const id = document.getElementById('materiaId').value;
    const data = {
        nome: document.getElementById('nome').value,
        descrizione: document.getElementById('descrizione').value,
        ore_settimanali: document.getElementById('ore_settimanali').value ? parseInt(document.getElementById('ore_settimanali').value) : null,
        docente: document.getElementById('docente').value
    };

    try {
        const url = id ? `/api/materie/${id}` : '/api/materie';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Materia aggiornata con successo' : 'Materia creata con successo');
            closeModal();
            loadMaterie();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina materia
async function deleteMateria(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questa materia? Tutti i dati associati verranno eliminati.')) {
        return;
    }

    try {
        const response = await fetch(`/api/materie/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Materia eliminata con successo');
            loadMaterie();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('materiaModal').classList.remove('show');
}

// Carica materie all'avvio
loadMaterie();
