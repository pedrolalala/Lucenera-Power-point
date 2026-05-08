"""
Sistema de Geração de PowerPoint - LUCENERA
Versão DESENVOLVIMENTO (com debug ativado)

⚠️ PARA PRODUÇÃO: Use app_production.py
   - Logging com rotação
   - Health check endpoint
   - Modo produção (sem debug)
   - Configuração via .env

📖 Ver DEPLOY_README.md para instruções de deploy
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

app = Flask(__name__, 
            static_folder='web',
            template_folder='web')

# Configurações
UPLOAD_FOLDER = r'C:\Users\pedro\OneDrive\Desktop\lucenera'
ALLOWED_EXTENSIONS = {'pdf', 'xml'}  # Suporte para PDF e XML
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Caminho dos scripts
SCRIPT_DIR = r'C:\script python\script python power point'
MAIN_PY = os.path.join(SCRIPT_DIR, 'main.py')
PPT_PY = os.path.join(SCRIPT_DIR, 'ppt.py')  # Novo sistema SharePoint
EXCEL_MASTER = r'C:\Users\pedro\OneDrive\Desktop\lucenera\master_produtos.xlsx'  # Caminho do Excel master
PYTHON_VENV = os.path.join(SCRIPT_DIR, '.venv', 'Scripts', 'python.exe')

# Armazenar status dos jobs em memória
jobs = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
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
        
        # Listar todos os arquivos .pptx na pasta
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.endswith('.pptx') and filename.startswith('orcamento_'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_stat = os.stat(file_path)
                
                # Extrair timestamp do nome do arquivo se possível
                timestamp_match = re.search(r'orcamento_(\d{8}_\d{6})\.pptx', filename)
                timestamp_str = timestamp_match.group(1) if timestamp_match else 'desconhecido'
                
                arquivos.append({
                    'filename': filename,
                    'timestamp': timestamp_str,
                    'size': file_stat.st_size,
                    'modified': datetime.fromtimestamp(file_stat.st_mtime).strftime('%d/%m/%Y %H:%M:%S'),
                    'download_url': f'/download_file/{filename}'
                })
        
        # Ordenar por data de modificação (mais recente primeiro)
        arquivos.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'success': True, 'arquivos': arquivos})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/processar', methods=['POST'])
def processar_orcamento():
    try:
        # Verificar se arquivo foi enviado (PDF ou XML)
        file_key = 'pdf_file' if 'pdf_file' in request.files else 'xml_file'
        
        if file_key not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files[file_key]
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido. Use PDF ou XML'}), 400
        
        # Determinar tipo de arquivo
        file_type = 'xml' if file.filename.lower().endswith('.xml') else 'pdf'
        
        # Gerar ID único para o job
        job_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvar arquivo
        filename = secure_filename(file.filename)
        file_extension = 'xml' if file_type == 'xml' else 'pdf'
        saved_filename = f'orcamento_{timestamp}.{file_extension}'
        file_path = os.path.join(UPLOAD_FOLDER, saved_filename)
        
        file.save(file_path)
        print(f"[OK] {file_type.upper()} salvo: {file_path}")
        
        # Criar registro do job
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
        
        # Iniciar processamento em background
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
        print(f"[ERRO] Erro geral: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

def process_xml_job(job_id, xml_path, timestamp):
    """Processar job XML usando SharePoint (novo sistema)"""
    try:
        print(f"[INICIO] [{job_id}] Iniciando processamento XML com SharePoint...")
        
        # Atualizar status: processando
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 30
        
        # Verificar se Excel master existe
        if not os.path.exists(EXCEL_MASTER):
            raise Exception(f'Excel master não encontrado: {EXCEL_MASTER}')
        
        # Atualizar status: gerando PPT
        jobs[job_id]['status'] = 'generating'
        jobs[job_id]['progress'] = 60
        
        # Preparar argumentos para o ppt.py
        output_ppt = os.path.join(UPLOAD_FOLDER, f'orcamento_{timestamp}.pptx')
        
        # Executar ppt.py com argumentos
        print(f"[EXEC] [{job_id}] Executando ppt.py (SharePoint)...")
        
        # Criar script wrapper temporário com parâmetros
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
            # Executar wrapper
            result = subprocess.run(
                [PYTHON_VENV, wrapper_path],
                capture_output=True,
                text=True,
                cwd=SCRIPT_DIR,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode != 0:
                raise Exception(f'Erro na geração PPT: {result.stderr}')
            
            print(f"[OK] [{job_id}] ppt.py executado com sucesso")
            print(f"[OUTPUT] Output: {result.stdout}")
            
        finally:
            # Remover wrapper temporário
            if os.path.exists(wrapper_path):
                os.remove(wrapper_path)
        
        # Verificar se PPT foi gerado
        if not os.path.exists(output_ppt):
            raise Exception('PPT não foi gerado corretamente')
        
        # Atualizar status: concluído
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['ppt_path'] = output_ppt
        jobs[job_id]['download_url'] = f'/download/{timestamp}'
        
        print(f"[SUCESSO] [{job_id}] Job XML concluído com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] [{job_id}] Erro XML: {str(e)}")
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['error'] = str(e)


def process_pdf_job(job_id, pdf_path, timestamp):
    """Processar job PDF (sistema reativado com SharePoint)"""
    try:
        print(f"[PDF] [{job_id}] Processando PDF...")
        
        # Atualizar status: processando
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['progress'] = 30
        
        # Verificar se Excel master existe
        if not os.path.exists(EXCEL_MASTER):
            raise Exception(f'Excel master não encontrado: {EXCEL_MASTER}')
        
        # Atualizar status: gerando PPT
        jobs[job_id]['status'] = 'generating'
        jobs[job_id]['progress'] = 60
        
        # Preparar argumentos para o ppt.py
        output_ppt = os.path.join(UPLOAD_FOLDER, f'orcamento_{timestamp}.pptx')
        
        # Executar ppt.py com argumentos PDF
        print(f"[EXEC] [{job_id}] Executando ppt.py (PDF + SharePoint)...")
        
        # Criar script wrapper temporário com parâmetros
        wrapper_script = f"""
