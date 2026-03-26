// Elementos DOM
const loading = document.getElementById('loading');
const filesContainer = document.getElementById('filesContainer');
const filesList = document.getElementById('filesList');
const emptyState = document.getElementById('emptyState');
const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');
const btnNovo = document.getElementById('btnNovo');
const btnReload = document.getElementById('btnReload');

// Carregar arquivos ao iniciar
loadFiles();

// Event Listeners
btnNovo.addEventListener('click', () => {
    window.location.href = '/';
});

btnReload.addEventListener('click', () => {
    loadFiles();
});

// Função para carregar arquivos
async function loadFiles() {
    // Mostrar loading
    loading.style.display = 'block';
    filesContainer.style.display = 'none';
    emptyState.style.display = 'none';
    errorMessage.style.display = 'none';

    try {
        const response = await fetch('/api/listar_arquivos');
        const data = await response.json();

        loading.style.display = 'none';

        if (response.ok && data.success) {
            if (data.arquivos.length === 0) {
                // Nenhum arquivo encontrado
                emptyState.style.display = 'block';
            } else {
                // Exibir arquivos
                filesContainer.style.display = 'block';
                renderFiles(data.arquivos);
            }
        } else {
            // Erro na resposta
            errorMessage.style.display = 'block';
            errorText.textContent = data.error || 'Erro ao carregar arquivos';
        }
    } catch (error) {
        // Erro de conexão
        loading.style.display = 'none';
        errorMessage.style.display = 'block';
        errorText.textContent = 'Erro de conexão com o servidor';
        console.error('Erro:', error);
    }
}

// Renderizar lista de arquivos
function renderFiles(arquivos) {
    filesList.innerHTML = '';

    arquivos.forEach(arquivo => {
        const fileCard = document.createElement('div');
        fileCard.className = 'file-card';

        fileCard.innerHTML = `
            <div class="file-icon-wrapper">
                <i class="fas fa-file-powerpoint"></i>
            </div>
            <div class="file-info">
                <div class="file-name">${arquivo.filename}</div>
                <div class="file-meta">
                    <span>
                        <i class="fas fa-calendar"></i>
                        ${arquivo.modified}
                    </span>
                    <span>
                        <i class="fas fa-hdd"></i>
                        ${formatFileSize(arquivo.size)}
                    </span>
                    <span>
                        <i class="fas fa-clock"></i>
                        ${formatTimestamp(arquivo.timestamp)}
                    </span>
                </div>
            </div>
            <div class="file-actions">
                <button class="btn-download" onclick="downloadFile('${arquivo.download_url}')">
                    <i class="fas fa-download"></i>
                    Baixar
                </button>
            </div>
        `;

        filesList.appendChild(fileCard);
    });
}

// Função para download
function downloadFile(url) {
    window.location.href = url;
}

// Formatar tamanho do arquivo
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Formatar timestamp
function formatTimestamp(timestamp) {
    if (timestamp === 'desconhecido') return 'Data desconhecida';
    
    // Formato: YYYYMMDD_HHMMSS
    try {
        const year = timestamp.substring(0, 4);
        const month = timestamp.substring(4, 6);
        const day = timestamp.substring(6, 8);
        const hour = timestamp.substring(9, 11);
        const minute = timestamp.substring(11, 13);
        
        return `${day}/${month}/${year} ${hour}:${minute}`;
    } catch {
        return timestamp;
    }
}
