import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configuração robusta do CORS (Para o Dashboard)
CORS(app, resources={r"/*": {"origins": "*"}})

# Nome do arquivo do banco de dados SQLite
DATABASE_FILE = "inventario.db"

def get_db_connection():
    """ Conecta-se ao banco de dados SQLite. """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

def init_db():
    """ Cria a tabela 'livros' se ela não existir. """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT,
            status TEXT DEFAULT 'Disponivel',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# Inicializa o banco de dados na inicialização do aplicativo
init_db()

@app.route('/')
def home():
    return "API Rodando no Render com SQLite (Solução de Emergência)!"

@app.route('/livros', methods=['POST'])
def add_livro():
    """ Adiciona um novo livro. """
    data = request.json
    if not data or not data.get('titulo'):
        return jsonify({"erro": "Título é obrigatório"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO livros (titulo, autor) VALUES (?, ?)",
            (data['titulo'], data.get('autor', 'Autor Desconhecido'))
        )
        conn.commit()
        
        # Recupera o livro recém-inserido para retornar o ID
        cur.execute("SELECT * FROM livros WHERE id = last_insert_rowid()")
        novo_livro = cur.fetchone()
        
        return jsonify(dict(novo_livro)), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Falha ao inserir no BD: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/livros', methods=['GET'])
def get_livros():
    """ Lista todos os livros cadastrados. """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, titulo, autor, status FROM livros ORDER BY created_at DESC;")
        livros = cur.fetchall()
        
        lista = [dict(l) for l in livros] # Converte linhas SQLite em dicionários
        
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Falha ao consultar o BD: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Cria o arquivo do banco de dados antes de iniciar a aplicação
    init_db()
    app.run(host='0.0.0.0', port=5000)import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configuração robusta do CORS (Para o Dashboard)
CORS(app, resources={r"/*": {"origins": "*"}})

# Nome do arquivo do banco de dados SQLite
DATABASE_FILE = "inventario.db"

def get_db_connection():
    """ Conecta-se ao banco de dados SQLite. """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
    return conn

def init_db():
    """ Cria a tabela 'livros' se ela não existir. """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            autor TEXT,
            status TEXT DEFAULT 'Disponivel',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# Inicializa o banco de dados na inicialização do aplicativo
init_db()

@app.route('/')
def home():
    return "API Rodando no Render com SQLite (Solução de Emergência)!"

@app.route('/livros', methods=['POST'])
def add_livro():
    """ Adiciona um novo livro. """
    data = request.json
    if not data or not data.get('titulo'):
        return jsonify({"erro": "Título é obrigatório"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO livros (titulo, autor) VALUES (?, ?)",
            (data['titulo'], data.get('autor', 'Autor Desconhecido'))
        )
        conn.commit()
        
        # Recupera o livro recém-inserido para retornar o ID
        cur.execute("SELECT * FROM livros WHERE id = last_insert_rowid()")
        novo_livro = cur.fetchone()
        
        return jsonify(dict(novo_livro)), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": f"Falha ao inserir no BD: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/livros', methods=['GET'])
def get_livros():
    """ Lista todos os livros cadastrados. """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, titulo, autor, status FROM livros ORDER BY created_at DESC;")
        livros = cur.fetchall()
        
        lista = [dict(l) for l in livros] # Converte linhas SQLite em dicionários
        
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": f"Falha ao consultar o BD: {str(e)}"}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Cria o arquivo do banco de dados antes de iniciar a aplicação
    init_db()
    app.run(host='0.0.0.0', port=5000)
