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


def atualizar_projeto(id_, nome, cliente, prazo, valor, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE projetos SET nome_projeto=?, cliente=?, prazo_entrega=?, valor=?, status=? WHERE id=?
    """, (nome, cliente, prazo, valor, status, id_))
    conn.commit()
    conn.close()

def excluir_projeto(id_):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projetos WHERE id=?", (id_,))
    conn.commit()
    conn.close()

def clientes_unicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT cliente FROM projetos")
    clientes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return clientes

def total_por_cliente(cliente):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(valor) FROM projetos 
        WHERE cliente=? AND status='Concluído'
    """, (cliente,))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0



