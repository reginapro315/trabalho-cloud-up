import os
import psycopg2
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS # Importado para evitar o erro de conexão

app = Flask(__name__)

# CORREÇÃO DO ERRO DE CONEXÃO: Configuração explícita do CORS
# Permite que qualquer frontend (origem="*") acesse a API
CORS(app, resources={r"/*": {"origins": "*"}})

# Variável de ambiente (DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    # Cria a conexão com o banco de dados Supabase
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def home():
    return "API Rodando no Render com Supabase!"

@app.route('/livros', methods=['POST'])
def add_livro():
    """ Adiciona um novo livro ao banco de dados. """
    data = request.json
    
    # Validação simples
    if not data or not data.get('titulo'):
        return jsonify({"erro": "Título é obrigatório"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO livros (titulo, autor) VALUES (%s, %s) RETURNING id, titulo, autor, status;",
            (data['titulo'], data.get('autor', 'Autor Desconhecido'))
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
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
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
        
        lista = []
        for l in livros:
            lista.append({"id": l[0], "titulo": l[1], "autor": l[2], "status": l[3]})
            
        return jsonify(lista)
    except Exception as e:
        return jsonify({"erro": "Falha ao consultar banco de dados: " + str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Configuração para rodar com Gunicorn no Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
