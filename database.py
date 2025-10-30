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

