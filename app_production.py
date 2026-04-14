"""
Sistema de Geração de PowerPoint - LUCENERA
Versão PRODUÇÃO com Cloudflared
"""

from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import subprocess
import shutil
from datetime import datetime
import threading
import uuid
import re
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, 
            static_folder='web',
            template_folder='web')

# ==================== CONFIGURAÇÕES ====================
# Usar variáveis de ambiente com fallback para valores padrão

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', r'C:\Users\pedro\OneDrive\Desktop\lucenera')
SCRIPT_DIR = os.getenv('SCRIPT_DIR', r'C:\script python\script python power point')
EXCEL_MASTER = os.getenv('EXCEL_MASTER', r'C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx')
PYTHON_VENV = os.getenv('PYTHON_VENV', os.path.join(SCRIPT_DIR, '.venv', 'Scripts', 'python.exe'))

ALLOWED_EXTENSIONS = {'pdf', 'xml'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
PORT = int(os.getenv('PORT', '5001'))

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ==================== LOGGING ====================
def setup_logging():
    """Configurar logging para produção"""
    
    # Criar pasta de logs se não existir
    log_dir = os.path.join(SCRIPT_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Arquivo de log com rotação
    log_file = os.path.join(log_dir, 'app.log')
    
    # Handler com rotação (max 10MB, manter 5 arquivos)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024, 
        backupCount=5,
        encoding='utf-8'
    )
    
    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Configurar logger da aplicação
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    
    # Configurar logger do werkzeug (Flask)
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)

# Inicializar logging
setup_logging()

# ==================== ARMAZENAMENTO DE JOBS ====================
jobs = {}

# ==================== FUNÇÕES AUXILIARES ====================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== ROTAS ====================

@app.route('/health')
def health_check():
    """Health check para monitoramento"""
    try:
        # Verificar se arquivos críticos existem
        checks = {
            'upload_folder': os.path.exists(UPLOAD_FOLDER),
            'excel_master': os.path.exists(EXCEL_MASTER),
            'python_venv': os.path.exists(PYTHON_VENV),
            'script_dir': os.path.exists(SCRIPT_DIR)
        }
        
        all_ok = all(checks.values())
        
        return jsonify({
            'status': 'healthy' if all_ok else 'degraded',
            'timestamp': datetime.now().isoformat(),
            'checks': checks,
            'active_jobs': len(jobs),
            'version': '2.0-production'
        }), 200 if all_ok else 503
        
    except Exception as e:
        app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.route('/')
def index():
    app.logger.info("Página inicial acessada")
    return render_template('index.html')

@app.route('/status.html')
def status_page():
    return render_template('status.html')

@app.route('/gerenciar')
def gerenciar():
    """Página para gerenciar arquivos gerados"""
    return render_template('gerenciar.html')

@app.route('/api/listar_arquivos')
def listar_arquivos():
    """API para listar todos os arquivos PPT gerados"""
    try:
        arquivos = []
        
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.endswith('.pptx') and filename.startswith('orcamento_'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_stat = os.stat(file_path)
                
                timestamp_match = re.search(r'orcamento_(\d{8}_\d{6})\.pptx', filename)
                timestamp_str = timestamp_match.group(1) if timestamp_match else 'desconhecido'
                
                arquivos.append({
                    'filename': filename,
                    'timestamp': timestamp_str,
                    'size': file_stat.st_size,
                    'modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S'),
                    'download_url': f'/download_file/{filename}'
                })
        
        arquivos.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'success': True, 'arquivos': arquivos})
    
    except Exception as e:
        app.logger.error(f"Erro ao listar arquivos: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/processar', methods=['POST'])
def processar_orcamento():
    try:
        file_key = 'pdf_file' if 'pdf_file' in request.files else 'xml_file'
        
        if file_key not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files[file_key]
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido. Use PDF ou XML'}), 400
        
        file_type = 'xml' if file.filename.lower().endswith('.xml') else 'pdf'
        job_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        filename = secure_filename(file.filename)
        file_extension = 'xml' if file_type == 'xml' else 'pdf'
        saved_filename = f'orcamento_{timestamp}.{file_extension}'
        file_path = os.path.join(UPLOAD_FOLDER, saved_filename)
        
        file.save(file_path)
        app.logger.info(f"[{job_id}] Arquivo {file_type.upper()} recebido: {filename}")
        
        jobs[job_id] = {
            'status': 'uploading',
            'progress': 10,
            'filename': filename,
            'file_path': file_path,
            'file_type': file_type,
            'timestamp': timestamp,
            'ppt_path': None,
            'error': None
        }
        
        if file_type == 'xml':
            thread = threading.Thread(target=process_xml_job, args=(job_id, file_path, timestamp))
        else:
            thread = threading.Thread(target=process_pdf_job, args=(job_id, file_path, timestamp))
            
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'file_type': file_type,
            'message': f'Processamento {file_type.upper()} iniciado'
        })
    
    except Exception as e:
        app.logger.error(f"Erro no processamento: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

def process_xml_job(job_id, xml_path, timestamp):
    """Processar job XML usando SharePoint"""
    try:
        app.logger.info(f"[{job_id}] Iniciando processamento XML")
        
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 30
        
        if not os.path.exists(EXCEL_MASTER):
            raise Exception(f'Excel master não encontrado: {EXCEL_MASTER}')
        
        jobs[job_id]['status'] = 'generating'
        jobs[job_id]['progress'] = 60
        
        output_ppt = os.path.join(UPLOAD_FOLDER, f'orcamento_{timestamp}.pptx')
        
        wrapper_script = f"""
import sys
sys.path.append(r'{SCRIPT_DIR}')

from ppt import gerar_powerpoint_sharepoint

try:
    resultado = gerar_powerpoint_sharepoint(
        xml_path=r'{xml_path}',
        excel_path=r'{EXCEL_MASTER}',
        output_path=r'{output_ppt}'
    )
    print(f"[OK] Sucesso: {{resultado}}")
except Exception as e:
    print(f"[ERRO] Erro: {{str(e)}}")
    raise
"""
        
        wrapper_path = os.path.join(SCRIPT_DIR, f'wrapper_{job_id}.py')
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_script)
        
        try:
            result = subprocess.run(
                [PYTHON_VENV, wrapper_path],
                capture_output=True,
                text=True,
                cwd=SCRIPT_DIR,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f'Erro na geração PPT: {result.stderr}')
            
            app.logger.info(f"[{job_id}] PPT gerado com sucesso")
            
        finally:
            if os.path.exists(wrapper_path):
                os.remove(wrapper_path)
        
        if not os.path.exists(output_ppt):
            raise Exception('PPT não foi gerado corretamente')
        
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['ppt_path'] = output_ppt
        jobs[job_id]['download_url'] = f'/download/{timestamp}'
        
        app.logger.info(f"[{job_id}] Job concluído com sucesso")
        
    except Exception as e:
        app.logger.error(f"[{job_id}] Erro: {str(e)}", exc_info=True)
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)

