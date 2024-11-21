from flask import Flask, request, render_template, flash
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Necessária para mensagens flash

# Classe Blockchain para manter o hash
class Blockchain:
    def __init__(self):
        self.blocks = []
        self.add_genesis_block()

    def add_genesis_block(self):
        self.blocks.append({"hash": "genesis_hash"})

    def add_block(self, hash_arquivo):
        self.blocks.append({"hash": hash_arquivo})

    def verify_hash(self, hash_arquivo):
        for bloco in self.blocks:
            if bloco["hash"] == hash_arquivo:
                return True
        return False

# Instância da blockchain
blockchain = Blockchain()

# Função para calcular o hash do arquivo
def calcular_hash_arquivo(caminho_arquivo):
    try:
        sha256_hash = hashlib.sha256()
        with open(caminho_arquivo, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Erro ao calcular o hash do arquivo: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join("uploads", filename)
        file.save(filepath)

        # Calcular o hash do arquivo
        hash_arquivo = calcular_hash_arquivo(filepath)
        if hash_arquivo:
            blockchain.add_block(hash_arquivo)
            flash(f"Arquivo enviado e registrado com sucesso! Hash: {hash_arquivo}", "success")
        else:
            flash("Erro ao calcular o hash do arquivo", "error")

    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    hash_arquivo = request.form['hash']
    if blockchain.verify_hash(hash_arquivo):
        flash(f"Hash {hash_arquivo} encontrado na blockchain!", "success")
    else:
        flash(f"Hash {hash_arquivo} não encontrado na blockchain.", "error")

    return render_template('index.html')

@app.route('/politicas')
def politicas_privacidade():
    return render_template('politicas.html')

if __name__ == '__main__':
    app.run(debug=True)