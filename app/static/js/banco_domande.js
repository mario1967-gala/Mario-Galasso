// Gestione Banco Domande

let domande = [];
let materie = [];
let argomenti = new Set();

// Carica domande con filtri
async function loadDomande() {
    try {
        const filterMateria = document.getElementById('filterMateria').value;
        const filterArgomento = document.getElementById('filterArgomento').value;
        const filterDifficolta = document.getElementById('filterDifficolta').value;
        const filterTipo = document.getElementById('filterTipo').value;

        const response = await fetch('/api/domande');
        let allDomande = await response.json();

        // Applica filtri
        domande = allDomande.filter(d => {
            if (filterMateria && d.materia_id != filterMateria) return false;
            if (filterArgomento && d.argomento !== filterArgomento) return false;
            if (filterDifficolta && d.difficolta !== filterDifficolta) return false;
            if (filterTipo && d.tipo !== filterTipo) return false;
            return true;
        });

        renderDomande();
        updateDomandeCount();
        updateArgomentiFilter(allDomande);
    } catch (error) {
        handleApiError(error);
    }
}

// Carica materie
async function loadMaterie() {
    try {
        const response = await fetch('/api/materie');
        materie = await response.json();

        const materiaSelects = ['filterMateria', 'materia_id'];
        materiaSelects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (selectId === 'filterMateria') {
                select.innerHTML = '<option value="">Tutte le materie</option>' +
                    materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
            } else {
                select.innerHTML = '<option value="">Seleziona materia</option>' +
                    materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
            }
        });
    } catch (error) {
        handleApiError(error);
    }
}

// Aggiorna filtro argomenti in base alle domande esistenti
function updateArgomentiFilter(allDomande) {
    argomenti = new Set();
    allDomande.forEach(d => {
        if (d.argomento) argomenti.add(d.argomento);
    });

    const select = document.getElementById('filterArgomento');
    const currentValue = select.value;

    select.innerHTML = '<option value="">Tutti gli argomenti</option>' +
        Array.from(argomenti).sort().map(a => `<option value="${a}">${a}</option>`).join('');

    if (currentValue && argomenti.has(currentValue)) {
        select.value = currentValue;
    }
}

// Renderizza tabella domande
function renderDomande() {
    const tbody = document.getElementById('domande-tbody');

    if (domande.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nessuna domanda trovata</td></tr>';
        return;
    }

    tbody.innerHTML = domande.map(domanda => {
        // Tronca testo per anteprima
        const testoPreview = domanda.testo.length > 80
            ? domanda.testo.substring(0, 80) + '...'
            : domanda.testo;

        const tipoLabels = {
            'aperta': 'Aperta',
            'multipla': 'Multipla',
            'vero_falso': 'Vero/Falso'
        };

        const difficoltaColors = {
            'facile': '#4caf50',
            'media': '#ff9800',
            'difficile': '#f44336'
        };

        return `
            <tr>
                <td>${domanda.materia_nome || '-'}</td>
                <td>${domanda.argomento || '-'}</td>
                <td>${testoPreview}</td>
                <td>${tipoLabels[domanda.tipo] || domanda.tipo}</td>
                <td><span style="color: ${difficoltaColors[domanda.difficolta]}; font-weight: bold;">${domanda.difficolta || '-'}</span></td>
                <td>${domanda.punteggio_default}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewDomanda(${domanda.id})">Vedi</button>
                    <button class="btn btn-sm btn-primary" onclick="editDomanda(${domanda.id})">Modifica</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteDomanda(${domanda.id})">Elimina</button>
                </td>
            </tr>
        `;
    }).join('');
}

// Aggiorna contatore
function updateDomandeCount() {
    const countDiv = document.getElementById('domande-count');
    if (!countDiv) return;

    const filterMateria = document.getElementById('filterMateria').value;
    const filterArgomento = document.getElementById('filterArgomento').value;

    let messaggio = `<strong>${domande.length}</strong> domande`;

    if (filterMateria) {
        const materia = materie.find(m => m.id == filterMateria);
        if (materia) messaggio += ` - Materia: <strong>${materia.nome}</strong>`;
    }

    if (filterArgomento) {
        messaggio += ` - Argomento: <strong>${filterArgomento}</strong>`;
    }

    countDiv.innerHTML = messaggio;
}

// Mostra modal aggiungi domanda
function showAddDomandaModal() {
    document.getElementById('modalTitle').textContent = 'Aggiungi Domanda';
    document.getElementById('domandaForm').reset();
    document.getElementById('domandaId').value = '';
    document.getElementById('punteggio_default').value = '1';
    toggleOpzioniMultipla();
    clearPreviews();
    document.getElementById('domandaModal').classList.add('show');
}

// Visualizza domanda (modal sola lettura)
async function viewDomanda(id) {
    const domanda = domande.find(d => d.id === id);
    if (!domanda) return;

    // Riusa il modal di modifica ma in modalità visualizzazione
    editDomanda(id);

    // Disabilita tutti i campi
    const form = document.getElementById('domandaForm');
    const inputs = form.querySelectorAll('input, textarea, select, button[type="submit"]');
    inputs.forEach(input => input.disabled = true);

    document.getElementById('modalTitle').textContent = 'Visualizza Domanda';
}

