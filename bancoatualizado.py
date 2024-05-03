import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class SistemaBancario:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancário")

        # Variáveis
        self.saldo = 0
        self.transacoes = []

        # Labels
        self.label_saldo = tk.Label(root, text="Saldo: R$0.00", font=("Arial", 12))
        self.label_saldo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Botões
        self.button_depositar = tk.Button(root, text="Depositar", command=self.depositar)
        self.button_depositar.grid(row=1, column=0, padx=10, pady=5, sticky="we")

        self.button_sacar = tk.Button(root, text="Sacar", command=self.sacar)
        self.button_sacar.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        self.button_extrato = tk.Button(root, text="Visualizar Extrato", command=self.visualizar_extrato)
        self.button_extrato.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.button_listar_usuarios = tk.Button(root, text="Listar Usuários Cadastrados", command=self.listar_usuarios_cadastrados)
        self.button_listar_usuarios.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def depositar(self, valor=None):
        if valor is None:
            valor = float(simpledialog.askstring("Depositar", "Digite o valor a ser depositado:"))
        if valor > 0:
            data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.transacoes.append((data_hora, f"Depósito de R${valor:.2f}"))
            self.saldo += valor
            self.atualizar_saldo()
            messagebox.showinfo("Sucesso", f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Valor de depósito inválido!")

    def sacar(self, *, valor=None):
        if valor is None:
            valor = float(simpledialog.askstring("Sacar", "Digite o valor a ser sacado:"))
        if len([transacao for transacao in self.transacoes if "Saque" in transacao[1]]) < 3:
            if valor > 0 and valor <= 500 and valor <= self.saldo:
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                self.transacoes.append((data_hora, f"Saque de R${valor:.2f}"))
                self.saldo -= valor
                self.atualizar_saldo()
                messagebox.showinfo("Sucesso", f"Saque de R${valor:.2f} realizado com sucesso!")
            elif valor > self.saldo:
                messagebox.showerror("Erro", "Saldo insuficiente para realizar o saque!")
            else:
                messagebox.showerror("Erro", "Valor de saque inválido!")
        else:
            messagebox.showerror("Erro", "Limite de saques diários atingido!")

    def visualizar_extrato(self, *, usuario=None):
        extrato = "Extrato:\n"
        for transacao in sorted(self.transacoes, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S")):
            extrato += f"{transacao[1]} - Data: {transacao[0]}\n"
        extrato += f"Saldo atual: R${self.saldo:.2f}"
        messagebox.showinfo("Extrato", extrato)

    def atualizar_saldo(self):
        self.label_saldo.config(text=f"Saldo: R${self.saldo:.2f}")

    def listar_usuarios_cadastrados(self):
        lista_usuarios = ""
        for usuario in usuarios:
            lista_usuarios += f"Nome: {usuario.nome}\nCPF: {usuario.cpf}\n"
            for conta in contas:
                if conta.usuario == usuario:
                    lista_usuarios += f"Número da Conta: {conta.numero_conta}\n"
            lista_usuarios += "\n"
        messagebox.showinfo("Usuários Cadastrados", lista_usuarios)

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class ContaBancaria:
    numero_conta = 1

    def __init__(self, usuario):
        self.agencia = "0001"
        self.numero_conta = ContaBancaria.numero_conta
        ContaBancaria.numero_conta += 1
        self.usuario = usuario

def cadastrar_usuario():
    nome = simpledialog.askstring("Cadastrar Usuário", "Nome:")
    data_nascimento = simpledialog.askstring("Cadastrar Usuário", "Data de Nascimento (dd/mm/aaaa):")
    cpf = simpledialog.askstring("Cadastrar Usuário", "CPF:")
    endereco = simpledialog.askstring("Cadastrar Usuário", "Endereço (logradouro, numero, bairro, cidade/sigla estado):")
    novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
    usuarios.append(novo_usuario)

def cadastrar_conta():
    cpf_usuario = simpledialog.askstring("Cadastrar Conta Bancária", "CPF do Usuário:")
    valor_deposito = float(simpledialog.askstring("Cadastrar Conta Bancária", "Valor do Depósito Inicial:"))
    for usuario in usuarios:
        if usuario.cpf == cpf_usuario:
            nova_conta = ContaBancaria(usuario)
            sistema_bancario.depositar(valor_deposito)
            contas.append(nova_conta)
            messagebox.showinfo("Sucesso", f"Conta cadastrada com sucesso para {usuario.nome}!")

if __name__ == "__main__":
    root = tk.Tk()
    sistema_bancario = SistemaBancario(root)
    usuarios = []
    contas = []

    # Botões de cadastro
    button_cadastrar_usuario = tk.Button(root, text="Cadastrar Usuário", command=cadastrar_usuario)
    button_cadastrar_usuario.grid(row=4, column=0, padx=10, pady=5, sticky="we")

    button_cadastrar_conta = tk.Button(root, text="Cadastrar Conta Bancária", command=cadastrar_conta)
    button_cadastrar_conta.grid(row=4, column=1, padx=10, pady=5, sticky="we")

    root.mainloop()
