# src/main.py
from views.interface import PedidoApp
import customtkinter as ctk
from utils.database import criar_banco_dados

if __name__ == "__main__":
    # Criar o banco de dados ao iniciar o aplicativo
    criar_banco_dados()

    root = ctk.CTk()
    app = PedidoApp(root)
    root.mainloop()