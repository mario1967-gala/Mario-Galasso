// Gestione Report

let classi = [];
let studenti = [];
let materie = [];

// Carica dati necessari
async function loadData() {
    try {
        const [classiRes, studentiRes, materieRes] = await Promise.all([
            fetch('/api/classi'),
            fetch('/api/studenti'),
            fetch('/api/materie')
        ]);

        classi = await classiRes.json();
        studenti = await studentiRes.json();
        materie = await materieRes.json();

        populateSelects();
    } catch (error) {
        handleApiError(error);
    }
}

// Popola i select
function populateSelects() {
    // Popola select classi
    const classeSelects = ['classe-voti', 'classe-presenze', 'classe-stats'];
    classeSelects.forEach(selectId => {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Seleziona classe...</option>' +
            classi.map(c => `<option value="${c.id}">${c.nome}</option>`).join('');
    });

    // Popola select studenti
    const studenteSelect = document.getElementById('studente-pagella');
    studenteSelect.innerHTML = '<option value="">Seleziona studente...</option>' +
        studenti.map(s => `<option value="${s.id}">${s.cognome} ${s.nome} - ${s.classe_nome || 'Nessuna classe'}</option>`).join('');

    // Popola select materie
    const materiaSelect = document.getElementById('materia-voti');
    materiaSelect.innerHTML = '<option value="">Tutte le materie</option>' +
        materie.map(m => `<option value="${m.id}">${m.nome}</option>`).join('');
}

// Genera report voti
async function generateReportVoti() {
    const classeId = document.getElementById('classe-voti').value;
    const materiaId = document.getElementById('materia-voti').value;

    if (!classeId) {
        showNotification('Seleziona una classe', 'error');
        return;
    }

    try {
        showNotification('Generazione report in corso...', 'info');

        let url = `/api/report/voti/${classeId}`;
        if (materiaId) {
            url += `?materia_id=${materiaId}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Errore nella generazione del report');
        }

        // Scarica il file PDF
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;

        const classe = classi.find(c => c.id == classeId);
        const nomeFile = `report_voti_${classe.nome.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        a.download = nomeFile;

        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        showNotification('Report generato con successo!');
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nella generazione del report', 'error');
    }
}

// Genera report presenze
async function generateReportPresenze() {
    const classeId = document.getElementById('classe-presenze').value;
    const dataInizio = document.getElementById('data-inizio').value;
    const dataFine = document.getElementById('data-fine').value;

    if (!classeId) {
        showNotification('Seleziona una classe', 'error');
        return;
    }

    try {
        showNotification('Generazione report in corso...', 'info');

        let url = `/api/report/presenze/${classeId}`;
        const params = new URLSearchParams();
        if (dataInizio) params.append('data_inizio', dataInizio);
        if (dataFine) params.append('data_fine', dataFine);

        if (params.toString()) {
            url += `?${params.toString()}`;
        }

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Errore nella generazione del report');
        }

        // Scarica il file PDF
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;

        const classe = classi.find(c => c.id == classeId);
        const nomeFile = `report_presenze_${classe.nome.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        a.download = nomeFile;

        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        showNotification('Report generato con successo!');
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nella generazione del report', 'error');
    }
}

// Genera pagella studente
async function generateReportPagella() {
    const studenteId = document.getElementById('studente-pagella').value;
    const periodo = document.getElementById('periodo').value;

    if (!studenteId) {
        showNotification('Seleziona uno studente', 'error');
        return;
    }

    try {
        showNotification('Generazione pagella in corso...', 'info');

        const url = `/api/report/pagella/${studenteId}?periodo=${periodo}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Errore nella generazione della pagella');
        }

        // Scarica il file PDF
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;

        const studente = studenti.find(s => s.id == studenteId);
        const nomeFile = `pagella_${studente.cognome}_${studente.nome}_${periodo}_${new Date().toISOString().split('T')[0]}.pdf`;
        a.download = nomeFile;

        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        showNotification('Pagella generata con successo!');
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nella generazione della pagella', 'error');
    }
}

// Genera report statistiche
async function generateReportStats() {
    const classeId = document.getElementById('classe-stats').value;

    if (!classeId) {
        showNotification('Seleziona una classe', 'error');
        return;
    }

    try {
        showNotification('Generazione report statistiche in corso...', 'info');

        const url = `/api/report/statistiche/${classeId}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Errore nella generazione del report');
        }

        // Scarica il file PDF
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;

        const classe = classi.find(c => c.id == classeId);
        const nomeFile = `statistiche_${classe.nome.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`;
        a.download = nomeFile;

        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        showNotification('Report statistiche generato con successo!');
    } catch (error) {
        console.error('Errore:', error);
        showNotification('Errore nella generazione del report', 'error');
    }
}

// Carica dati all'avvio
loadData();
