# src/utils/database.py
import sqlite3

def criar_banco_dados():
    conn = sqlite3.connect('pedidos.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

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
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos