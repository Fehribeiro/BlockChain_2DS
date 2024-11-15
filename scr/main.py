from flask import Flask, render_template, request, redirect, url_for, flash
import os 
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)                       #senha de segurança

UPLOAD_FOLDER = 'uploads'                             #garante que o upload tenha um diretório
if not os.path.exists(UPLOAD_FOLDER):                 #verifica se o diretorio ja existe/ makedirs cria a pasta
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

def criar_timestamp(arquivo):
    try:
        subprocess.run(["ots", "stamp", arquivo], check=True) #executa timestamp no terminal/servidor (que no flask sou eu)
        flash(f"Timestamp criado para o arquivo {arquivo}.", "success")
    except subprocess.CalledProcessError as e:         #tratamento para erro no timestamp
        flash(f"Erro ao criar timestamp: {e}", "error")

def verificar_timestamp(arquivo):
    arquivo_timestamp = f"{arquivo}.ots"               #define o nome do arquivo de timestamp com a extensão .ots
    if not os.path.exists(arquivo_timestamp):          #verifica se o arquivo de fato existe
        flash(f"Arquivo de timestamp '{arquivo_timestamp}' não encontrado.", "error")
        return

    try:
        subprocess.run(["ots", "verify", arquivo_timestamp], check=True) #verifica o timestamp
        flash(f"Timestamp do arquivo {arquivo} verificado com sucesso.", "success") 
    except subprocess.CalledProcessError as e:         #verifica possiveis erros
        flash(f"Erro ao verificar timestamp: {e}", "error")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo enviado.', "error")
            return redirect(request.url)       #situação para constar possivel erro

        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado.', "error")  #situação para constar possivel erro
            return redirect(request.url)

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)        #Upload do arquivo
            criar_timestamp(file_path)
            return redirect(url_for('upload_file'))    
        
    return render_template('upload.html')

@app.route('/verify/<filename>')
def verify_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    verificar_timestamp(file_path)
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    app.run(debug=True)
    