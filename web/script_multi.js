// Elementos DOM - XML
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileListContainer = document.getElementById('fileListContainer');
const fileList = document.getElementById('fileList');
const fileCount = document.getElementById('fileCount');
const clearAllBtn = document.getElementById('clearAllBtn');
const processBtn = document.getElementById('processBtn');

// Elementos DOM - PDF
const dropZonePdf = document.getElementById('dropZonePdf');
const fileInputPdf = document.getElementById('fileInputPdf');
const fileListContainerPdf = document.getElementById('fileListContainerPdf');
const fileListPdf = document.getElementById('fileListPdf');
const fileCountPdf = document.getElementById('fileCountPdf');
const clearAllBtnPdf = document.getElementById('clearAllBtnPdf');
const processBtnPdf = document.getElementById('processBtnPdf');

// Elementos comuns
const feedback = document.getElementById('feedback');
const feedbackMessage = document.getElementById('feedbackMessage');
const progressSection = document.getElementById('progressSection');
const jobsContainer = document.getElementById('jobsContainer');

// Elementos das abas
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

// Armazenar arquivos selecionados
let selectedFilesXml = [];
let selectedFilesPdf = [];
let currentTab = 'xml';
let activeJobs = {};

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
    console.log('Aba ativa: ' + tabId);
}

// ==================== XML UPLOAD ====================

// Drag & Drop - XML
dropZone.addEventListener('click', () => fileInput.click());

// Prevent defaults
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

// Handle drop - XML
dropZone.addEventListener('drop', (e) => {
    const files = Array.from(e.dataTransfer.files);
    handleFilesXml(files);
}, false);

// Handle file selection - XML
fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    handleFilesXml(files);
});

// Handle multiple files - XML
function handleFilesXml(files) {
    const validFiles = files.filter(file => {
        if (!file.name.toLowerCase().endsWith('.xml')) {
            showFeedback('error', `${file.name}: Apenas arquivos XML são aceitos.`);
            return false;
        }
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            showFeedback('error', `${file.name}: Arquivo muito grande (máx. 10MB).`);
            return false;
        }
        return true;
    });

    if (validFiles.length === 0) return;

    // Adicionar arquivos válidos
    validFiles.forEach(file => {
        // Evitar duplicatas
        if (!selectedFilesXml.some(f => f.name === file.name && f.size === file.size)) {
            selectedFilesXml.push(file);
        }
    });

    updateFileListXml();
    feedback.style.display = 'none';
}

// Atualizar lista de arquivos - XML
function updateFileListXml() {
    fileList.innerHTML = '';
    fileCount.textContent = selectedFilesXml.length;

    if (selectedFilesXml.length === 0) {
        fileListContainer.style.display = 'none';
        processBtn.disabled = true;
        return;
    }

    fileListContainer.style.display = 'block';
    processBtn.disabled = false;

    selectedFilesXml.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <i class="fas fa-code file-item-icon"></i>
            <div class="file-item-info">
                <div class="file-item-name">${file.name}</div>
                <div class="file-item-size">${formatFileSize(file.size)}</div>
            </div>
            <button class="file-item-remove" data-index="${index}">
                <i class="fas fa-times"></i>
            </button>
        `;

        const removeBtn = fileItem.querySelector('.file-item-remove');
        removeBtn.addEventListener('click', () => removeFileXml(index));

        fileList.appendChild(fileItem);
    });
}

// Remover arquivo individual - XML
function removeFileXml(index) {
    selectedFilesXml.splice(index, 1);
    updateFileListXml();
}

// Limpar todos os arquivos - XML
clearAllBtn.addEventListener('click', () => {
    selectedFilesXml = [];
    fileInput.value = '';
    updateFileListXml();
});

// ==================== PDF UPLOAD ====================

// Drag & Drop - PDF
dropZonePdf.addEventListener('click', () => fileInputPdf.click());

// Handle drop - PDF
dropZonePdf.addEventListener('drop', (e) => {
    const files = Array.from(e.dataTransfer.files);
    handleFilesPdf(files);
}, false);

// Handle file selection - PDF
fileInputPdf.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    handleFilesPdf(files);
});

// Handle multiple files - PDF
function handleFilesPdf(files) {
    const validFiles = files.filter(file => {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showFeedback('error', `${file.name}: Apenas arquivos PDF são aceitos.`);
            return false;
        }
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            showFeedback('error', `${file.name}: Arquivo muito grande (máx. 10MB).`);
            return false;
        }
        return true;
    });

    if (validFiles.length === 0) return;

    validFiles.forEach(file => {
        if (!selectedFilesPdf.some(f => f.name === file.name && f.size === file.size)) {
            selectedFilesPdf.push(file);
        }
    });

    updateFileListPdf();
    feedback.style.display = 'none';
}

// Atualizar lista de arquivos - PDF
function updateFileListPdf() {
    fileListPdf.innerHTML = '';
    fileCountPdf.textContent = selectedFilesPdf.length;

    if (selectedFilesPdf.length === 0) {
        fileListContainerPdf.style.display = 'none';
        processBtnPdf.disabled = true;
        return;
    }

    fileListContainerPdf.style.display = 'block';
    processBtnPdf.disabled = false;

    selectedFilesPdf.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <i class="fas fa-file-pdf file-item-icon"></i>
            <div class="file-item-info">
                <div class="file-item-name">${file.name}</div>
                <div class="file-item-size">${formatFileSize(file.size)}</div>
            </div>
            <button class="file-item-remove" data-index="${index}">
                <i class="fas fa-times"></i>
            </button>
        `;

        const removeBtn = fileItem.querySelector('.file-item-remove');
        removeBtn.addEventListener('click', () => removeFilePdf(index));

        fileListPdf.appendChild(fileItem);
    });
}

