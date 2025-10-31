import sqlite3  # Importa a biblioteca SQLite embutida no Python

# Função para conectar (ou criar) o banco de dados freelancer.db
def conectar():
    conexao = sqlite3.connect("freelancer.db")  # Cria ou conecta ao arquivo do banco
    cursor = conexao.cursor()                   # Cria um cursor para executar comandos SQL
    # Cria a tabela de projetos caso não exista ainda
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada projeto
        nome_projeto TEXT NOT NULL,            -- Nome do projeto
        cliente TEXT NOT NULL,                 -- Nome do cliente
        prazo_entrega DATE,                    -- Prazo de entrega do projeto
        valor REAL,                            -- Valor do projeto
        status TEXT                            -- Status (Proposta, Em Andamento, Concluído)
    )
    """)
    conexao.commit()  # Salva as alterações
    return conexao    # Retorna a conexão ativa


# Insere um novo projeto no banco de dados
def inserir_projeto(nome, cliente, prazo, valor, status):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        valor = float(valor)  # Garante que o valor seja numérico
    except ValueError:
        valor = 0.0           # Se não for, define como 0
    # Executa o comando SQL de inserção
    cursor.execute("""
        INSERT INTO projetos (nome_projeto, cliente, prazo_entrega, valor, status)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, cliente, prazo, valor, status))
    conexao.commit()  # Salva os dados
    conexao.close()   # Fecha a conexão


# Retorna uma lista com todos os projetos cadastrados
def listar_projetos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM projetos")  # Busca todos os registros
    projetos = cursor.fetchall()              # Coleta o resultado como lista de tuplas
    conexao.close()
    return projetos


# Atualiza um projeto existente (com base no ID)
def atualizar_projeto(id_, nome, cliente, prazo, valor, status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE projetos
        SET nome_projeto=?, cliente=?, prazo_entrega=?, valor=?, status=?
        WHERE id=?
    """, (nome, cliente, prazo, valor, status, id_))
    conexao.commit()
    conexao.close()


# Exclui um projeto com base no ID
def excluir_projeto(id_):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM projetos WHERE id=?", (id_,))
    conexao.commit()
    conexao.close()


# Retorna uma lista de clientes únicos (sem repetições)
def clientes_unicos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT DISTINCT cliente FROM projetos")  # DISTINCT remove duplicatas
    clientes = [row[0] for row in cursor.fetchall()]         # Extrai só o nome
    conexao.close()
    return clientes


# Retorna o total de valores "Concluídos" por cliente
def total_por_cliente(cliente):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM projetos
        WHERE cliente = ? AND status = 'Concluído'
    """, (cliente,))          # COALESCE evita retornar None caso não haja registros
    total = cursor.fetchone()[0]  # Pega o primeiro (e único) resultado da soma
    conexao.close()
    return float(total)           # Retorna o total como número
