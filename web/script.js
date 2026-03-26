// Elementos DOM
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeBtn = document.getElementById('removeBtn');
const processBtn = document.getElementById('processBtn');
const feedback = document.getElementById('feedback');
const feedbackMessage = document.getElementById('feedbackMessage');
const loading = document.getElementById('loading');

let selectedFile = null;

// Click na drop zone abre seletor de arquivo
dropZone.addEventListener('click', () => {
    fileInput.click();
});

// Prevenir comportamento padrão do drag
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight na drop zone
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropZone.classList.add('drag-over');
}

function unhighlight() {
    dropZone.classList.remove('drag-over');
}

// Handle drop
dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// Handle file selection
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Processar arquivo selecionado
function handleFile(file) {
    // Validar tipo de arquivo
    if (file.type !== 'application/pdf') {
        showFeedback('error', 'Por favor, selecione apenas arquivos PDF.');
        return;
    }

    // Validar tamanho (10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB em bytes
    if (file.size > maxSize) {
        showFeedback('error', 'O arquivo é muito grande. Tamanho máximo: 10MB.');
        return;
    }

    // Salvar arquivo selecionado
    selectedFile = file;

    // Mostrar informações do arquivo
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    fileInfo.style.display = 'block';
    processBtn.disabled = false;
    
    // Ocultar feedback anterior
    feedback.style.display = 'none';
}

// Formatar tamanho do arquivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Remover arquivo
removeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    removeFile();
});

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    processBtn.disabled = true;
    feedback.style.display = 'none';
}

// Processar orçamento
processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Mostrar loading
    loading.style.display = 'block';
    processBtn.disabled = true;
    feedback.style.display = 'none';

    // Criar FormData
    const formData = new FormData();
    formData.append('pdf_file', selectedFile);

    try {
        // Enviar para o servidor
        const response = await fetch('/processar', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success && result.job_id) {
            // Redirecionar para página de status
            window.location.href = `/status.html?job=${result.job_id}&filename=${encodeURIComponent(selectedFile.name)}`;
        } else {
            loading.style.display = 'none';
            showFeedback('error', result.error || 'Erro ao processar orçamento. Tente novamente.');
            processBtn.disabled = false;
        }
    } catch (error) {
        loading.style.display = 'none';
        showFeedback('error', 'Erro de conexão com o servidor. Verifique se o servidor está rodando.');
        processBtn.disabled = false;
        console.error('Erro:', error);
    }
});

// Mostrar feedback
function showFeedback(type, message) {
    feedback.className = 'feedback ' + type;
    feedbackMessage.textContent = message;
    feedback.style.display = 'flex';

    // Atualizar ícone
    const icon = feedback.querySelector('.feedback-icon');
    if (type === 'success') {
        icon.className = 'fas fa-check-circle feedback-icon';
    } else {
        icon.className = 'fas fa-exclamation-circle feedback-icon';
    }
}
