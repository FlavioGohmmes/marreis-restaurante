import customtkinter as ctk
from tkinter import messagebox
from models.pedido import Pedido
from utils.pdf_generator import gerar_pdf
import os

# Configuração do tema do customtkinter
ctk.set_appearance_mode("dark")  # Modo de aparência (System, Light, Dark)
ctk.set_default_color_theme("blue")  # Tema de cores (blue, green, dark-blue)

class PedidoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marreis Restaurante - Gerador de Pedidos")
        self.root.state("zoomed")  # Abre em tela cheia
        self.root.minsize(800, 600)  # Tamanho mínimo da janela

        # Configuração do grid para responsividade
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.pedidos = []  # Lista para armazenar múltiplos pedidos
        self.num_pedidos = 1  # Número inicial de pedidos

        self.criar_interface()

    def criar_interface(self):
        # Frame principal com barra de rolagem
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#2E2E2E")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Canvas para a barra de rolagem
        self.canvas = ctk.CTkCanvas(self.main_frame, bg="#2E2E2E", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Barra de rolagem vertical
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

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
        titulo = ctk.CTkLabel(self.inner_frame, text="Marreis Restaurante", font=("Helvetica", 24, "bold"), text_color="#FFFFFF")
        titulo.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        # Frame para seleção do número de pedidos
        frame_num_pedidos = ctk.CTkFrame(self.inner_frame, fg_color="#3E3E3E")
        frame_num_pedidos.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame_num_pedidos, text="Número de Pedidos", font=("Helvetica", 16), text_color="#FFFFFF").pack(pady=5)
        self.num_pedidos_var = ctk.IntVar(value=1)
        self.num_pedidos_menu = ctk.CTkOptionMenu(frame_num_pedidos, variable=self.num_pedidos_var, values=[str(i) for i in range(1, 6)], command=self.atualizar_pedidos)
        self.num_pedidos_menu.pack(pady=5)

        # Frame para os pedidos
        self.frame_pedidos = ctk.CTkFrame(self.inner_frame, fg_color="#2E2E2E")
        self.frame_pedidos.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Botão Finalizar Pedido
        btn_finalizar = ctk.CTkButton(self.inner_frame, text="Finalizar Pedido", command=self.finalizar_pedido, fg_color="#4CAF50", hover_color="#45a049")
        btn_finalizar.grid(row=3, column=0, columnspan=3, pady=20, sticky="nsew")

        # Configuração do redimensionamento
        self.root.bind("<Configure>", self.on_resize)

        # Inicializa os pedidos
        self.atualizar_pedidos()

    def on_mousewheel(self, event):
        # Rola a tela com o mouse
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def atualizar_pedidos(self, *args):
        # Remove os pedidos existentes
        for widget in self.frame_pedidos.winfo_children():
            widget.destroy()

        # Cria os novos pedidos
        self.num_pedidos = self.num_pedidos_var.get()
        self.pedidos = [Pedido() for _ in range(self.num_pedidos)]

        for i in range(self.num_pedidos):
            frame_pedido = ctk.CTkFrame(self.frame_pedidos, fg_color="#3E3E3E")
            frame_pedido.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(frame_pedido, text=f"Pedido {i + 1}", font=("Helvetica", 16), text_color="#FFFFFF").grid(row=0, column=0, columnspan=3, pady=5, sticky="nsew")

            # Frame para os pratos principais
            frame_pratos = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_pratos.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_pratos, text="Pratos Principais", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            pratos = ["Frango a Passarinho", "Linguiça", "Carne Moída com Batata", "Parmegiana de Frango", "Carne de Panela", "Bife de Pernil"]
            for prato in pratos:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(frame_pratos, text=prato, variable=var, command=lambda p=prato, v=var, idx=i: self.adicionar_prato(p, v, idx), fg_color="#4CAF50", hover_color="#45a049")
                cb.pack(pady=2, anchor="w")
                self.pedidos[i].pratos_vars[prato] = var

            # Frame para as guarnições
            frame_guarnicoes = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_guarnicoes.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_guarnicoes, text="Guarnições", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            guarnicoes = ["Arroz", "Feijão", "Macarrão", "Quibebe", "Farofa", "Batata Frita", "Legumes Refogados"]
            for guarnicao in guarnicoes:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(frame_guarnicoes, text=guarnicao, variable=var, command=lambda g=guarnicao, v=var, idx=i: self.adicionar_guarnicao(g, v, idx), fg_color="#4CAF50", hover_color="#45a049")
                cb.pack(pady=2, anchor="w")
                self.pedidos[i].guarn_vars[guarnicao] = var

            # Frame para as bebidas
            frame_bebidas = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_bebidas.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_bebidas, text="Bebidas", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            bebidas = {"Água": 4, "Refrigerante": 6, "Suco": 10}
            for bebida, valor in bebidas.items():
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(frame_bebidas, text=f"{bebida} (R$ {valor:.2f})", variable=var, command=lambda b=bebida, v=var, val=valor, idx=i: self.adicionar_bebida(b, v, val, idx), fg_color="#4CAF50", hover_color="#45a049")
                cb.pack(pady=2, anchor="w")
                self.pedidos[i].bebidas_vars[bebida] = var

            # Frame para a "Economia do Dia"
            frame_economia_dia = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_economia_dia.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_economia_dia, text="Economia do Dia", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            self.pedidos[i].economia_dia_var = ctk.StringVar(value="Nenhum")
            rb_economia_p = ctk.CTkRadioButton(frame_economia_dia, text="P - R$ 12,00", variable=self.pedidos[i].economia_dia_var, value="P", command=lambda idx=i: self.adicionar_economia_dia("P", idx))
            rb_economia_p.pack(pady=2, anchor="w")
            rb_economia_m = ctk.CTkRadioButton(frame_economia_dia, text="M - R$ 18,00", variable=self.pedidos[i].economia_dia_var, value="M", command=lambda idx=i: self.adicionar_economia_dia("M", idx))
            rb_economia_m.pack(pady=2, anchor="w")

            # Frame para o "Principal"
            frame_principal = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_principal.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_principal, text="Principal", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            self.pedidos[i].principal_var = ctk.StringVar(value="Nenhum")
            rb_principal_p = ctk.CTkRadioButton(frame_principal, text="P - R$ 18,00", variable=self.pedidos[i].principal_var, value="P", command=lambda idx=i: self.adicionar_principal("P", idx))
            rb_principal_p.pack(pady=2, anchor="w")
            rb_principal_m = ctk.CTkRadioButton(frame_principal, text="M - R$ 20,00", variable=self.pedidos[i].principal_var, value="M", command=lambda idx=i: self.adicionar_principal("M", idx))
            rb_principal_m.pack(pady=2, anchor="w")

            # Frame para o modo de pagamento
            frame_pagamento = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_pagamento.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_pagamento, text="Modo de Pagamento", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            pagamentos = ["Pix", "Débito", "Crédito", "Dinheiro"]
            for pagamento in pagamentos:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(frame_pagamento, text=pagamento, variable=var, command=lambda p=pagamento, v=var, idx=i: self.adicionar_pagamento(p, v, idx), fg_color="#4CAF50", hover_color="#45a049")
                cb.pack(side="left", padx=5, pady=2, anchor="w")
                self.pedidos[i].pagamentos_vars[pagamento] = var

                # Adiciona campo de texto para o troco se o pagamento for em dinheiro
                if pagamento == "Dinheiro":
                    self.pedidos[i].troco_entry = ctk.CTkEntry(frame_pagamento, placeholder_text="Troco para quanto?", fg_color="#FFFFFF", text_color="#000000")
                    self.pedidos[i].troco_entry.pack(side="left", padx=5, pady=5, anchor="w")

            # Frame para endereço e observações
            frame_endereco_obs = ctk.CTkFrame(frame_pedido, fg_color="#4E4E4E")
            frame_endereco_obs.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

            ctk.CTkLabel(frame_endereco_obs, text="Endereço", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            self.pedidos[i].endereco_entry = ctk.CTkEntry(frame_endereco_obs, placeholder_text="Digite seu endereço", fg_color="#FFFFFF", text_color="#000000")
            self.pedidos[i].endereco_entry.pack(pady=5, fill="x")

            ctk.CTkLabel(frame_endereco_obs, text="Observações", font=("Helvetica", 14), text_color="#FFFFFF").pack(pady=5)
            self.pedidos[i].observacoes_entry = ctk.CTkEntry(frame_endereco_obs, placeholder_text="Alguma observação?", fg_color="#FFFFFF", text_color="#000000")
            self.pedidos[i].observacoes_entry.pack(pady=5, fill="x")

    def on_resize(self, event):
        # Ajusta o tamanho do canvas ao redimensionar a janela
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def adicionar_prato(self, prato, var, idx):
        if var.get():
            self.pedidos[idx].adicionar_prato(prato)
        else:
            self.pedidos[idx].remover_prato(prato)

    def adicionar_guarnicao(self, guarnicao, var, idx):
        if var.get():
            self.pedidos[idx].adicionar_guarnicao(guarnicao)
        else:
            self.pedidos[idx].remover_guarnicao(guarnicao)

    def adicionar_bebida(self, bebida, var, valor, idx):
        if var.get():
            self.pedidos[idx].adicionar_bebida(bebida, valor)
        else:
            self.pedidos[idx].remover_bebida(bebida)

    def adicionar_economia_dia(self, tamanho, idx):
        self.pedidos[idx].adicionar_economia_dia(tamanho)

    def adicionar_principal(self, tamanho, idx):
        self.pedidos[idx].adicionar_principal(tamanho)

    def adicionar_pagamento(self, pagamento, var, idx):
        if var.get():
            self.pedidos[idx].adicionar_pagamento(pagamento)
        else:
            self.pedidos[idx].remover_pagamento(pagamento)

    def finalizar_pedido(self):
        for i, pedido in enumerate(self.pedidos):
            if not pedido.pratos_principais:
                messagebox.showwarning("Aviso", f"Selecione pelo menos um prato principal no Pedido {i + 1}.")
                return

            pedido.endereco = pedido.endereco_entry.get()
            pedido.observacoes = pedido.observacoes_entry.get()

            # Verifica se o pagamento é em dinheiro e se o campo de troco foi preenchido
            if "Dinheiro" in pedido.pagamentos and not pedido.troco_entry.get():
                messagebox.showwarning("Aviso", f"Informe o valor do troco para pagamento em dinheiro no Pedido {i + 1}.")
                return
            pedido.troco = pedido.troco_entry.get() if "Dinheiro" in pedido.pagamentos else ""

        confirmar = messagebox.askyesno("Confirmar", "Deseja finalizar a comanda?")
        if confirmar:
            gerar_pdf(self.pedidos)
            messagebox.showinfo("Sucesso", "Comanda finalizada e PDF gerado com sucesso!")
            os.startfile("pedido.pdf")
            self.limpar_campos()

    def limpar_campos(self):
        # Limpa todos os pedidos
        for pedido in self.pedidos:
            pedido.limpar_campos()

        # Atualiza a interface para refletir a limpeza
        self.atualizar_pedidos()

if __name__ == "__main__":
    root = ctk.CTk()
    app = PedidoApp(root)
    root.mainloop()