// Obter parâmetros da URL
const urlParams = new URLSearchParams(window.location.search);
const jobId = urlParams.get('job');
const filename = urlParams.get('filename');

// Elementos DOM
const fileNameDisplay = document.getElementById('fileNameDisplay');
const timestamp = document.getElementById('timestamp');
const statusIcon = document.getElementById('statusIcon');
const statusTitle = document.getElementById('statusTitle');
const statusDescription = document.getElementById('statusDescription');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusCard = document.getElementById('statusCard');
const errorCard = document.getElementById('errorCard');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const backBtn = document.getElementById('backBtn');

// Steps
const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');

let checkInterval = null;
let downloadUrl = null;

// Inicializar página
function init() {
    if (!jobId || !filename) {
        showError('Parâmetros inválidos. Retorne à página inicial.');
        return;
    }

    // Exibir nome do arquivo
    fileNameDisplay.textContent = decodeURIComponent(filename);
    
    // Exibir timestamp
    const now = new Date();
    timestamp.textContent = `Iniciado em: ${formatDateTime(now)}`;

    // Iniciar verificação de status
    checkStatus();
    checkInterval = setInterval(checkStatus, 2000); // Verifica a cada 2 segundos
}

// Verificar status do job
async function checkStatus() {
    try {
        const response = await fetch(`/status/${jobId}`);
        const data = await response.json();

        if (response.ok) {
            updateUI(data);
        } else {
            showError(data.error || 'Erro ao verificar status');
            clearInterval(checkInterval);
        }
    } catch (error) {
        console.error('Erro ao verificar status:', error);
        showError('Erro de conexão com o servidor');
        clearInterval(checkInterval);
    }
}

// Atualizar interface com status
function updateUI(data) {
    const status = data.status;
    const progress = data.progress || 0;

    // Atualizar barra de progresso
    progressFill.style.width = progress + '%';
    progressText.textContent = progress + '%';

    // Atualizar baseado no status
    switch (status) {
        case 'waiting':
            updateStatus('waiting', 'Aguardando', 'Preparando processamento...', 'fa-clock');
            break;

        case 'uploading':
            updateStatus('processing', 'Processando', 'Fazendo upload do arquivo...', 'fa-upload');
            updateSteps(1, 'ativo');
            break;

        case 'organizing':
            updateStatus('processing', 'Processando', 'Organizando arquivos...', 'fa-folder-open');
            updateSteps(1, 'concluído');
            updateSteps(2, 'ativo');
            break;

        case 'generating':
            updateStatus('processing', 'Processando', 'Gerando PowerPoint...', 'fa-file-powerpoint');
            updateSteps(2, 'concluído');
            updateSteps(3, 'ativo');
            break;

        case 'completed':
            updateStatus('success', 'Pronto!', 'PowerPoint gerado com sucesso', 'fa-check-circle');
            updateSteps(3, 'concluído');
            clearInterval(checkInterval);
            
            // Mostrar botão de download
            if (data.download_url) {
                downloadUrl = data.download_url;
                downloadBtn.style.display = 'flex';
            }
            break;

        case 'error':
            updateStatus('error', 'Erro', 'Falha no processamento', 'fa-times-circle');
            showError(data.error || 'Erro desconhecido no processamento');
            clearInterval(checkInterval);
            break;
    }
}

// Atualizar status visual
function updateStatus(type, title, description, icon) {
    // Atualizar classes do ícone
    statusIcon.className = `status-icon ${type}`;
    statusIcon.innerHTML = `<i class="fas ${icon}"></i>`;

    // Atualizar texto
    statusTitle.textContent = title;
    statusDescription.textContent = description;
}

// Atualizar etapas
function updateSteps(stepNumber, state) {
    let step, statusText;

    switch (stepNumber) {
        case 1:
            step = step1;
            statusText = step.querySelector('.step-status');
            break;
        case 2:
            step = step2;
            statusText = step.querySelector('.step-status');
            break;
        case 3:
            step = step3;
            statusText = step.querySelector('.step-status');
            break;
    }

    if (!step) return;

    // Remover classes antigas
    step.classList.remove('active', 'completed');

    if (state === 'ativo') {
        step.classList.add('active');
        statusText.textContent = 'Processando...';
    } else if (state === 'concluído') {
        step.classList.add('completed');
        statusText.textContent = 'Concluído ✓';
    }
}

// Mostrar erro
function showError(message) {
    errorCard.style.display = 'block';
    errorMessage.textContent = message;
    statusCard.style.display = 'none';
}

// Formatar data/hora
function formatDateTime(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${day}/${month}/${year} às ${hours}:${minutes}`;
}

// Event Listeners
downloadBtn.addEventListener('click', () => {
    if (downloadUrl) {
        window.location.href = downloadUrl;
    }
});

backBtn.addEventListener('click', () => {
    window.location.href = '/';
});

// Limpar interval ao sair da página
window.addEventListener('beforeunload', () => {
    if (checkInterval) {
        clearInterval(checkInterval);
    }
});

// Iniciar
init();
