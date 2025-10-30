// Variabili globali
let classi = [];
let currentClasseId = null;

// Carica le classi al caricamento della pagina
document.addEventListener('DOMContentLoaded', () => {
    loadClassi();
    setupAutoNomeGeneration();
});

// Carica tutte le classi
async function loadClassi() {
    try {
        const response = await fetch('/api/classi');
        if (!response.ok) throw new Error('Errore nel caricamento delle classi');

        classi = await response.json();
        renderClassi();
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nel caricamento delle classi', 'error');
    }
}

// Renderizza le classi nella griglia
function renderClassi() {
    const container = document.getElementById('classi-container');

    if (classi.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>Nessuna classe presente</p>
                <p>Clicca su "Aggiungi Classe" per iniziare</p>
            </div>
        `;
        return;
    }

    container.innerHTML = classi.map(classe => `
        <div class="classe-card">
            <div class="classe-header">
                <h3>${classe.nome}</h3>
                <span class="badge">${classe.num_studenti} studenti</span>
            </div>
            <div class="classe-info">
                <p><strong>Anno:</strong> ${classe.anno}°</p>
                <p><strong>Sezione:</strong> ${classe.sezione}</p>
                ${classe.indirizzo ? `<p><strong>Indirizzo:</strong> ${classe.indirizzo}</p>` : ''}
                <p><strong>A.S.:</strong> ${classe.anno_scolastico}</p>
                ${classe.note ? `<p class="note">${classe.note}</p>` : ''}
            </div>
            <div class="classe-actions">
                <button onclick="viewStudenti(${classe.id})" class="btn btn-sm btn-info">
                    Studenti
                </button>
                <button onclick="editClasse(${classe.id})" class="btn btn-sm btn-primary">
                    Modifica
                </button>
                <button onclick="deleteClasse(${classe.id})" class="btn btn-sm btn-danger">
                    Elimina
                </button>
            </div>
        </div>
    `).join('');
}

// Apre il modal per creare una nuova classe
function openModal() {
    currentClasseId = null;
    document.getElementById('modalTitle').textContent = 'Aggiungi Classe';
    document.getElementById('classeForm').reset();
    document.getElementById('classe-id').value = '';
    document.getElementById('classeModal').style.display = 'block';

    // Imposta anno scolastico corrente
    const now = new Date();
    const year = now.getFullYear();
    const nextYear = year + 1;
    const annoScolastico = `${year}/${nextYear}`;
    document.getElementById('anno-scolastico').value = annoScolastico;
}

// Chiude il modal
function closeModal() {
    document.getElementById('classeModal').style.display = 'none';
}

// Modifica una classe esistente
async function editClasse(classeId) {
    try {
        const response = await fetch(`/api/classi/${classeId}`);
        if (!response.ok) throw new Error('Errore nel caricamento della classe');

        const classe = await response.json();
        currentClasseId = classeId;

        document.getElementById('modalTitle').textContent = 'Modifica Classe';
        document.getElementById('classe-id').value = classe.id;
        document.getElementById('anno').value = classe.anno;
        document.getElementById('sezione').value = classe.sezione;
        document.getElementById('indirizzo').value = classe.indirizzo || '';
        document.getElementById('nome').value = classe.nome;
        document.getElementById('anno-scolastico').value = classe.anno_scolastico;
        document.getElementById('note').value = classe.note || '';

        document.getElementById('classeModal').style.display = 'block';
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nel caricamento della classe', 'error');
    }
}

// Elimina una classe
async function deleteClasse(classeId) {
    const classe = classi.find(c => c.id === classeId);

    if (classe.num_studenti > 0) {
        if (!confirm(`Attenzione! La classe "${classe.nome}" ha ${classe.num_studenti} studenti.\nSe elimini la classe, anche gli studenti verranno eliminati.\n\nSei sicuro di voler continuare?`)) {
            return;
        }
    } else {
        if (!confirm(`Sei sicuro di voler eliminare la classe "${classe.nome}"?`)) {
            return;
        }
    }

    try {
        const response = await fetch(`/api/classi/${classeId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Errore nell\'eliminazione della classe');

        showNotification('Classe eliminata con successo', 'success');
        loadClassi();
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nell\'eliminazione della classe', 'error');
    }
}

