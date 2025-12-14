import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configuração robusta do CORS (Resolve o erro do Dashboard)
CORS(app, resources={r"/*": {"origins": "*"}})

# Obtém o URI da variável de ambiente (já corrigida no Render)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """ Tenta conectar ao Supabase usando a DATABASE_URL. """
    if not DATABASE_URL:
        # Se a variável de ambiente não estiver no Render, ele falha.
        raise ValueError("DATABASE_URL não está configurada no ambiente.")
    
    # Adicionando timeout para evitar que a conexão trave
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=10) 
    return conn

@app.route('/')
def home():
    return "API Rodando no Render com Supabase (Versão Final)!"

@app.route('/livros', methods=['POST'])
def add_livro():
    """ Adiciona um novo livro ao banco de dados. """
    data = request.json
    if not data or not data.get('titulo'):
        return jsonify({"erro": "Título é obrigatório"}), 400

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO livros (titulo, autor) VALUES (%s, %s) RETURNING id, titulo, autor, status;",
            (data['titulo'], data.get('autor', 'N/A'))
        )
        novo_livro = cur.fetchone()
        conn.commit()
        return jsonify({
            "id": novo_livro[0], 
            "titulo": novo_livro[1], 
            "autor": novo_livro[2],
            "status": novo_livro[3]
        }), 201
    except Exception as e:
        if conn: conn.rollback()
        # Retorna o erro específico do banco de dados, útil para depuração
        return jsonify({"erro": f"Falha no Banco de Dados: {str(e)}"}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

@app.route('/livros', methods=['GET'])
def get_livros():
    """ Lista todos os livros cadastrados. """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, autor, status FROM livros ORDER BY created_at DESC;")
        livros = cur.fetchall()
        
        lista = []
        for l in livros:
            lista.append({"id": l[0], "titulo": l[1], "autor": l[2], "status": l[3]})
            
        return jsonify(lista)
    except Exception as e:
        # Retorna a falha de conexão como JSON, resolvendo o Internal Server Error
        return jsonify({"erro": f"Falha ao conectar/consultar o banco de dados: {str(e)}"}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
