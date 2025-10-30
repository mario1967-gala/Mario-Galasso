// Gestione import studenti da screenshot

let extractedStudents = [];
let selectedFile = null;

// Switch tra le tab
function switchTab(tabName) {
    // Nascondi tutte le tab
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Mostra la tab selezionata
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');

    // Reset
    resetImport();
}

// Gestione selezione file
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    selectedFile = file;

    // Mostra anteprima
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('image-preview').src = e.target.result;
        document.getElementById('preview-section').style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Drag & Drop support
const uploadArea = document.getElementById('upload-area');

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            selectedFile = file;
            document.getElementById('screenshot-input').files = files;

            // Mostra anteprima
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('image-preview').src = e.target.result;
                document.getElementById('preview-section').style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            showNotification('Per favore carica un file immagine', 'error');
        }
    }
});

// Toggle visibilità API key
function toggleApiKeyVisibility() {
    const apiKeyInput = document.getElementById('api-key-input');
    if (apiKeyInput.type === 'password') {
        apiKeyInput.type = 'text';
    } else {
        apiKeyInput.type = 'password';
    }
}

// Upload screenshot e estrai dati con Claude AI Vision
async function uploadScreenshot() {
    if (!selectedFile) {
        showNotification('Seleziona prima un\'immagine', 'error');
        return;
    }

    // Ottieni API key
    const apiKey = document.getElementById('api-key-input').value.trim();

    if (!apiKey) {
        showNotification('Inserisci la chiave API di Anthropic per usare Claude AI Vision', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('screenshot', selectedFile);
    formData.append('api_key', apiKey);

    try {
        showNotification('🤖 Claude AI sta analizzando l\'immagine...', 'info');

        const response = await fetch('/api/studenti/upload-screenshot', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            extractedStudents = result.students;
            displayExtractedStudents(extractedStudents);
            showNotification(result.message || `Estratti ${result.count} studenti dall'immagine`, 'success');
        } else {
            if (result.ocr_error) {
                // Se l'errore è dovuto all'OCR mancante, mostra un messaggio specifico
                showNotification('OCR non disponibile. Usa la modalità "Incolla Testo" invece.', 'warning');
            } else {
                showNotification('Errore: ' + result.error, 'error');
            }
        }
    } catch (error) {
        showNotification('Errore nella comunicazione con il server', 'error');
        console.error(error);
    }
}

// Parse testo incollato
async function parseText() {
    const text = document.getElementById('text-input').value.trim();

    if (!text) {
        showNotification('Inserisci il testo da analizzare', 'error');
        return;
    }

    try {
        const response = await fetch('/api/studenti/parse-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const result = await response.json();

        if (result.success) {
            extractedStudents = result.students;
            displayExtractedStudents(extractedStudents);
            showNotification(`Estratti ${result.count} studenti dal testo`, 'success');
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Errore nella comunicazione con il server', 'error');
        console.error(error);
    }
}

// Visualizza gli studenti estratti in una tabella
function displayExtractedStudents(students) {
    if (students.length === 0) {
        showNotification('Nessuno studente trovato', 'warning');
        return;
    }

    const tbody = document.getElementById('students-table');
    tbody.innerHTML = students.map((student, index) => `
        <tr data-index="${index}">
            <td>
                <input type="checkbox" class="student-checkbox" checked>
            </td>
            <td class="editable-cell">
                <input type="text" value="${student.cognome || ''}"
                    onchange="updateStudent(${index}, 'cognome', this.value)">
            </td>
            <td class="editable-cell">
                <input type="text" value="${student.nome || ''}"
                    onchange="updateStudent(${index}, 'nome', this.value)">
            </td>
            <td class="editable-cell">
                <input type="date" value="${student.data_nascita || ''}"
                    onchange="updateStudent(${index}, 'data_nascita', this.value)">
            </td>
            <td class="editable-cell">
                <input type="email" value="${student.email || ''}"
                    onchange="updateStudent(${index}, 'email', this.value)">
            </td>
            <td class="editable-cell">
                <input type="tel" value="${student.telefono || ''}"
                    onchange="updateStudent(${index}, 'telefono', this.value)">
            </td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="removeStudent(${index})">
                    Rimuovi
                </button>
            </td>
        </tr>
    `).join('');

    document.getElementById('students-count').textContent =
        `Trovati ${students.length} studenti. Verifica i dati e modifica se necessario:`;
    document.getElementById('results-section').style.display = 'block';

    // Scroll alla sezione risultati
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth' });
}

// Aggiorna dati studente
function updateStudent(index, field, value) {
    extractedStudents[index][field] = value;
}

// Rimuovi studente dalla lista
function removeStudent(index) {
    extractedStudents.splice(index, 1);
    displayExtractedStudents(extractedStudents);
}

// Seleziona/deseleziona tutti
function toggleSelectAll(checkbox) {
    document.querySelectorAll('.student-checkbox').forEach(cb => {
        cb.checked = checkbox.checked;
    });
}

// Importa studenti selezionati
async function importSelectedStudents() {
    const checkboxes = document.querySelectorAll('.student-checkbox');
    const selectedStudents = [];

    checkboxes.forEach((checkbox, index) => {
        if (checkbox.checked) {
            selectedStudents.push(extractedStudents[index]);
        }
    });

    if (selectedStudents.length === 0) {
        showNotification('Seleziona almeno uno studente da importare', 'error');
        return;
    }

    // Valida dati obbligatori
    const invalid = selectedStudents.filter(s => !s.nome || !s.cognome);
    if (invalid.length > 0) {
        showNotification('Alcuni studenti non hanno nome o cognome', 'error');
        return;
    }

    if (!confirm(`Importare ${selectedStudents.length} studenti?`)) {
        return;
    }

    try {
        const response = await fetch('/api/studenti/batch-import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ students: selectedStudents })
        });

        const result = await response.json();

        if (result.success) {
            showNotification(`Importati ${result.imported} studenti con successo!`, 'success');

            if (result.errors.length > 0) {
                console.log('Errori durante import:', result.errors);
                showNotification(`${result.errors.length} errori. Controlla la console.`, 'warning');
            }

            // Reindirizza alla pagina studenti dopo 2 secondi
            setTimeout(() => {
                window.location.href = '/studenti';
            }, 2000);
        } else {
            showNotification('Errore: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Errore nella comunicazione con il server', 'error');
        console.error(error);
    }
}

// Reset import
function resetImport() {
    extractedStudents = [];
    selectedFile = null;
    document.getElementById('screenshot-input').value = '';
    document.getElementById('text-input').value = '';
    document.getElementById('preview-section').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
}
