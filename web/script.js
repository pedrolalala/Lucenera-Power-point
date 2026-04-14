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
const loadingMessage = document.getElementById('loadingMessage');

// Elementos das abas
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

let selectedFile = null;
let currentTab = 'xml'; // Aba padrão é XML

// ===== SISTEMA DE ABAS =====
tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabId = button.dataset.tab;
        switchTab(tabId);
    });
});

function switchTab(tabId) {
    currentTab = tabId;
    
    // Atualizar botões das abas
    tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    
    // Atualizar conteúdo das abas
    tabContents.forEach(content => {
        content.classList.toggle('active', content.id === `tab-${tabId}`);
    });
    
    // Reset do arquivo quando troca aba
    removeFile();
    
    console.log(`Aba ativa: ${tabId}`);
}

// ===== DRAG & DROP =====
// Click na drop zone abre seletor de arquivo
dropZone.addEventListener('click', () => {
    if (currentTab === 'xml') {
        fileInput.click();
    }
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
    
    if (files.length > 0 && currentTab === 'xml') {
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
    // Validar tipo baseado na aba ativa
    if (currentTab === 'xml') {
        // Validar XML
        if (!file.name.toLowerCase().endsWith('.xml')) {
            showFeedback('error', 'Por favor, selecione apenas arquivos XML.');
            return;
        }
        
        // Atualizar mensagem de loading
        loadingMessage.textContent = 'Processando XML com SharePoint...';
    } else if (currentTab === 'pdf') {
        // Sistema PDF desabilitado
        showFeedback('error', 'Sistema PDF está temporariamente desabilitado. Use XML.');
        return;
    }

    // Validar tamanho (10MB)
    const maxSize = 10 * 1024 * 1024;
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
    
    console.log(`Arquivo ${currentTab.toUpperCase()} selecionado:`, file.name);
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

    // Verificar se sistema está habilitado
    if (currentTab === 'pdf') {
        showFeedback('error', 'Sistema PDF está desabilitado. Use XML.');
        return;
    }

    // Mostrar loading com mensagem específica
    loading.style.display = 'block';
    processBtn.disabled = true;
    feedback.style.display = 'none';

    if (currentTab === 'xml') {
        loadingMessage.textContent = 'Conectando ao SharePoint...';
    }

    // Criar FormData com campo apropriado
    const formData = new FormData();
    
    if (currentTab === 'xml') {
        formData.append('xml_file', selectedFile);
    } else {
        formData.append('pdf_file', selectedFile);
    }

    try {
        // Enviar para o servidor
        const response = await fetch('/processar', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success && result.job_id) {
            // Mensagem específica do sistema
            const systemType = result.file_type || currentTab;
            
            // Redirecionar para página de status
            const redirectUrl = `/status.html?job=${result.job_id}&filename=${encodeURIComponent(selectedFile.name)}&type=${systemType}`;
            window.location.href = redirectUrl;
        } else {
            loading.style.display = 'none';
            showFeedback('error', result.error || 'Erro ao processar orçamento. Tente novamente.');
            processBtn.disabled = false;
        }

    } catch (error) {
        loading.style.display = 'none';
        
        let errorMessage = 'Erro de conexão com o servidor.';
        if (currentTab === 'xml') {
            errorMessage += ' Verifique conectividade com SharePoint.';
        }
        
        showFeedback('error', errorMessage);
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