def process_pdf_job(job_id, pdf_path, timestamp):
    """Processar job PDF (sistema legado)"""
    try:
        app.logger.warning(f"[{job_id}] PDF não suportado")
        raise Exception("Sistema legado PDF não implementado. Use XML.")
        
    except Exception as e:
        app.logger.error(f"[{job_id}] Erro PDF: {str(e)}")
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)

@app.route('/status/<job_id>')
def get_status(job_id):
    """Obter status de um job"""
    if job_id not in jobs:
        return jsonify({'error': 'Job não encontrado'}), 404
    
    job = jobs[job_id]
    return jsonify({
        'status': job['status'],
        'progress': job['progress'],
        'filename': job['filename'],
        'error': job.get('error'),
        'download_url': job.get('download_url')
    })

@app.route('/download/<timestamp>')
def download_ppt(timestamp):
    """Download do PPT pelo timestamp"""
    try:
        ppt_path = os.path.join(UPLOAD_FOLDER, f'orcamento_{timestamp}.pptx')
        
        if not os.path.exists(ppt_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        app.logger.info(f"Download iniciado: orcamento_{timestamp}.pptx")
        
        return send_file(
            ppt_path,
            as_attachment=True,
            download_name=f'orcamento_lucenera_{timestamp}.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    
    except Exception as e:
        app.logger.error(f"Erro no download: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    """Download de arquivo específico pelo nome completo"""
    try:
        filename = secure_filename(filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        if filename.endswith('.pptx'):
            mimetype = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        elif filename.endswith('.pdf'):
            mimetype = 'application/pdf'
        else:
            mimetype = 'application/octet-stream'
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
    
    except Exception as e:
        app.logger.error(f"Erro no download do arquivo: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Erro interno: {str(error)}", exc_info=True)
    return jsonify({'error': 'Erro interno do servidor'}), 500

# ==================== STARTUP ====================

if __name__ == '__main__':
    # Criar pastas necessárias
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(SCRIPT_DIR, 'logs'), exist_ok=True)
    
    app.logger.info("=" * 60)
    app.logger.info("SERVIDOR LUCENERA - PRODUÇÃO")
    app.logger.info("=" * 60)
    app.logger.info(f"Pasta de upload: {UPLOAD_FOLDER}")
    app.logger.info(f"Python venv: {PYTHON_VENV}")
    app.logger.info(f"Excel master: {EXCEL_MASTER}")
    app.logger.info(f"Porta: {PORT}")
    app.logger.info(f"Acesse: http://localhost:{PORT}")
    app.logger.info(f"Público: https://apilucenera.site")
    app.logger.info("=" * 60)
    
    # PRODUÇÃO: sem debug, multi-threaded
    app.run(
        debug=False,
        host='0.0.0.0',
        port=PORT,
        threaded=True
    )
