// Elementos DOM - XML
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeBtn = document.getElementById('removeBtn');
const processBtn = document.getElementById('processBtn');

// Elementos DOM - PDF
const dropZonePdf = document.getElementById('dropZonePdf');
const fileInputPdf = document.getElementById('fileInputPdf');
const fileInfoPdf = document.getElementById('fileInfoPdf');
const fileNamePdf = document.getElementById('fileNamePdf');
const fileSizePdf = document.getElementById('fileSizePdf');
const removeBtnPdf = document.getElementById('removeBtnPdf');
const processBtnPdf = document.getElementById('processBtnPdf');

// Elementos comuns
const feedback = document.getElementById('feedback');
const feedbackMessage = document.getElementById('feedbackMessage');
const loading = document.getElementById('loading');
const loadingMessage = document.getElementById('loadingMessage');

// Elementos das abas
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

let selectedFile = null;
let currentTab = 'xml';

// Sistema de abas
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.dataset.tab;
        switchTab(tabId);
    });
});

function switchTab(tabId) {
    currentTab = tabId;
    tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    tabContents.forEach(content => {
        content.classList.toggle('active', content.id === 'tab-' + tabId);
    });
    removeFile('xml');
    removeFile('pdf');
    console.log('Aba ativa: ' + tabId);
}

// Drag & Drop - XML
dropZone.addEventListener('click', () => fileInput.click());

// Drag & Drop - PDF
dropZonePdf.addEventListener('click', () => fileInputPdf.click());

// Prevenir comportamento padrão
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
    dropZonePdf.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

// Highlight dropzones
['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
    dropZonePdf.addEventListener(eventName, () => dropZonePdf.classList.add('drag-over'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
    dropZonePdf.addEventListener(eventName, () => dropZonePdf.classList.remove('drag-over'), false);
});

// Handle drop
dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0], 'xml');
}, false);

dropZonePdf.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0], 'pdf');
}, false);

// Handle file selection
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0], 'xml');
});

fileInputPdf.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0], 'pdf');
});

// Processar arquivo
function handleFile(file, fileType) {
    if (fileType === 'xml') {
        if (!file.name.toLowerCase().endsWith('.xml')) {
            showFeedback('error', 'Por favor, selecione apenas arquivos XML.');
            return;
        }
        loadingMessage.textContent = 'Processando XML com SharePoint...';
        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
        processBtn.disabled = false;
    } else if (fileType === 'pdf') {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showFeedback('error', 'Por favor, selecione apenas arquivos PDF.');
            return;
        }
        loadingMessage.textContent = 'Processando PDF...';
        selectedFile = file;
        fileNamePdf.textContent = file.name;
        fileSizePdf.textContent = formatFileSize(file.size);
        fileInfoPdf.style.display = 'block';
        processBtnPdf.disabled = false;
    }

    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showFeedback('error', 'O arquivo é muito grande. Tamanho máximo: 10MB.');
        return;
    }
    
    feedback.style.display = 'none';
    console.log('Arquivo ' + fileType.toUpperCase() + ' selecionado:', file.name);
}

// Formatar tamanho
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
    removeFile('xml');
});

removeBtnPdf.addEventListener('click', (e) => {
    e.stopPropagation();
    removeFile('pdf');
});

function removeFile(fileType) {
    selectedFile = null;
    if (fileType === 'xml') {
        fileInput.value = '';
        fileInfo.style.display = 'none';
        processBtn.disabled = true;
    } else if (fileType === 'pdf') {
        fileInputPdf.value = '';
        fileInfoPdf.style.display = 'none';
        processBtnPdf.disabled = true;
    }
    feedback.style.display = 'none';
}

// Processar
processBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    await processarOrcamento('xml');
});

processBtnPdf.addEventListener('click', async () => {
    if (!selectedFile) return;
    await processarOrcamento('pdf');
});

async function processarOrcamento(fileType) {
    loading.style.display = 'block';
    
    if (fileType === 'xml') {
        processBtn.disabled = true;
        loadingMessage.textContent = 'Conectando ao SharePoint...';
    } else {
        processBtnPdf.disabled = true;
        loadingMessage.textContent = 'Extraindo produtos do PDF...';
    }
    
    feedback.style.display = 'none';

    const formData = new FormData();
    if (fileType === 'xml') {
        formData.append('xml_file', selectedFile);
    } else {
        formData.append('pdf_file', selectedFile);
    }

    try {
        const response = await fetch('/processar', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success && result.job_id) {
            const redirectUrl = '/status.html?job=' + result.job_id + '&filename=' + encodeURIComponent(selectedFile.name) + '&type=' + fileType;
            window.location.href = redirectUrl;
        } else {
            loading.style.display = 'none';
            showFeedback('error', result.error || 'Erro ao processar orçamento. Tente novamente.');
            
            if (fileType === 'xml') {
                processBtn.disabled = false;
            } else {
                processBtnPdf.disabled = false;
            }
        }

    } catch (error) {
        loading.style.display = 'none';
        
        let errorMessage = 'Erro de conexão com o servidor.';
        if (fileType === 'xml') {
            errorMessage += ' Verifique conectividade com SharePoint.';
        }
        
        showFeedback('error', errorMessage);
        
        if (fileType === 'xml') {
            processBtn.disabled = false;
        } else {
            processBtnPdf.disabled = false;
        }
        
        console.error('Erro:', error);
    }
}

// Mostrar feedback
function showFeedback(type, message) {
    feedback.className = 'feedback ' + type;
    feedbackMessage.textContent = message;
    feedback.style.display = 'flex';

    const icon = feedback.querySelector('.feedback-icon');
    if (type === 'success') {
        icon.className = 'fas fa-check-circle feedback-icon';
    } else {
        icon.className = 'fas fa-exclamation-circle feedback-icon';
    }
}
