// Gestione verifiche scritte con criteri di valutazione

let verifiche = [];
let materie = [];
let currentVerifica = null;
let domandaCounter = 0;
let domande = [];

// ==================== CARICAMENTO DATI ====================

async function loadVerifiche() {
    try {
        const filterMateria = document.getElementById('filterMateria').value;

        let url = '/api/verifiche';
        if (filterMateria) {
            url = `/api/verifiche/materia/${filterMateria}`;
        }

        const response = await fetch(url);
        verifiche = await response.json();

        renderVerifiche();
    } catch (error) {
        handleApiError(error);
    }
}

async function loadMaterie() {
    try {
        const response = await fetch('/api/materie');
        materie = await response.json();

        // Popola i filtri
        const filterMateria = document.getElementById('filterMateria');
        filterMateria.innerHTML = '<option value="">Tutte le materie</option>' +
            materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');

        // Popola i select dei form
        const materiaSelects = ['materia_id', 'ai_materia_id'];
        materiaSelects.forEach(selectId => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Seleziona materia</option>' +
                materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
        });
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== RENDERING ====================

function renderVerifiche() {
    const grid = document.getElementById('verifiche-grid');

    if (verifiche.length === 0) {
        grid.innerHTML = '<div class="loading">Nessuna verifica trovata</div>';
        return;
    }

    grid.innerHTML = verifiche.map(verifica => `
        <div class="verifica-card">
            <div class="card-header">
                <h3>${verifica.titolo}</h3>
                ${verifica.generata_ai ? '<span class="badge badge-ai">🤖 AI</span>' : ''}
            </div>
            <p><strong>Materia:</strong> ${verifica.materia_nome}</p>
            ${verifica.descrizione ? `<p>${verifica.descrizione}</p>` : ''}
            ${verifica.argomenti ? `<p><strong>Argomenti:</strong> ${verifica.argomenti}</p>` : ''}
            <div class="verifica-stats">
                <span class="stat">📅 ${formatDate(verifica.data_verifica)}</span>
                ${verifica.durata_minuti ? `<span class="stat">⏱️ ${verifica.durata_minuti} min</span>` : ''}
                <span class="stat">📝 ${verifica.num_domande} domande</span>
                <span class="stat">⭐ ${verifica.punteggio_totale} pt</span>
            </div>
            <div class="card-actions">
                <button class="btn btn-sm btn-info" onclick="viewVerifica(${verifica.id})">Visualizza</button>
                <button class="btn btn-sm btn-primary" onclick="editVerifica(${verifica.id})">Modifica</button>
                <button class="btn btn-sm btn-danger" onclick="deleteVerifica(${verifica.id})">Elimina</button>
            </div>
        </div>
    `).join('');
}

// ==================== MODAL NUOVA VERIFICA ====================

function showAddVerificaModal() {
    document.getElementById('modalTitle').textContent = 'Nuova Verifica';
    document.getElementById('verificaForm').reset();
    document.getElementById('verificaId').value = '';
    domande = [];
    domandaCounter = 0;
    renderDomande();
    document.getElementById('verificaModal').classList.add('show');
}

function closeVerificaModal() {
    document.getElementById('verificaModal').classList.remove('show');
}

// ==================== GESTIONE DOMANDE ====================

function addDomanda() {
    const domanda = {
        id: ++domandaCounter,
        numero: domande.length + 1,
        testo: '',
        tipo: 'aperta',
        punteggio: 0,
        opzioni: '',
        risposta_corretta: '',
        righe_risposta: 5,
        note: '',
        criteri: []
    };
    domande.push(domanda);
    renderDomande();
}

function removeDomanda(id) {
    domande = domande.filter(d => d.id !== id);
    // Rinumera le domande
    domande.forEach((d, idx) => d.numero = idx + 1);
    renderDomande();
}

function addCriterio(domandaId) {
    const domanda = domande.find(d => d.id === domandaId);
    if (!domanda) return;

    domanda.criteri.push({
        id: Date.now(),
        descrizione: '',
        punteggio: 0
    });
    renderDomande();
}

function removeCriterio(domandaId, criterioId) {
    const domanda = domande.find(d => d.id === domandaId);
    if (!domanda) return;

    domanda.criteri = domanda.criteri.filter(c => c.id !== criterioId);
    renderDomande();
}

function renderDomande() {
    const container = document.getElementById('domande-container');

    if (domande.length === 0) {
        container.innerHTML = '<div class="empty-state">Nessuna domanda. Clicca "+ Aggiungi Domanda" per iniziare.</div>';
        updatePunteggioTotale();
        return;
    }

    container.innerHTML = domande.map(domanda => `
        <div class="domanda-item" data-id="${domanda.id}">
            <div class="domanda-header">
                <h5>Domanda ${domanda.numero}</h5>
                <button type="button" class="btn-icon btn-danger" onclick="removeDomanda(${domanda.id})" title="Rimuovi domanda">×</button>
            </div>

            <div class="form-row">
                <div class="form-group flex-grow">
                    <label>Testo domanda *</label>
                    <textarea class="domanda-testo" data-id="${domanda.id}" rows="2" required>${domanda.testo}</textarea>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label>Tipo</label>
                    <select class="domanda-tipo" data-id="${domanda.id}" onchange="updateDomandaTipo(${domanda.id})">
                        <option value="aperta" ${domanda.tipo === 'aperta' ? 'selected' : ''}>Aperta</option>
                        <option value="multipla" ${domanda.tipo === 'multipla' ? 'selected' : ''}>Scelta Multipla</option>
                        <option value="vero_falso" ${domanda.tipo === 'vero_falso' ? 'selected' : ''}>Vero/Falso</option>
                        <option value="esercizio" ${domanda.tipo === 'esercizio' ? 'selected' : ''}>Esercizio</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Punteggio *</label>
                    <input type="number" class="domanda-punteggio" data-id="${domanda.id}" step="0.5" min="0" value="${domanda.punteggio}" required onchange="updatePunteggioTotale()">
                </div>

                <div class="form-group">
                    <label>Righe risposta</label>
                    <input type="number" class="domanda-righe" data-id="${domanda.id}" min="1" value="${domanda.righe_risposta}">
                </div>
            </div>

            ${domanda.tipo === 'multipla' || domanda.tipo === 'vero_falso' ? `
                <div class="form-group">
                    <label>Opzioni ${domanda.tipo === 'multipla' ? '(A, B, C, D...)' : '(Vero/Falso)'}</label>
                    <input type="text" class="domanda-opzioni" data-id="${domanda.id}" value="${domanda.opzioni}" placeholder="A) ... B) ... C) ...">
                </div>
                <div class="form-group">
                    <label>Risposta corretta</label>
                    <input type="text" class="domanda-risposta" data-id="${domanda.id}" value="${domanda.risposta_corretta}" placeholder="Es: A">
                </div>
            ` : ''}

            <div class="criteri-section">
                <div class="criteri-header">
                    <label>Criteri di Valutazione</label>
                    <button type="button" class="btn btn-xs btn-success" onclick="addCriterio(${domanda.id})">+ Criterio</button>
                </div>
                <div class="criteri-list">
                    ${domanda.criteri.length === 0 ? '<p class="empty-state-sm">Nessun criterio</p>' : ''}
                    ${domanda.criteri.map(criterio => `
                        <div class="criterio-item">
                            <input type="text" class="criterio-descrizione" data-domanda-id="${domanda.id}" data-criterio-id="${criterio.id}"
                                value="${criterio.descrizione}" placeholder="Descrizione criterio" required>
                            <input type="number" class="criterio-punteggio" data-domanda-id="${domanda.id}" data-criterio-id="${criterio.id}"
                                value="${criterio.punteggio}" step="0.25" min="0" placeholder="Pt" style="width: 80px;" required>
                            <button type="button" class="btn-icon btn-danger" onclick="removeCriterio(${domanda.id}, ${criterio.id})">×</button>
                        </div>
                    `).join('')}
                </div>
            </div>

            <div class="form-group">
                <label>Note (visibili solo al docente)</label>
                <textarea class="domanda-note" data-id="${domanda.id}" rows="1">${domanda.note || ''}</textarea>
            </div>
        </div>
    `).join('');

    updatePunteggioTotale();
}

function updateDomandaTipo(domandaId) {
    const domanda = domande.find(d => d.id === domandaId);
    if (!domanda) return;

    const tipoSelect = document.querySelector(`.domanda-tipo[data-id="${domandaId}"]`);
    domanda.tipo = tipoSelect.value;

    renderDomande();
}

function updatePunteggioTotale() {
    collectDomandeData();
    const totale = domande.reduce((sum, d) => sum + parseFloat(d.punteggio || 0), 0);
    document.getElementById('punteggioTotale').textContent = `Totale: ${totale.toFixed(1)} pt`;
}

function collectDomandeData() {
    domande.forEach(domanda => {
        const testoEl = document.querySelector(`.domanda-testo[data-id="${domanda.id}"]`);
        const tipoEl = document.querySelector(`.domanda-tipo[data-id="${domanda.id}"]`);
        const punteggioEl = document.querySelector(`.domanda-punteggio[data-id="${domanda.id}"]`);
        const righeEl = document.querySelector(`.domanda-righe[data-id="${domanda.id}"]`);
        const noteEl = document.querySelector(`.domanda-note[data-id="${domanda.id}"]`);

        if (testoEl) domanda.testo = testoEl.value;
        if (tipoEl) domanda.tipo = tipoEl.value;
        if (punteggioEl) domanda.punteggio = parseFloat(punteggioEl.value) || 0;
        if (righeEl) domanda.righe_risposta = parseInt(righeEl.value) || 5;
        if (noteEl) domanda.note = noteEl.value;

        const opzioniEl = document.querySelector(`.domanda-opzioni[data-id="${domanda.id}"]`);
        const rispostaEl = document.querySelector(`.domanda-risposta[data-id="${domanda.id}"]`);
        if (opzioniEl) domanda.opzioni = opzioniEl.value;
        if (rispostaEl) domanda.risposta_corretta = rispostaEl.value;

        // Collect criteri data
        domanda.criteri.forEach(criterio => {
            const descrizioneEl = document.querySelector(`.criterio-descrizione[data-domanda-id="${domanda.id}"][data-criterio-id="${criterio.id}"]`);
            const punteggioCritEl = document.querySelector(`.criterio-punteggio[data-domanda-id="${domanda.id}"][data-criterio-id="${criterio.id}"]`);

            if (descrizioneEl) criterio.descrizione = descrizioneEl.value;
            if (punteggioCritEl) criterio.punteggio = parseFloat(punteggioCritEl.value) || 0;
        });
    });
}

// ==================== SALVA VERIFICA ====================

async function saveVerifica(event) {
    event.preventDefault();

    collectDomandeData();

    const id = document.getElementById('verificaId').value;
    const data = {
        materia_id: parseInt(document.getElementById('materia_id').value),
        titolo: document.getElementById('titolo').value,
        descrizione: document.getElementById('descrizione').value,
        argomenti: document.getElementById('argomenti').value,
        data_verifica: document.getElementById('data_verifica').value,
        durata_minuti: parseInt(document.getElementById('durata_minuti').value) || null,
        domande: domande.map(d => ({
            numero: d.numero,
            testo: d.testo,
            tipo: d.tipo,
            punteggio: d.punteggio,
            opzioni: d.opzioni,
            risposta_corretta: d.risposta_corretta,
            righe_risposta: d.righe_risposta,
            note: d.note,
            criteri: d.criteri.map(c => ({
                descrizione: c.descrizione,
                punteggio: c.punteggio
            }))
        }))
    };

    try {
        const url = id ? `/api/verifiche/${id}` : '/api/verifiche';
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification(id ? 'Verifica aggiornata!' : 'Verifica creata con successo!');
            closeVerificaModal();
            loadVerifiche();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== VISUALIZZA VERIFICA ====================

async function viewVerifica(id) {
    try {
        const response = await fetch(`/api/verifiche/${id}`);
        const verifica = await response.json();

        document.getElementById('viewModalTitle').textContent = verifica.titolo;

        const content = `
            <div class="verifica-details">
                <div class="verifica-meta">
                    <p><strong>Materia:</strong> ${verifica.materia_nome}</p>
                    <p><strong>Data:</strong> ${formatDate(verifica.data_verifica)}</p>
                    ${verifica.durata_minuti ? `<p><strong>Durata:</strong> ${verifica.durata_minuti} minuti</p>` : ''}
                    <p><strong>Punteggio Totale:</strong> ${verifica.punteggio_totale} punti</p>
                    ${verifica.argomenti ? `<p><strong>Argomenti:</strong> ${verifica.argomenti}</p>` : ''}
                    ${verifica.descrizione ? `<p><strong>Descrizione:</strong> ${verifica.descrizione}</p>` : ''}
                </div>

                <div class="domande-view">
                    <h4>Domande</h4>
                    ${verifica.domande.map(domanda => `
                        <div class="domanda-view-item">
                            <div class="domanda-view-header">
                                <strong>Domanda ${domanda.numero}</strong>
                                <span class="badge">${domanda.tipo}</span>
                                <span class="badge badge-primary">${domanda.punteggio} pt</span>
                            </div>
                            <p class="domanda-view-testo">${domanda.testo}</p>

                            ${domanda.opzioni ? `<p class="domanda-view-opzioni"><strong>Opzioni:</strong> ${domanda.opzioni}</p>` : ''}
                            ${domanda.risposta_corretta ? `<p class="domanda-view-risposta"><strong>Risposta corretta:</strong> ${domanda.risposta_corretta}</p>` : ''}

                            ${domanda.criteri && domanda.criteri.length > 0 ? `
                                <div class="criteri-view">
                                    <strong>Criteri di Valutazione:</strong>
                                    <ul>
                                        ${domanda.criteri.map(c => `<li>${c.descrizione} <span class="badge-sm">${c.punteggio} pt</span></li>`).join('')}
                                    </ul>
                                </div>
                            ` : ''}

                            ${domanda.note ? `<p class="domanda-view-note"><em>Note: ${domanda.note}</em></p>` : ''}
                            <p class="domanda-view-spazio"><em>Spazio risposta: ${domanda.righe_risposta} righe</em></p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;

        document.getElementById('viewVerificaContent').innerHTML = content;
        currentVerifica = verifica;
        document.getElementById('viewVerificaModal').classList.add('show');
    } catch (error) {
        handleApiError(error);
    }
}

function closeViewModal() {
    document.getElementById('viewVerificaModal').classList.remove('show');
    currentVerifica = null;
}

// ==================== MODIFICA VERIFICA ====================

async function editVerifica(id) {
    try {
        const response = await fetch(`/api/verifiche/${id}`);
        const verifica = await response.json();

        document.getElementById('modalTitle').textContent = 'Modifica Verifica';
        document.getElementById('verificaId').value = verifica.id;
        document.getElementById('materia_id').value = verifica.materia_id;
        document.getElementById('titolo').value = verifica.titolo;
        document.getElementById('descrizione').value = verifica.descrizione || '';
        document.getElementById('argomenti').value = verifica.argomenti || '';
        document.getElementById('data_verifica').value = verifica.data_verifica;
        document.getElementById('durata_minuti').value = verifica.durata_minuti || '';

        // Carica le domande
        domande = verifica.domande.map((d, idx) => ({
            id: ++domandaCounter,
            numero: d.numero,
            testo: d.testo,
            tipo: d.tipo,
            punteggio: d.punteggio,
            opzioni: d.opzioni || '',
            risposta_corretta: d.risposta_corretta || '',
            righe_risposta: d.righe_risposta,
            note: d.note || '',
            criteri: d.criteri ? d.criteri.map(c => ({
                id: Date.now() + Math.random(),
                descrizione: c.descrizione,
                punteggio: c.punteggio
            })) : []
        }));

        renderDomande();
        document.getElementById('verificaModal').classList.add('show');
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== ELIMINA VERIFICA ====================

async function deleteVerifica(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questa verifica? Saranno eliminate anche tutte le domande e i criteri di valutazione.')) {
        return;
    }

    try {
        const response = await fetch(`/api/verifiche/${id}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            showNotification('Verifica eliminata con successo');
            loadVerifiche();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== GENERATORE AI ====================

function showGeneraAIModal() {
    document.getElementById('generaAIModal').classList.add('show');
}

function closeGeneraAIModal() {
    document.getElementById('generaAIModal').classList.remove('show');
}

async function generaVerificaAI(event) {
    event.preventDefault();

    const data = {
        materia_id: parseInt(document.getElementById('ai_materia_id').value),
        argomenti: document.getElementById('ai_argomenti').value,
        num_domande: parseInt(document.getElementById('ai_num_domande').value),
        punteggio_totale: parseFloat(document.getElementById('ai_punteggio_totale').value),
        difficolta: document.getElementById('ai_difficolta').value,
        tipo_domande: document.getElementById('ai_tipo_domande').value
    };

    try {
        showNotification('🤖 Generazione in corso con Claude AI...', 'info');

        const response = await fetch('/api/verifiche/genera-ai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            showNotification('✅ Verifica generata! Rivedi e salva.');
            closeGeneraAIModal();

            // Popola il form con i dati generati
            const verificaData = result.verifica_data;

            document.getElementById('modalTitle').textContent = 'Nuova Verifica (Generata da AI)';
            document.getElementById('verificaId').value = '';
            document.getElementById('materia_id').value = data.materia_id;
            document.getElementById('titolo').value = verificaData.titolo;
            document.getElementById('descrizione').value = verificaData.descrizione || '';
            document.getElementById('argomenti').value = data.argomenti;
            document.getElementById('data_verifica').value = '';
            document.getElementById('durata_minuti').value = '';

            // Carica domande generate
            domande = verificaData.domande.map((d, idx) => ({
                id: ++domandaCounter,
                numero: d.numero || (idx + 1),
                testo: d.testo,
                tipo: d.tipo || 'aperta',
                punteggio: d.punteggio,
                opzioni: d.opzioni || '',
                risposta_corretta: d.risposta_corretta || '',
                righe_risposta: d.righe_risposta || 5,
                note: d.note || '',
                criteri: (d.criteri || []).map(c => ({
                    id: Date.now() + Math.random(),
                    descrizione: c.descrizione,
                    punteggio: c.punteggio
                }))
            }));

            renderDomande();
            document.getElementById('verificaModal').classList.add('show');
        } else {
            showNotification('❌ Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// ==================== EXPORT PDF ====================

function exportVerificaPDF() {
    if (!currentVerifica) return;

    showNotification('Funzionalità export PDF in sviluppo', 'info');
    // TODO: Implementare export PDF con libreria come jsPDF
}

// ==================== INIT ====================

loadMaterie().then(() => loadVerifiche());
