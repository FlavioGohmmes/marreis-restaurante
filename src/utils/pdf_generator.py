from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_pdf(pedidos, filename="pedido.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Tamanho da página
    margin = 50  # Margem para o conteúdo
    y = height - margin  # Posição vertical inicial

    # Função para adicionar uma nova página
    def nova_pagina():
        nonlocal y
        c.showPage()  # Finaliza a página atual
        y = height - margin  # Reinicia a posição vertical
        c.drawString(margin, y, "Comanda do Marreis Restaurante (Continuação)")
        y -= 20

    # Título da comanda
    c.drawString(margin, y, "Comanda do Marreis Restaurante")
    y -= 20

    for i, pedido in enumerate(pedidos):
        # Verifica se há espaço suficiente para o próximo pedido
        if y < margin + 200:  # Se faltar espaço, cria uma nova página
            nova_pagina()

        # Adiciona os detalhes do pedido
        c.drawString(margin, y, f"Pedido {i + 1}")
        y -= 20
        c.drawString(margin + 20, y, "Pratos Principais: " + ", ".join(pedido.pratos_principais))
        y -= 20
        c.drawString(margin + 20, y, "Guarnições: " + ", ".join(pedido.guarnicoes))
        y -= 20
        c.drawString(margin + 20, y, "Bebidas:")
        y -= 15
        for bebida in pedido.bebidas:
            c.drawString(margin + 40, y, f"{bebida['nome']} - R$ {bebida['valor']:.2f}")
            y -= 15
        if pedido.economia_dia["tamanho"]:
            c.drawString(margin + 20, y, f"Economia do Dia ({pedido.economia_dia['tamanho']}) - R$ {pedido.economia_dia['valor']:.2f}")
            y -= 20
        if pedido.principal["tamanho"]:
            c.drawString(margin + 20, y, f"Principal ({pedido.principal['tamanho']}) - R$ {pedido.principal['valor']:.2f}")
            y -= 20
        c.drawString(margin + 20, y, "Modo de Pagamento: " + ", ".join(pedido.pagamentos))
        y -= 20
        if "Dinheiro" in pedido.pagamentos:
            c.drawString(margin + 20, y, "Troco para: " + pedido.troco)
            y -= 20
        c.drawString(margin + 20, y, "Endereço: " + pedido.endereco)
        y -= 20
        c.drawString(margin + 20, y, "Observações: " + pedido.observacoes)
        y -= 40  # Espaço entre pedidos

    # Adiciona o valor total
    total = sum(pedido.calcular_total() for pedido in pedidos)
    c.drawString(margin, y, f"Valor Total: R$ {total:.2f}")
    y -= 40

    # Finaliza o PDF
    c.save()