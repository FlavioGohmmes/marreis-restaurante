class Pedido:
    def __init__(self):
        self.pratos_principais = []
        self.guarnicoes = []
        self.bebidas = []
        self.economia_dia = {"tamanho": None, "valor": 0}
        self.principal = {"tamanho": None, "valor": 0}
        self.pagamentos = []
        self.endereco = ""
        self.observacoes = ""
        self.troco = ""
        self.pratos_vars = {}
        self.guarn_vars = {}
        self.bebidas_vars = {}
        self.economia_dia_var = None
        self.principal_var = None
        self.pagamentos_vars = {}
        self.endereco_entry = None
        self.observacoes_entry = None
        self.troco_entry = None

    def adicionar_prato(self, prato):
        if prato not in self.pratos_principais:
            self.pratos_principais.append(prato)

    def remover_prato(self, prato):
        if prato in self.pratos_principais:
            self.pratos_principais.remove(prato)

    def adicionar_guarnicao(self, guarnicao):
        if guarnicao not in self.guarnicoes:
            self.guarnicoes.append(guarnicao)

    def remover_guarnicao(self, guarnicao):
        if guarnicao in self.guarnicoes:
            self.guarnicoes.remove(guarnicao)

    def adicionar_bebida(self, bebida, valor):
        self.bebidas.append({"nome": bebida, "valor": valor})

    def remover_bebida(self, bebida):
        self.bebidas = [b for b in self.bebidas if b["nome"] != bebida]

    def adicionar_economia_dia(self, tamanho):
        self.economia_dia = {"tamanho": tamanho, "valor": 12 if tamanho == "P" else 18}

    def remover_economia_dia(self):
        self.economia_dia = {"tamanho": None, "valor": 0}

    def adicionar_principal(self, tamanho):
        self.principal = {"tamanho": tamanho, "valor": 18 if tamanho == "P" else 20}

    def remover_principal(self):
        self.principal = {"tamanho": None, "valor": 0}

    def adicionar_pagamento(self, pagamento):
        if pagamento not in self.pagamentos:
            self.pagamentos.append(pagamento)

    def remover_pagamento(self, pagamento):
        if pagamento in self.pagamentos:
            self.pagamentos.remove(pagamento)

    def calcular_total(self):
        total = 0
        for bebida in self.bebidas:
            total += bebida["valor"]
        total += self.economia_dia["valor"]
        total += self.principal["valor"]
        return total

    def limpar_campos(self):
        self.pratos_principais.clear()
        self.guarnicoes.clear()
        self.bebidas.clear()
        self.economia_dia = {"tamanho": None, "valor": 0}
        self.principal = {"tamanho": None, "valor": 0}
        self.pagamentos.clear()
        self.endereco = ""
        self.observacoes = ""
        self.troco = ""
        for var in self.pratos_vars.values():
            var.set(False)
        for var in self.guarn_vars.values():
            var.set(False)
        for var in self.bebidas_vars.values():
            var.set(False)
        if self.economia_dia_var:
            self.economia_dia_var.set(None)
        if self.principal_var:
            self.principal_var.set(None)
        for var in self.pagamentos_vars.values():
            var.set(False)
        if self.endereco_entry:
            self.endereco_entry.delete(0, "end")
        if self.observacoes_entry:
            self.observacoes_entry.delete(0, "end")
        if self.troco_entry:
            self.troco_entry.delete(0, "end")