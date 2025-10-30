import sqlite3

def conectar():
    conn = sqlite3.connect("freelancer.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_projeto TEXT NOT NULL,
        cliente TEXT NOT NULL,
        prazo_entrega TEXT,
        valor REAL,
        status TEXT
    )
    """)
    conn.commit()
    return conn

import sqlite3


def inserir_projeto(nome, cliente, prazo, valor, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projetos (nome_projeto, cliente, prazo_entrega, valor, status) VALUES (?, ?, ?, ?, ?)",
                   (nome, cliente, prazo, valor, status))
    conn.commit()
    conn.close()

def listar_projetos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projetos")
    projetos = cursor.fetchall()
    conn.close()
    return projetos