// Modifica domanda
function editDomanda(id) {
    const domanda = domande.find(d => d.id === id);
    if (!domanda) return;

    document.getElementById('modalTitle').textContent = 'Modifica Domanda';
    document.getElementById('domandaId').value = domanda.id;
    document.getElementById('materia_id').value = domanda.materia_id || '';
    document.getElementById('argomento').value = domanda.argomento || '';
    document.getElementById('tipo').value = domanda.tipo || 'aperta';
    document.getElementById('difficolta').value = domanda.difficolta || 'media';
    document.getElementById('punteggio_default').value = domanda.punteggio_default || 1;
    document.getElementById('testo').value = domanda.testo || '';
    document.getElementById('soluzione').value = domanda.soluzione || '';
    document.getElementById('note').value = domanda.note || '';

    // Carica opzioni multipla se presente
    if (domanda.tipo === 'multipla' && domanda.opzioni_json) {
        try {
            const opzioni = JSON.parse(domanda.opzioni_json);
            document.getElementById('opzione-a').value = opzioni.a || '';
            document.getElementById('opzione-b').value = opzioni.b || '';
            document.getElementById('opzione-c').value = opzioni.c || '';
            document.getElementById('opzione-d').value = opzioni.d || '';
        } catch (e) {
            console.error('Errore parsing opzioni:', e);
        }
    }

    toggleOpzioniMultipla();
    updatePreview();
    document.getElementById('domandaModal').classList.add('show');
}

// Toggle opzioni multipla
function toggleOpzioniMultipla() {
    const tipo = document.getElementById('tipo').value;
    const opzioniGroup = document.getElementById('opzioni-multipla-group');

    if (tipo === 'multipla') {
        opzioniGroup.style.display = 'block';
    } else {
        opzioniGroup.style.display = 'none';
    }
}

// Aggiorna preview con MathJax
function updatePreview() {
    const testo = document.getElementById('testo').value;
    const soluzione = document.getElementById('soluzione').value;

    const previewTesto = document.getElementById('preview-testo');
    const previewSoluzione = document.getElementById('preview-soluzione');

    previewTesto.textContent = testo || 'Nessun testo';
    previewSoluzione.textContent = soluzione || 'Nessuna soluzione';

    // Renderizza con MathJax se disponibile
    if (window.MathJax) {
        MathJax.typesetPromise([previewTesto, previewSoluzione]).catch((err) => console.log(err));
    }
}

// Clear previews
function clearPreviews() {
    document.getElementById('preview-testo').textContent = 'Nessun testo';
    document.getElementById('preview-soluzione').textContent = 'Nessuna soluzione';
}

// Event listeners per preview live
document.addEventListener('DOMContentLoaded', function() {
    const testoInput = document.getElementById('testo');
    const soluzioneInput = document.getElementById('soluzione');

    if (testoInput) {
        testoInput.addEventListener('input', updatePreview);
    }
    if (soluzioneInput) {
        soluzioneInput.addEventListener('input', updatePreview);
    }
});

// Salva domanda
async function saveDomanda(event) {
    event.preventDefault();

    const id = document.getElementById('domandaId').value;
    const tipo = document.getElementById('tipo').value;

    const data = {
        materia_id: parseInt(document.getElementById('materia_id').value),
        testo: document.getElementById('testo').value,
        argomento: document.getElementById('argomento').value,
        difficolta: document.getElementById('difficolta').value,
        tipo: tipo,
        soluzione: document.getElementById('soluzione').value,
        punteggio_default: parseFloat(document.getElementById('punteggio_default').value),
        note: document.getElementById('note').value
    };

    // Aggiungi opzioni se scelta multipla
    if (tipo === 'multipla') {
        const opzioni = {
            a: document.getElementById('opzione-a').value,
            b: document.getElementById('opzione-b').value,
            c: document.getElementById('opzione-c').value,
            d: document.getElementById('opzione-d').value
        };
        data.opzioni_json = JSON.stringify(opzioni);
    }

    try {
        const url = id ? `/api/domande/${id}` : '/api/domande';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Domanda aggiornata con successo' : 'Domanda creata con successo');
            closeModal();
            loadDomande();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina domanda
async function deleteDomanda(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questa domanda? Verrà rimossa anche dalle verifiche che la utilizzano.')) {
        return;
    }

    try {
        const response = await fetch(`/api/domande/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Domanda eliminata con successo');
            loadDomande();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Chiudi modal
function closeModal() {
    document.getElementById('domandaModal').classList.remove('show');

    // Riabilita eventuali campi disabilitati (da viewDomanda)
    const form = document.getElementById('domandaForm');
    const inputs = form.querySelectorAll('input, textarea, select, button');
    inputs.forEach(input => input.disabled = false);
}

// Carica dati all'avvio
Promise.all([loadMaterie(), loadDomande()]);