import sys
sys.path.append(r'{SCRIPT_DIR}')

from ppt import gerar_powerpoint_pdf

try:
    resultado = gerar_powerpoint_pdf(
        pdf_path=r'{pdf_path}',
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
            # Executar wrapper
            result = subprocess.run(
                [PYTHON_VENV, wrapper_path],
                capture_output=True,
                text=True,
                cwd=SCRIPT_DIR,
                timeout=300  # 5 minutos timeout
            )
            
            if result.returncode != 0:
                raise Exception(f'Erro na geração PPT de PDF: {result.stderr}')
            
            print(f"[OK] [{job_id}] ppt.py executado com sucesso")
            print(f"[OUTPUT] Output: {result.stdout}")
            
        finally:
            # Remover wrapper temporário
            if os.path.exists(wrapper_path):
                os.remove(wrapper_path)
        
        # Verificar se PPT foi gerado
        if not os.path.exists(output_ppt):
            raise Exception('PPT não foi gerado corretamente')
        
        # Atualizar status: concluído
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['ppt_path'] = output_ppt
        jobs[job_id]['download_url'] = f'/download/{timestamp}'
        
        print(f"[SUCESSO] [{job_id}] Job PDF concluído com sucesso!")
        
    except Exception as e:
        print(f"[ERRO] [{job_id}] Erro PDF: {str(e)}")
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
        'ppt_path': job.get('ppt_path'),
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
        
        return send_file(
            ppt_path,
            as_attachment=True,
            download_name=f'orcamento_lucenera_{timestamp}.pptx',
            mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    """Download de arquivo específico pelo nome completo"""
    try:
        # Sanitizar nome do arquivo para segurança
        filename = secure_filename(filename)
        
        # Caminho completo do arquivo
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        # Verificar se arquivo existe
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        # Determinar mimetype baseado na extensão
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
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Criar pasta de upload se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    print("[SERVIDOR] Servidor Lucenera iniciado!")
    print(f"[PASTA] Pasta de upload: {UPLOAD_FOLDER}")
    print(f"[PYTHON] Python venv: {PYTHON_VENV}")
    print("[WEB] Acesse: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