// Gestisce il submit del form
document.getElementById('classeForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const classeData = {
        nome: document.getElementById('nome').value,
        anno: parseInt(document.getElementById('anno').value),
        sezione: document.getElementById('sezione').value,
        indirizzo: document.getElementById('indirizzo').value,
        anno_scolastico: document.getElementById('anno-scolastico').value,
        note: document.getElementById('note').value
    };

    try {
        const url = currentClasseId ? `/api/classi/${currentClasseId}` : '/api/classi';
        const method = currentClasseId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(classeData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Errore nel salvataggio');
        }

        showNotification(
            currentClasseId ? 'Classe aggiornata con successo' : 'Classe creata con successo',
            'success'
        );

        closeModal();
        loadClassi();
    } catch (error) {
        console.error('Errore:', error);
        showNotification(error.message, 'error');
    }
});

// Setup generazione automatica del nome classe
function setupAutoNomeGeneration() {
    const annoSelect = document.getElementById('anno');
    const sezioneInput = document.getElementById('sezione');
    const indirizzoSelect = document.getElementById('indirizzo');
    const nomeInput = document.getElementById('nome');

    function updateNome() {
        const anno = annoSelect.value;
        const sezione = sezioneInput.value.trim().toUpperCase();
        const indirizzo = indirizzoSelect.value;

        if (anno && sezione) {
            const nomeGenerato = indirizzo ?
                `${anno}${sezione} ${indirizzo}` :
                `${anno}${sezione}`;
            nomeInput.value = nomeGenerato;
        }
    }

    annoSelect.addEventListener('change', updateNome);
    sezioneInput.addEventListener('input', updateNome);
    indirizzoSelect.addEventListener('change', updateNome);
}

// Visualizza gli studenti di una classe
async function viewStudenti(classeId) {
    try {
        const [classeResponse, studentiResponse] = await Promise.all([
            fetch(`/api/classi/${classeId}`),
            fetch(`/api/classi/${classeId}/studenti`)
        ]);

        if (!classeResponse.ok || !studentiResponse.ok) {
            throw new Error('Errore nel caricamento dei dati');
        }

        const classe = await classeResponse.json();
        const studenti = await studentiResponse.json();

        document.getElementById('studentiModalTitle').textContent =
            `Studenti di ${classe.nome} (${studenti.length})`;

        const studentiList = document.getElementById('studenti-list');

        if (studenti.length === 0) {
            studentiList.innerHTML = `
                <div class="empty-state">
                    <p>Nessuno studente in questa classe</p>
                    <p><a href="/studenti">Vai alla pagina Studenti per aggiungerne</a></p>
                </div>
            `;
        } else {
            studentiList.innerHTML = `
                <table class="studenti-table">
                    <thead>
                        <tr>
                            <th>Cognome</th>
                            <th>Nome</th>
                            <th>Data Nascita</th>
                            <th>Email</th>
                            <th>Telefono</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${studenti.map(s => `
                            <tr>
                                <td>${s.cognome}</td>
                                <td>${s.nome}</td>
                                <td>${s.data_nascita || '-'}</td>
                                <td>${s.email || '-'}</td>
                                <td>${s.telefono || '-'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        }

        document.getElementById('studentiModal').style.display = 'block';
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nel caricamento degli studenti', 'error');
    }
}

// Chiude il modal studenti
function closeStudentiModal() {
    document.getElementById('studentiModal').style.display = 'none';
}

// Chiude i modal quando si clicca fuori
window.onclick = function(event) {
    const classeModal = document.getElementById('classeModal');
    const studentiModal = document.getElementById('studentiModal');

    if (event.target === classeModal) {
        closeModal();
    }
    if (event.target === studentiModal) {
        closeStudentiModal();
    }
}

// Mostra notifiche
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
