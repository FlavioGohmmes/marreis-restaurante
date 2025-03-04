from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime


def gerar_pdf(pedido, numero_pedido, filename="pedido.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Tamanho da página
    margin = 30  # Margem reduzida
    y = height - margin  # Posição vertical inicial

    # Título da comanda
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "MARREIS Restaurante")
    y -= 25

    # Número do pedido
    c.setFont("Helvetica", 14)
    c.drawString(margin, y, f"Número do Pedido: {numero_pedido}")
    y -= 25

    # Data e Hora
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c.drawString(margin, y, f"Data e Hora: {data_hora_atual}")
    y -= 25

    # Adiciona os detalhes do pedido
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Pedido:")
    y -= 20

    # Pratos Principais
    c.setFont("Helvetica", 12)
    c.drawString(margin + 20, y, "Pratos Principais: " +
                 ", ".join(pedido.pratos_principais))
    y -= 20

    # Guarnições (uma embaixo da outra)
    c.drawString(margin + 20, y, "Guarnições:")
    y -= 15
    for guarnicao in pedido.guarnicoes:
        c.drawString(margin + 40, y, f"- {guarnicao}")
        y -= 15

    # Bebidas
    c.drawString(margin + 20, y, "Bebidas:")
    y -= 15
    for bebida in pedido.bebidas:
        c.drawString(margin + 40, y,
                     f"{bebida['nome']} - R$ {bebida['valor']:.2f}")
        y -= 15

    # Economia do Dia
    if pedido.economia_dia["tamanho"]:
        c.drawString(
            margin + 20, y, f"Economia do Dia ({pedido.economia_dia['tamanho']}) - R$ {pedido.economia_dia['valor']:.2f}")
        y -= 20

    # Principal
    if pedido.principal["tamanho"]:
        c.drawString(
            margin + 20, y, f"Principal ({pedido.principal['tamanho']}) - R$ {pedido.principal['valor']:.2f}")
        y -= 20

    # Modo de Pagamento
    c.drawString(margin + 20, y, "Modo de Pagamento: " +
                 ", ".join(pedido.pagamentos))
    y -= 20

    # Troco (se aplicável)
    if "Dinheiro" in pedido.pagamentos:
        c.drawString(margin + 20, y, "Troco de: " + pedido.troco)
        y -= 20

    # Endereço
    c.drawString(margin + 20, y, "Endereço: " + pedido.endereco)
    y -= 20

    # Observações
    c.drawString(margin + 20, y, "Observações: " + pedido.observacoes)
    y -= 30  # Espaço entre pedidos

    # Valor Total
    c.setFont("Helvetica-Bold", 14)
    total = pedido.calcular_total()
    c.drawString(margin, y, f"Valor Total: R$ {total:.2f}")
    y -= 40

    # Finaliza o PDF
    c.save()