// Remover arquivo individual - PDF
function removeFilePdf(index) {
    selectedFilesPdf.splice(index, 1);
    updateFileListPdf();
}

// Limpar todos os arquivos - PDF
clearAllBtnPdf.addEventListener('click', () => {
    selectedFilesPdf = [];
    fileInputPdf.value = '';
    updateFileListPdf();
});

// ==================== PROCESSING ====================

// Processar arquivos
processBtn.addEventListener('click', async () => {
    if (selectedFilesXml.length === 0) return;
    await processMultipleFiles(selectedFilesXml, 'xml');
});

processBtnPdf.addEventListener('click', async () => {
    if (selectedFilesPdf.length === 0) return;
    await processMultipleFiles(selectedFilesPdf, 'pdf');
});

// Processar múltiplos arquivos
async function processMultipleFiles(files, fileType) {
    // Desabilitar botões
    processBtn.disabled = true;
    processBtnPdf.disabled = true;

    // Mostrar seção de progresso
    progressSection.style.display = 'block';
    jobsContainer.innerHTML = '';

    // Processar cada arquivo
    for (const file of files) {
        const jobId = await uploadAndProcessFile(file, fileType);
        if (jobId) {
            createJobItem(jobId, file.name);
            pollJobStatus(jobId);
        }
    }

    // Limpar lista de arquivos após iniciar processamento
    if (fileType === 'xml') {
        selectedFilesXml = [];
        fileInput.value = '';
        updateFileListXml();
    } else {
        selectedFilesPdf = [];
        fileInputPdf.value = '';
        updateFileListPdf();
    }

    // Reabilitar botões
    processBtn.disabled = false;
    processBtnPdf.disabled = false;
}

// Upload e processar arquivo individual
async function uploadAndProcessFile(file, fileType) {
    const formData = new FormData();
    if (fileType === 'xml') {
        formData.append('xml_file', file);
    } else {
        formData.append('pdf_file', file);
    }

    try {
        const response = await fetch('/processar', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success && result.job_id) {
            return result.job_id;
        } else {
            showFeedback('error', `${file.name}: ${result.error || 'Erro ao processar'}`);
            return null;
        }
    } catch (error) {
        showFeedback('error', `${file.name}: Erro de conexão - ${error.message}`);
        return null;
    }
}

// Criar item de job na UI
function createJobItem(jobId, fileName) {
    const jobItem = document.createElement('div');
    jobItem.className = 'job-item';
    jobItem.id = `job-${jobId}`;
    jobItem.innerHTML = `
        <div class="job-header">
            <div class="job-name">${fileName}</div>
            <div class="job-status processing">⏳ Processando...</div>
        </div>
        <div class="job-progress-bar">
            <div class="job-progress-fill" style="width: 0%"></div>
        </div>
        <div class="job-message" style="font-size: 12px; color: #64748b;"></div>
    `;

    jobsContainer.appendChild(jobItem);
    activeJobs[jobId] = { fileName, element: jobItem };
}

// Polling do status do job
function pollJobStatus(jobId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/status/${jobId}`);
            const data = await response.json();

            if (!response.ok || !activeJobs[jobId]) {
                clearInterval(interval);
                return;
            }

            updateJobUI(jobId, data);

            // Parar polling se job terminou
            if (data.status === 'completed' || data.status === 'error') {
                clearInterval(interval);
            }
        } catch (error) {
            console.error(`Erro ao verificar status do job ${jobId}:`, error);
        }
    }, 2000); // Poll a cada 2 segundos
}

// Atualizar UI do job
function updateJobUI(jobId, data) {
    const job = activeJobs[jobId];
    if (!job) return;

    const jobElement = job.element;
    const progressFill = jobElement.querySelector('.job-progress-fill');
    const statusBadge = jobElement.querySelector('.job-status');
    const messageEl = jobElement.querySelector('.job-message');

    // Atualizar progresso
    progressFill.style.width = `${data.progress || 0}%`;

    // Atualizar status
    if (data.status === 'completed' && data.ppt_path) {
        statusBadge.className = 'job-status success';
        statusBadge.textContent = '✅ Concluído';
        
        const fileName = data.ppt_path.split('\\').pop().split('/').pop();
        jobElement.querySelector('.job-message').innerHTML = `
            <a href="/download_file/${fileName}" class="job-download">
                <i class="fas fa-download"></i> Baixar PowerPoint
            </a>
        `;
    } else if (data.status === 'error') {
        statusBadge.className = 'job-status error';
        statusBadge.textContent = '❌ Erro';
        messageEl.textContent = data.error || 'Erro desconhecido';
    } else {
        statusBadge.textContent = `⏳ ${data.status}...`;
    }
}

// ==================== UTILITIES ====================

// Formatar tamanho de arquivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Mostrar feedback
function showFeedback(type, message) {
    if (feedback) {
        feedback.style.display = 'block';
        feedback.className = 'feedback ' + (type === 'error' ? 'feedback-error' : 'feedback-success');
        feedbackMessage.textContent = message;
        
        setTimeout(() => {
            feedback.style.display = 'none';
        }, 5000);
    }
}
