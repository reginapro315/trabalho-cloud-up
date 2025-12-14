import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pega a URL do banco das variáveis de ambiente (Segurança!)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def home():
    return "API Rodando no Render com Supabase!"

@app.route('/livros', methods=['POST'])
def add_livro():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO livros (titulo, autor) VALUES (%s, %s) RETURNING id, titulo, autor;",
        (data['titulo'], data['autor'])
    )
    novo_livro = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": novo_livro[0], "titulo": novo_livro[1], "autor": novo_livro[2]}), 201

@app.route('/livros', methods=['GET'])
def get_livros():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titulo, autor, status FROM livros;")
    livros = cur.fetchall()
    cur.close()
    conn.close()
    
    lista = []
    for l in livros:
        lista.append({"id": l[0], "titulo": l[1], "autor": l[2], "status": l[3]})
        
    return jsonify(lista)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
