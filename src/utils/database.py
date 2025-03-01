# src/utils/database.py
import sqlite3

def criar_banco_dados():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    # Tabela de pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido TEXT UNIQUE,
            pratos_principais TEXT,
            guarnicoes TEXT,
            bebidas TEXT,
            economia_dia TEXT,
            principal TEXT,
            pagamentos TEXT,
            endereco TEXT,
            observacoes TEXT,
            troco TEXT,
            total REAL
        )
    ''')

    # Tabela para controle de sequência
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sequencia_pedidos (
            ultimo_numero INTEGER DEFAULT 0
        )
    ''')

    # Inicializar a sequência se a tabela estiver vazia
    cursor.execute('SELECT COUNT(*) FROM sequencia_pedidos')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO sequencia_pedidos (ultimo_numero) VALUES (0)')

    conn.commit()
    conn.close()

def gerar_numero_pedido():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()

    # Incrementar o último número de pedido
    cursor.execute('UPDATE sequencia_pedidos SET ultimo_numero = ultimo_numero + 1')
    cursor.execute('SELECT ultimo_numero FROM sequencia_pedidos')
    numero_pedido = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    return f"PED{numero_pedido:04d}"  # Formato PED0001, PED0002, etc.

def salvar_pedido(pedido, numero_pedido):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pedidos (
            numero_pedido, pratos_principais, guarnicoes, bebidas, economia_dia, principal, pagamentos, endereco, observacoes, troco, total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        numero_pedido,
        ', '.join(pedido.pratos_principais),
        ', '.join(pedido.guarnicoes),
        ', '.join([f"{b['nome']} (R$ {b['valor']:.2f})" for b in pedido.bebidas]),
        f"{pedido.economia_dia['tamanho']} - R$ {pedido.economia_dia['valor']:.2f}" if pedido.economia_dia['tamanho'] else "Nenhum",
        f"{pedido.principal['tamanho']} - R$ {pedido.principal['valor']:.2f}" if pedido.principal['tamanho'] else "Nenhum",
        ', '.join(pedido.pagamentos),
        pedido.endereco,
        pedido.observacoes,
        pedido.troco,
        pedido.calcular_total()
    ))
    conn.commit()
    conn.close()

def listar_pedidos():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos ORDER BY id DESC')
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def buscar_pedido_por_numero(numero_pedido):
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE numero_pedido = ?', (numero_pedido,))
    pedido = cursor.fetchone()
    conn.close()
    return pedido