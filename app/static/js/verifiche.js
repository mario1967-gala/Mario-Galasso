// Gestione Verifiche

let verifiche = [];
let classi = [];
let materie = [];
let bancoDomande = [];
let domandeSelezionate = [];
let argomentiDisponibili = new Set();

// Carica verifiche con filtri
async function loadVerifiche() {
    try {
        const filterClasse = document.getElementById('filterClasse').value;
        const filterMateria = document.getElementById('filterMateria').value;
        const filterStato = document.getElementById('filterStato').value;

        const response = await fetch('/api/verifiche');
        let allVerifiche = await response.json();

        // Applica filtri
        verifiche = allVerifiche.filter(v => {
            if (filterClasse && v.classe_id != filterClasse) return false;
            if (filterMateria && v.materia_id != filterMateria) return false;
            if (filterStato && v.stato !== filterStato) return false;
            return true;
        });

        renderVerifiche();
        updateVerificheCount();
    } catch (error) {
        handleApiError(error);
    }
}

// Renderizza tabella verifiche
function renderVerifiche() {
    const tbody = document.getElementById('verifiche-tbody');

    if (verifiche.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">Nessuna verifica trovata</td></tr>';
        return;
    }

    tbody.innerHTML = verifiche.map(verifica => {
        const statoClass = `stato-${verifica.stato}`;
        const dataStr = verifica.data_somministrazione
            ? new Date(verifica.data_somministrazione).toLocaleDateString('it-IT')
            : '-';

        return `
            <tr>
                <td><strong>${verifica.titolo}</strong></td>
                <td>${verifica.materia_nome || '-'}</td>
                <td>${verifica.classe_nome || '-'}</td>
                <td>${dataStr}</td>
                <td>${verifica.durata_minuti ? verifica.durata_minuti + ' min' : '-'}</td>
                <td>${verifica.num_domande || 0}</td>
                <td>${verifica.num_versioni || 1}</td>
                <td><span class="stato-badge ${statoClass}">${verifica.stato}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewVerifica(${verifica.id})">Dettagli</button>
                    <button class="btn btn-sm btn-primary" onclick="editVerifica(${verifica.id})">Modifica</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteVerifica(${verifica.id})">Elimina</button>
                </td>
            </tr>
        `;
    }).join('');
}

// Aggiorna contatore
function updateVerificheCount() {
    const countDiv = document.getElementById('verifiche-count');
    if (!countDiv) return;

    let messaggio = `<strong>${verifiche.length}</strong> verifiche`;

    const filterClasse = document.getElementById('filterClasse').value;
    const filterMateria = document.getElementById('filterMateria').value;

    if (filterClasse) {
        const classe = classi.find(c => c.id == filterClasse);
        if (classe) messaggio += ` - Classe: <strong>${classe.nome}</strong>`;
    }

    if (filterMateria) {
        const materia = materie.find(m => m.id == filterMateria);
        if (materia) messaggio += ` - Materia: <strong>${materia.nome}</strong>`;
    }

    countDiv.innerHTML = messaggio;
}

// Carica classi
async function loadClassi() {
    try {
        const response = await fetch('/api/classi');
        classi = await response.json();

        const classeSelects = ['filterClasse', 'classe_id'];
        classeSelects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (selectId === 'filterClasse') {
                select.innerHTML = '<option value="">Tutte le classi</option>' +
                    classi.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
            } else {
                select.innerHTML = '<option value="">Seleziona classe</option>' +
                    classi.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
            }
        });
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

// Mostra modal aggiungi verifica
function showAddVerificaModal() {
    document.getElementById('modalTitle').textContent = 'Crea Nuova Verifica';
    document.getElementById('verificaForm').reset();
    document.getElementById('verificaId').value = '';
    document.getElementById('num_versioni').value = '1';
    document.getElementById('stato').value = 'bozza';
    domandeSelezionate = [];
    bancoDomande = [];
    updateDomandeSelezionateView();
    document.getElementById('banco-domande-list').innerHTML =
        '<p style="color: #999; text-align: center;">Seleziona una materia per vedere le domande</p>';
    document.getElementById('verificaModal').classList.add('show');
}

