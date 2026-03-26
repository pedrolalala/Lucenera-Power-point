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
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Caminho dos scripts
SCRIPT_DIR = r'C:\script python\script python power point'
MAIN_PY = os.path.join(SCRIPT_DIR, 'main.py')
MAGICA_PPT_PY = os.path.join(SCRIPT_DIR, 'magica_ppt.py')
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
        # Verificar se arquivo foi enviado
        if 'pdf_file' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['pdf_file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nenhum arquivo selecionado'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Tipo de arquivo não permitido'}), 400
        
        # Gerar ID único para o job
        job_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvar arquivo PDF
        filename = secure_filename(file.filename)
        pdf_filename = f'orcamento_{timestamp}.pdf'
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        
        file.save(pdf_path)
        print(f"✅ PDF salvo: {pdf_path}")
        
        # Criar registro do job
        jobs[job_id] = {
            'status': 'uploading',
            'progress': 10,
            'filename': filename,
            'pdf_path': pdf_path,
            'timestamp': timestamp,
            'ppt_path': None,
            'error': None
        }
        
        # Iniciar processamento em background
        thread = threading.Thread(target=process_job, args=(job_id, pdf_path, timestamp))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Processamento iniciado'
        })
    
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

def process_job(job_id, pdf_path, timestamp):
    """Processar job em background"""
    try:
        # Atualizar status: organizando
        jobs[job_id]['status'] = 'organizing'
        jobs[job_id]['progress'] = 30
        
        # Atualizar caminho do PDF no magica_ppt.py temporariamente
        magica_ppt_modified = os.path.join(SCRIPT_DIR, f'magica_ppt_{job_id}.py')
        
        # Ler conteúdo do magica_ppt.py
        with open(MAGICA_PPT_PY, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir caminho do PDF
        original_pdf = r'OR_0006316 FELIPE E DENISE PAISAGISMO b.pdf'
        content_modified = content.replace(
            f'pdf_orcamento = r"C:\\Users\\pedro\\OneDrive\\Desktop\\lucenera\\{original_pdf}"',
            f'pdf_orcamento = r"{pdf_path}"'
        )
        
        # Salvar versão modificada
        with open(magica_ppt_modified, 'w', encoding='utf-8') as f:
            f.write(content_modified)
        
        # Executar main.py (organizar arquivos)
        print(f"🔄 [{job_id}] Executando main.py...")
        result_main = subprocess.run(
            [PYTHON_VENV, MAIN_PY],
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        if result_main.returncode != 0:
            raise Exception(f'Erro ao organizar arquivos: {result_main.stderr}')
        
        print(f"✅ [{job_id}] main.py executado")
        
        # Atualizar status: gerando PPT
        jobs[job_id]['status'] = 'generating'
        jobs[job_id]['progress'] = 60
        
        # Executar magica_ppt.py (gerar PowerPoint)
        print(f"🔄 [{job_id}] Executando magica_ppt.py...")
        result_magica = subprocess.run(
            [PYTHON_VENV, magica_ppt_modified],
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR
        )
        
        # Remover arquivo temporário
        if os.path.exists(magica_ppt_modified):
            os.remove(magica_ppt_modified)
        
        if result_magica.returncode != 0:
            raise Exception(f'Erro ao gerar PPT: {result_magica.stderr}')
        
        print(f"✅ [{job_id}] magica_ppt.py executado")
        
        # Verificar se PPT foi gerado
        ppt_path = os.path.join(UPLOAD_FOLDER, 'orçamento_magico_v10.pptx')
        
        if not os.path.exists(ppt_path):
            raise Exception('PPT não foi gerado corretamente')
        
        # Renomear PPT com timestamp
        ppt_final = os.path.join(UPLOAD_FOLDER, f'orcamento_{timestamp}.pptx')
        shutil.copy2(ppt_path, ppt_final)
        
        # Atualizar status: concluído
        jobs[job_id]['status'] = 'completed'
        jobs[job_id]['progress'] = 100
        jobs[job_id]['ppt_path'] = ppt_final
        jobs[job_id]['download_url'] = f'/download/{timestamp}'
        
        print(f"✅ [{job_id}] Job concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ [{job_id}] Erro: {str(e)}")
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
    
    print("🚀 Servidor Lucenera iniciado!")
    print(f"📁 Pasta de upload: {UPLOAD_FOLDER}")
    print(f"🐍 Python venv: {PYTHON_VENV}")
    print("🌐 Acesse: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
