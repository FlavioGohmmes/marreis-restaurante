import customtkinter as ctk
from tkinter import messagebox
from models.pedido import Pedido
from utils.pdf_generator import gerar_pdf
from utils.database import salvar_pedido, listar_pedidos, buscar_pedido_por_numero, gerar_numero_pedido
import os
from datetime import datetime

# Configuração do tema do customtkinter
ctk.set_appearance_mode("dark")  # Modo de aparência (System, Light, Dark)
ctk.set_default_color_theme("blue")  # Tema de cores (blue, green, dark-blue)


class PedidoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marreis Restaurante - Gerador de Pedidos")
        self.root.minsize(670, 970)  # Tamanho mínimo da janela

        # Configuração do grid para responsividade
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.pedido = Pedido()  # Agora só há um pedido por vez
        self.criar_interface()

    def criar_interface(self):
        # Frame principal com barra de rolagem
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#2E2E2E")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Canvas para a barra de rolagem
        self.canvas = ctk.CTkCanvas(
            self.main_frame, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical
        self.scrollbar = ctk.CTkScrollbar(
            self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        # Frame interno para os widgets
        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color="#2E2E2E")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Habilitar rolagem com o mouse
        self.inner_frame.bind("<MouseWheel>", self.on_mousewheel)

        # Configuração do grid do inner_frame para centralização
        self.inner_frame.grid_columnconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(1, weight=1)
        self.inner_frame.grid_columnconfigure(2, weight=1)

        # Título do restaurante
        titulo = ctk.CTkLabel(self.inner_frame, text="MARREIS Restaurante", font=(
            "Helvetica", 24, "bold"), text_color="#FFFFFF")
        titulo.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        # Frame para o pedido
        self.frame_pedido = ctk.CTkFrame(
            self.inner_frame, fg_color="#3E3E3E", corner_radius=10)
        self.frame_pedido.grid(row=1, column=0, columnspan=3,
                               padx=10, pady=10, sticky="nsew")

        # Adicionar campo de data e hora
        self.data_hora_label = ctk.CTkLabel(self.frame_pedido, text="Data e Hora: ", font=(
            "Helvetica", 14), text_color="#FFFFFF")
        self.data_hora_label.grid(row=0, column=0, columnspan=3, pady=5)
        self.atualizar_data_hora()

        # Botão Finalizar Pedido
        btn_finalizar = ctk.CTkButton(self.inner_frame, text="Finalizar Pedido",
                                      command=self.finalizar_pedido, fg_color="#00004B", hover_color="#1C86EE", corner_radius=10)
        btn_finalizar.grid(row=2, column=0, columnspan=2,
                           pady=10, sticky="nsew")

        # Botão para visualizar pedidos
        btn_visualizar_pedidos = ctk.CTkButton(self.inner_frame, text="Visualizar Pedidos",
                                               command=self.mostrar_pedidos, fg_color="#00004B", hover_color="#1C86EE", corner_radius=10)
        btn_visualizar_pedidos.grid(
            row=2, column=2, columnspan=1, pady=10, sticky="nsew")

        # Botão para limpar pedido
        btn_limpar_pedido = ctk.CTkButton(self.inner_frame, text="Limpar Pedido",
                                          command=self.limpar_campos, fg_color="#8B4600", hover_color="#FF4500", corner_radius=10)
        btn_limpar_pedido.grid(row=3, column=0, columnspan=3,
                               pady=10, sticky="nsew")

        # Configuração do redimensionamento
        self.root.bind("<Configure>", self.on_resize)

        # Inicializa o pedido
        self.criar_pedido_interface()

    def criar_pedido_interface(self):
        frame_pedido = self.frame_pedido

        ctk.CTkLabel(frame_pedido, text="Pedido 1", font=("Helvetica", 16), text_color="#FFFFFF").grid(
            row=1, column=0, columnspan=3, pady=5, sticky="nsew")

        # Frame para os pratos principais
        frame_pratos = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_pratos.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(frame_pratos, text="Pratos Principais", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        pratos = ["Frango a Passarinho", "Linguiça", "Carne Moída com Batata",
                  "Parmegiana de Frango", "Carne de Panela", "Bife de Pernil"]
        for prato in pratos:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(frame_pratos, text=prato, variable=var, command=lambda p=prato, v=var: self.adicionar_prato(
                p, v), fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=5)
            cb.pack(pady=2, anchor="w")
            self.pedido.pratos_vars[prato] = var

        # Frame para as guarnições
        frame_guarnicoes = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_guarnicoes.grid(row=2, column=1, padx=5,
                              pady=5, sticky="nsew")

        ctk.CTkLabel(frame_guarnicoes, text="Guarnições", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        guarnicoes = ["Arroz", "Feijão", "Macarrão", "Quibebe",
                      "Farofa", "Batata Frita", "Legumes Refogados"]
        for guarnicao in guarnicoes:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(frame_guarnicoes, text=guarnicao, variable=var, command=lambda g=guarnicao, v=var: self.adicionar_guarnicao(
                g, v), fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=5)
            cb.pack(pady=2, anchor="w")
            self.pedido.guarn_vars[guarnicao] = var

        # Frame para as bebidas
        frame_bebidas = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_bebidas.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(frame_bebidas, text="Bebidas", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        bebidas = {"Água": 4, "Refrigerante": 6, "Suco": 10}
        for bebida, valor in bebidas.items():
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(frame_bebidas, text=f"{bebida} (R$ {valor:.2f})", variable=var, command=lambda b=bebida, v=var, val=valor: self.adicionar_bebida(
                b, v, val), fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=5)
            cb.pack(pady=2, anchor="w")
            self.pedido.bebidas_vars[bebida] = var

        # Frame para a "Economia do Dia"
        frame_economia_dia = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_economia_dia.grid(
            row=3, column=0, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(frame_economia_dia, text="Economia do Dia", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        self.pedido.economia_dia_var = ctk.StringVar(value="Nenhum")
        rb_economia_p = ctk.CTkRadioButton(frame_economia_dia, text="P - R$ 12,00",
                                           variable=self.pedido.economia_dia_var, value="P", command=lambda: self.adicionar_economia_dia("P"))
        rb_economia_p.pack(pady=2, anchor="w")
        rb_economia_m = ctk.CTkRadioButton(frame_economia_dia, text="M - R$ 18,00",
                                           variable=self.pedido.economia_dia_var, value="M", command=lambda: self.adicionar_economia_dia("M"))
        rb_economia_m.pack(pady=2, anchor="w")

        # Frame para o "Principal"
        frame_principal = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_principal.grid(row=3, column=1, padx=5,
                             pady=5, sticky="nsew")

        ctk.CTkLabel(frame_principal, text="Principal", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        self.pedido.principal_var = ctk.StringVar(value="Nenhum")
        rb_principal_p = ctk.CTkRadioButton(
            frame_principal, text="P - R$ 18,00", variable=self.pedido.principal_var, value="P", command=lambda: self.adicionar_principal("P"))
        rb_principal_p.pack(pady=2, anchor="w")
        rb_principal_m = ctk.CTkRadioButton(
            frame_principal, text="M - R$ 20,00", variable=self.pedido.principal_var, value="M", command=lambda: self.adicionar_principal("M"))
        rb_principal_m.pack(pady=2, anchor="w")

        # Frame para o modo de pagamento
        frame_pagamento = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_pagamento.grid(row=4, column=0, columnspan=3,
                             padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(frame_pagamento, text="Modo de Pagamento", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        pagamentos = ["Pix", "Débito", "Crédito", "Dinheiro"]
        for pagamento in pagamentos:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(frame_pagamento, text=pagamento, variable=var, command=lambda p=pagamento, v=var: self.adicionar_pagamento(
                p, v), fg_color="#1E90FF", hover_color="#1C86EE", corner_radius=5)
            cb.pack(side="left", padx=5, pady=2, anchor="w")
            self.pedido.pagamentos_vars[pagamento] = var

            # Adiciona campo de texto para o troco se o pagamento for em dinheiro
            if pagamento == "Dinheiro":
                self.pedido.troco_entry = ctk.CTkEntry(
                    frame_pagamento, placeholder_text="Troco ?", fg_color="#FFFFFF", text_color="#000000", corner_radius=5)
                self.pedido.troco_entry.pack(
                    side="left", padx=5, pady=5, anchor="w")

        # Frame para endereço e observações
        frame_endereco_obs = ctk.CTkFrame(
            frame_pedido, fg_color="#4E4E4E", corner_radius=10)
        frame_endereco_obs.grid(
            row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(frame_endereco_obs, text="Endereço", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        self.pedido.endereco_entry = ctk.CTkEntry(
            frame_endereco_obs, placeholder_text="Digite seu endereço", fg_color="#FFFFFF", text_color="#000000", corner_radius=5)
        self.pedido.endereco_entry.pack(pady=5, fill="x")

        ctk.CTkLabel(frame_endereco_obs, text="Observações", font=(
            "Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
        self.pedido.observacoes_entry = ctk.CTkEntry(
            frame_endereco_obs, placeholder_text="Alguma observação?", fg_color="#FFFFFF", text_color="#000000", corner_radius=5)
        self.pedido.observacoes_entry.pack(pady=5, fill="x")

    def atualizar_data_hora(self):
        data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.data_hora_label.configure(text=f"Data e Hora: {data_hora_atual}")
        # Atualiza a cada 1 segundo
        self.root.after(1000, self.atualizar_data_hora)

    def on_mousewheel(self, event):
        # Rola a tela com o mouse
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_resize(self, event):
        # Ajusta o tamanho do canvas ao redimensionar a janela
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def adicionar_prato(self, prato, var):
        if var.get():
            self.pedido.adicionar_prato(prato)
        else:
            self.pedido.remover_prato(prato)

    def adicionar_guarnicao(self, guarnicao, var):
        if var.get():
            self.pedido.adicionar_guarnicao(guarnicao)
        else:
            self.pedido.remover_guarnicao(guarnicao)

    def adicionar_bebida(self, bebida, var, valor):
        if var.get():
            self.pedido.adicionar_bebida(bebida, valor)
        else:
            self.pedido.remover_bebida(bebida)

    def adicionar_economia_dia(self, tamanho):
        self.pedido.adicionar_economia_dia(tamanho)

    def adicionar_principal(self, tamanho):
        self.pedido.adicionar_principal(tamanho)

    def adicionar_pagamento(self, pagamento, var):
        if var.get():
            self.pedido.adicionar_pagamento(pagamento)
        else:
            self.pedido.remover_pagamento(pagamento)

    def finalizar_pedido(self):
        if not self.pedido.pratos_principais:
            messagebox.showwarning(
                "Aviso", "Selecione pelo menos um prato principal.")
            return

        self.pedido.endereco = self.pedido.endereco_entry.get()
        self.pedido.observacoes = self.pedido.observacoes_entry.get()

        # Verifica se o campo de endereço está vazio
        if not self.pedido.endereco:
            messagebox.showwarning(
                "Aviso", "O campo de endereço não pode estar vazio.")
            return

        # Verifica se o pagamento é em dinheiro e se o campo de troco foi preenchido
        if "Dinheiro" in self.pedido.pagamentos and not self.pedido.troco_entry.get():
            messagebox.showwarning(
                "Aviso", "Informe o valor do troco para pagamento em dinheiro.")
            return
        self.pedido.troco = self.pedido.troco_entry.get(
        ) if "Dinheiro" in self.pedido.pagamentos else ""

        confirmar = messagebox.askyesno(
            "Confirmar", "Deseja finalizar a comanda?")
        if confirmar:
            # Gerar um número de pedido sequencial
            numero_pedido = gerar_numero_pedido()

            # Salvar o pedido no banco de dados
            salvar_pedido(self.pedido, numero_pedido)

            # Gerar o PDF
            gerar_pdf(self.pedido, numero_pedido)
            messagebox.showinfo(
                "Sucesso", f"Comanda finalizada e PDF gerado com sucesso! Número do pedido: {numero_pedido}")
            os.startfile("pedido.pdf")
            self.limpar_campos()

    def limpar_campos(self):
        # Limpa todos os campos do pedido
        self.pedido.limpar_campos()

    def mostrar_pedidos(self):
        pedidos = listar_pedidos()
        if not pedidos:
            messagebox.showinfo("Pedidos", "Nenhum pedido encontrado.")
            return

        # Criar uma nova janela para exibir os pedidos
        self.janela_pedidos = ctk.CTkToplevel(
            self.root)  # Armazenar a referência da janela
        self.janela_pedidos.title("Pedidos Realizados")
        self.janela_pedidos.geometry("800x600")

        # Frame para busca
        frame_busca = ctk.CTkFrame(
            self.janela_pedidos, fg_color="#3E3E3E", corner_radius=10)
        frame_busca.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(frame_busca, text="Buscar por Número do Pedido:").pack(
            side="left", padx=5)
        self.entry_busca = ctk.CTkEntry(
            frame_busca, width=150, fg_color="#FFFFFF", text_color="#000000", corner_radius=5)
        self.entry_busca.pack(side="left", padx=5)
        btn_buscar = ctk.CTkButton(frame_busca, text="Buscar", command=self.buscar_pedido,
                                   fg_color="#00004B", hover_color="#1C86EE", corner_radius=5)
        btn_buscar.pack(side="left", padx=5)

        # Área de texto para exibir os pedidos
        self.texto_pedidos = ctk.CTkTextbox(
            self.janela_pedidos, wrap="word", fg_color="#2E2E2E", text_color="#FFFFFF", corner_radius=10)
        self.texto_pedidos.pack(fill="both", expand=True, padx=10, pady=10)

        # Exibir todos os pedidos
        self.exibir_pedidos(pedidos)

    def exibir_pedidos(self, pedidos):
        self.texto_pedidos.delete("1.0", "end")
        for pedido in pedidos:
            self.texto_pedidos.insert(
                "end", f"Número do Pedido: {pedido[1]}\n")
            self.texto_pedidos.insert(
                "end", f"Pratos Principais: {pedido[2]}\n")
            self.texto_pedidos.insert("end", f"Guarnições: {pedido[3]}\n")
            self.texto_pedidos.insert("end", f"Bebidas: {pedido[4]}\n")
            self.texto_pedidos.insert("end", f"Economia do Dia: {pedido[5]}\n")
            self.texto_pedidos.insert("end", f"Principal: {pedido[6]}\n")
            self.texto_pedidos.insert(
                "end", f"Modo de Pagamento: {pedido[7]}\n")
            self.texto_pedidos.insert("end", f"Endereço: {pedido[8]}\n")
            self.texto_pedidos.insert("end", f"Observações: {pedido[9]}\n")
            self.texto_pedidos.insert("end", f"Troco: {pedido[10]}\n")
            self.texto_pedidos.insert("end", f"Total: R$ {pedido[11]:.2f}\n")
            self.texto_pedidos.insert("end", "-" * 50 + "\n")

    def buscar_pedido(self):
        # Verificar se a janela de pedidos ainda está aberta
        if not hasattr(self, 'janela_pedidos') or not self.janela_pedidos.winfo_exists():
            messagebox.showwarning("Erro", "A janela de pedidos foi fechada.")
            return

        # Obter o número do pedido
        numero_pedido = self.entry_busca.get().strip()
        if not numero_pedido:
            messagebox.showwarning("Busca", "Informe o número do pedido.")
            return

        # Buscar o pedido no banco de dados
        pedido = buscar_pedido_por_numero(numero_pedido)
        if pedido:
            self.exibir_pedidos([pedido])
        else:
            messagebox.showinfo(
                "Busca", f"Nenhum pedido encontrado com o número {numero_pedido}.")


if __name__ == "__main__":
    root = ctk.CTk()
    app = PedidoApp(root)
    root.mainloop()