// Visualizza dettagli verifica
async function viewVerifica(id) {
    try {
        const response = await fetch(`/api/verifiche/${id}`);
        const verifica = await response.json();

        const dataStr = verifica.data_somministrazione
            ? new Date(verifica.data_somministrazione).toLocaleDateString('it-IT')
            : 'Non specificata';

        const statoClass = `stato-${verifica.stato}`;

        let html = `
            <div style="padding: 1rem;">
                <h4>${verifica.titolo}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.5rem 0;">
                    <div>
                        <strong>Classe:</strong> ${verifica.classe_nome || '-'}<br>
                        <strong>Materia:</strong> ${verifica.materia_nome || '-'}<br>
                        <strong>Argomento:</strong> ${verifica.argomento || '-'}
                    </div>
                    <div>
                        <strong>Data:</strong> ${dataStr}<br>
                        <strong>Durata:</strong> ${verifica.durata_minuti || '-'} minuti<br>
                        <strong>Stato:</strong> <span class="stato-badge ${statoClass}">${verifica.stato}</span>
                    </div>
                </div>

                <div style="margin: 1.5rem 0;">
                    <strong>Configurazione:</strong><br>
                    Numero versioni: ${verifica.num_versioni || 1}<br>
                    Mescola domande: ${verifica.mescola_domande ? 'Sì' : 'No'}
                </div>

                ${verifica.istruzioni ? `
                    <div style="margin: 1.5rem 0; padding: 1rem; background: #f5f5f5; border-radius: 4px;">
                        <strong>Istruzioni:</strong><br>
                        ${verifica.istruzioni}
                    </div>
                ` : ''}

                <h5>Domande (${verifica.domande ? verifica.domande.length : 0})</h5>
                <div style="max-height: 400px; overflow-y: auto;">
                    ${renderDomandeDettaglio(verifica.domande || [])}
                </div>

                <div style="margin-top: 1rem; padding: 1rem; background: #e8f5e9; border-radius: 4px;">
                    <strong>Punteggio Totale: ${verifica.punteggio_totale || 0} punti</strong>
                </div>
            </div>
        `;

        document.getElementById('dettaglioContent').innerHTML = html;
        document.getElementById('dettaglioModal').classList.add('show');

        // Renderizza LaTeX se presente
        if (window.MathJax) {
            MathJax.typesetPromise([document.getElementById('dettaglioContent')]).catch((err) => console.log(err));
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Renderizza domande per dettaglio
function renderDomandeDettaglio(domande) {
    if (!domande || domande.length === 0) {
        return '<p style="color: #999; text-align: center;">Nessuna domanda</p>';
    }

    return domande.map((d, idx) => {
        const difficoltaClass = `difficolta-${d.difficolta}`;
        const testoPreview = d.testo.length > 100 ? d.testo.substring(0, 100) + '...' : d.testo;

        return `
            <div style="border: 1px solid #ddd; border-radius: 4px; padding: 0.75rem; margin-bottom: 0.5rem; background: white;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <strong>${idx + 1}. </strong>
                        <span class="difficolta-badge ${difficoltaClass}">${d.difficolta}</span>
                        <span style="color: #666; font-size: 0.9rem;"> - ${d.tipo}</span>
                        <div style="margin: 0.5rem 0; color: #333;">${testoPreview}</div>
                        <div style="font-size: 0.85rem; color: #999;">
                            Argomento: ${d.argomento || '-'}
                        </div>
                    </div>
                    <div style="text-align: right; margin-left: 1rem;">
                        <strong style="color: #4CAF50;">${d.punteggio} punti</strong>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Modifica verifica
async function editVerifica(id) {
    try {
        const response = await fetch(`/api/verifiche/${id}`);
        const verifica = await response.json();

        document.getElementById('modalTitle').textContent = 'Modifica Verifica';
        document.getElementById('verificaId').value = verifica.id;
        document.getElementById('titolo').value = verifica.titolo || '';
        document.getElementById('classe_id').value = verifica.classe_id || '';
        document.getElementById('materia_id').value = verifica.materia_id || '';
        document.getElementById('argomento').value = verifica.argomento || '';
        document.getElementById('data_somministrazione').value = verifica.data_somministrazione || '';
        document.getElementById('durata_minuti').value = verifica.durata_minuti || '';
        document.getElementById('num_versioni').value = verifica.num_versioni || 1;
        document.getElementById('mescola_domande').checked = verifica.mescola_domande || false;
        document.getElementById('istruzioni').value = verifica.istruzioni || '';
        document.getElementById('stato').value = verifica.stato || 'bozza';

        // Carica domande selezionate
        domandeSelezionate = verifica.domande || [];
        updateDomandeSelezionateView();

        // Carica banco domande per la materia
        if (verifica.materia_id) {
            await updateDomandeByMateria();
        }

        document.getElementById('verificaModal').classList.add('show');
    } catch (error) {
        handleApiError(error);
    }
}

// Aggiorna banco domande quando cambia materia
async function updateDomandeByMateria() {
    const materiaId = document.getElementById('materia_id').value;

    if (!materiaId) {
        bancoDomande = [];
        document.getElementById('banco-domande-list').innerHTML =
            '<p style="color: #999; text-align: center;">Seleziona una materia per vedere le domande</p>';
        return;
    }

    try {
        const response = await fetch('/api/domande');
        const allDomande = await response.json();

        bancoDomande = allDomande.filter(d => d.materia_id == materiaId);

        // Aggiorna argomenti disponibili
        argomentiDisponibili = new Set();
        bancoDomande.forEach(d => {
            if (d.argomento) argomentiDisponibili.add(d.argomento);
        });

        const selectArgomento = document.getElementById('filterArgomento');
        selectArgomento.innerHTML = '<option value="">Tutti gli argomenti</option>' +
            Array.from(argomentiDisponibili).sort().map(a => `<option value="${a}">${a}</option>`).join('');

        filterBancoDomande();
    } catch (error) {
        handleApiError(error);
    }
}

// Filtra banco domande
function filterBancoDomande() {
    const searchText = document.getElementById('searchDomande').value.toLowerCase();
    const filterArgomento = document.getElementById('filterArgomento').value;
    const filterDifficolta = document.getElementById('filterDifficolta').value;

    let filtrate = bancoDomande.filter(d => {
        // Escludi domande già selezionate
        if (domandeSelezionate.find(ds => ds.id === d.id)) return false;

        if (searchText && !d.testo.toLowerCase().includes(searchText)) return false;
        if (filterArgomento && d.argomento !== filterArgomento) return false;
        if (filterDifficolta && d.difficolta !== filterDifficolta) return false;
        return true;
    });

    renderBancoDomande(filtrate);
}

// Renderizza banco domande
function renderBancoDomande(domande) {
    const container = document.getElementById('banco-domande-list');

    if (domande.length === 0) {
        container.innerHTML = '<p style="color: #999; text-align: center;">Nessuna domanda disponibile</p>';
        return;
    }

    container.innerHTML = domande.map(d => {
        const testoPreview = d.testo.length > 80 ? d.testo.substring(0, 80) + '...' : d.testo;
        const difficoltaClass = `difficolta-${d.difficolta}`;

        return `
            <div class="domanda-item" onclick="aggiungiDomanda(${d.id})">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <span class="difficolta-badge ${difficoltaClass}">${d.difficolta}</span>
                        <span style="color: #666; font-size: 0.85rem;"> - ${d.tipo}</span>
                        <div class="domanda-preview">${testoPreview}</div>
                        <div class="domanda-meta">
                            Argomento: ${d.argomento || '-'} | Punteggio default: ${d.punteggio_default}
                        </div>
                    </div>
                    <button class="btn-add" onclick="event.stopPropagation(); aggiungiDomanda(${d.id})">+ Aggiungi</button>
                </div>
            </div>
        `;
    }).join('');
}

// Aggiungi domanda alla verifica
function aggiungiDomanda(domandaId) {
    const domanda = bancoDomande.find(d => d.id === domandaId);
    if (!domanda) return;

    // Aggiungi con ordine e punteggio default
    domandeSelezionate.push({
        ...domanda,
        ordine: domandeSelezionate.length + 1,
        punteggio: domanda.punteggio_default
    });

    updateDomandeSelezionateView();
    filterBancoDomande(); // Rimuovi dalla lista disponibili
}

// Rimuovi domanda dalla verifica
function rimuoviDomanda(domandaId) {
    domandeSelezionate = domandeSelezionate.filter(d => d.id !== domandaId);

    // Ricalcola ordini
    domandeSelezionate.forEach((d, idx) => {
        d.ordine = idx + 1;
    });

    updateDomandeSelezionateView();
    filterBancoDomande(); // Aggiungi alla lista disponibili
}

// Sposta domanda su
function spostaDomandaSu(index) {
    if (index === 0) return;

    [domandeSelezionate[index], domandeSelezionate[index - 1]] =
    [domandeSelezionate[index - 1], domandeSelezionate[index]];

    // Ricalcola ordini
    domandeSelezionate.forEach((d, idx) => {
        d.ordine = idx + 1;
    });

    updateDomandeSelezionateView();
}

// Sposta domanda giù
function spostaDomandaGiu(index) {
    if (index === domandeSelezionate.length - 1) return;

    [domandeSelezionate[index], domandeSelezionate[index + 1]] =
    [domandeSelezionate[index + 1], domandeSelezionate[index]];

    // Ricalcola ordini
    domandeSelezionate.forEach((d, idx) => {
        d.ordine = idx + 1;
    });

    updateDomandeSelezionateView();
}

// Aggiorna punteggio domanda
function aggiornaPunteggio(index, value) {
    const punteggio = parseFloat(value);
    if (!isNaN(punteggio) && punteggio >= 0) {
        domandeSelezionate[index].punteggio = punteggio;
        updatePunteggioTotale();
    }
}

// Aggiorna vista domande selezionate
function updateDomandeSelezionateView() {
    const container = document.getElementById('domande-selezionate-list');
    const countSpan = document.getElementById('domande-count');

    countSpan.textContent = domandeSelezionate.length;

    if (domandeSelezionate.length === 0) {
        container.innerHTML = '<p style="color: #999; text-align: center; padding: 2rem;">Nessuna domanda selezionata</p>';
        updatePunteggioTotale();
        return;
    }

    container.innerHTML = domandeSelezionate.map((d, idx) => {
        const testoPreview = d.testo.length > 80 ? d.testo.substring(0, 80) + '...' : d.testo;
        const difficoltaClass = `difficolta-${d.difficolta}`;
        const isFirst = idx === 0;
        const isLast = idx === domandeSelezionate.length - 1;

        return `
            <div class="domanda-item-selected">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                    <div style="flex: 1;">
                        <span class="domanda-handle">☰</span>
                        <strong>${d.ordine}.</strong>
                        <span class="difficolta-badge ${difficoltaClass}">${d.difficolta}</span>
                        <span style="color: #666; font-size: 0.85rem;"> - ${d.tipo}</span>
                        <div class="domanda-preview">${testoPreview}</div>
                        <div class="domanda-meta">Argomento: ${d.argomento || '-'}</div>
                    </div>
                    <div style="text-align: right; min-width: 120px;">
                        <label style="font-size: 0.85rem; color: #666;">Punti:</label>
                        <input type="number" class="punteggio-input"
                               value="${d.punteggio}"
                               min="0"
                               step="0.25"
                               onchange="aggiornaPunteggio(${idx}, this.value)">
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
                    <button class="btn btn-sm btn-secondary"
                            onclick="spostaDomandaSu(${idx})"
                            ${isFirst ? 'disabled' : ''}>↑</button>
                    <button class="btn btn-sm btn-secondary"
                            onclick="spostaDomandaGiu(${idx})"
                            ${isLast ? 'disabled' : ''}>↓</button>
                    <button class="btn-remove" onclick="rimuoviDomanda(${d.id})">✕ Rimuovi</button>
                </div>
            </div>
        `;
    }).join('');

    updatePunteggioTotale();
}

// Aggiorna punteggio totale
function updatePunteggioTotale() {
    const totale = domandeSelezionate.reduce((sum, d) => sum + (d.punteggio || 0), 0);
    document.getElementById('punteggio-totale').textContent = totale.toFixed(2);
}

// Salva verifica
async function saveVerifica(event) {
    event.preventDefault();

    if (domandeSelezionate.length === 0) {
        showNotification('Aggiungi almeno una domanda alla verifica', 'error');
        return;
    }

    const id = document.getElementById('verificaId').value;

    const data = {
        titolo: document.getElementById('titolo').value,
        classe_id: parseInt(document.getElementById('classe_id').value),
        materia_id: parseInt(document.getElementById('materia_id').value),
        argomento: document.getElementById('argomento').value,
        data_somministrazione: document.getElementById('data_somministrazione').value || null,
        durata_minuti: parseInt(document.getElementById('durata_minuti').value) || null,
        num_versioni: parseInt(document.getElementById('num_versioni').value) || 1,
        mescola_domande: document.getElementById('mescola_domande').checked,
        istruzioni: document.getElementById('istruzioni').value,
        stato: document.getElementById('stato').value,
        domande: domandeSelezionate.map(d => ({
            domanda_id: d.id,
            ordine: d.ordine,
            punteggio: d.punteggio
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
            showNotification(id ? 'Verifica aggiornata con successo' : 'Verifica creata con successo');
            closeModal();
            loadVerifiche();
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        handleApiError(error);
    }
}

// Elimina verifica
async function deleteVerifica(id) {
    if (!confirmDelete('Sei sicuro di voler eliminare questa verifica? I voti associati non saranno eliminati.')) {
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

// Chiudi modal
function closeModal() {
    document.getElementById('verificaModal').classList.remove('show');
}

// Chiudi modal dettaglio
function closeDettaglioModal() {
    document.getElementById('dettaglioModal').classList.remove('show');
}

// Carica dati all'avvio
Promise.all([loadClassi(), loadMaterie(), loadVerifiche()]);
