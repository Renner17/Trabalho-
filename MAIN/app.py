import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def criar_banco():
    conexao = sqlite3.connect('marmitas.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            forma_pagamento TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Marmitas")
        self.root.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        # Labels e Entradas
        self.label_nome = tk.Label(self.root, text="Nome:")
        self.label_nome.grid(row=0, column=0, padx=10, pady=10)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10)

        self.label_telefone = tk.Label(self.root, text="Telefone:")
        self.label_telefone.grid(row=1, column=0, padx=10, pady=10)
        self.entry_telefone = tk.Entry(self.root)
        self.entry_telefone.grid(row=1, column=1, padx=10, pady=10)

        self.label_quantidade = tk.Label(self.root, text="Quantidade:")
        self.label_quantidade.grid(row=2, column=0, padx=10, pady=10)
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.grid(row=2, column=1, padx=10, pady=10)

        self.label_pagamento = tk.Label(self.root, text="Forma de Pagamento:")
        self.label_pagamento.grid(row=3, column=0, padx=10, pady=10)
        self.combo_pagamento = ttk.Combobox(self.root, values=["dinheiro", "cartão de crédito", "cartão de débito", "pix"])
        self.combo_pagamento.grid(row=3, column=1, padx=10, pady=10)

        # Botões
        self.btn_add = tk.Button(self.root, text="Adicionar", command=self.adicionar_registro)
        self.btn_add.grid(row=4, column=0, padx=10, pady=10)

        self.btn_edit = tk.Button(self.root, text="Editar", command=self.editar_registro)
        self.btn_edit.grid(row=4, column=1, padx=10, pady=10)

        self.btn_delete = tk.Button(self.root, text="Apagar", command=self.apagar_registro)
        self.btn_delete.grid(row=4, column=2, padx=10, pady=10)

        self.btn_total = tk.Button(self.root, text="Total Vendido", command=self.total_vendido)
        self.btn_total.grid(row=5, column=0, padx=10, pady=10)

        self.btn_arrecadado = tk.Button(self.root, text="Total Arrecadado", command=self.total_arrecadado)
        self.btn_arrecadado.grid(row=5, column=1, padx=10, pady=10)

        # Tabela
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nome", "Telefone", "Quantidade", "Pagamento"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Pagamento", text="Pagamento")
        self.tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        
        self.carregar_registros()

    def carregar_registros(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conexao = sqlite3.connect('marmitas.db')
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM registros")
        registros = cursor.fetchall()
        for registro in registros:
            self.tree.insert("", "end", values=registro)
        conexao.close()

    def adicionar_registro(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        quantidade = int(self.entry_quantidade.get())
        forma_pagamento = self.combo_pagamento.get()
        
        if nome and telefone and quantidade and forma_pagamento:
            conexao = sqlite3.connect('marmitas.db')
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO registros (nome, telefone, quantidade, forma_pagamento) VALUES (?, ?, ?, ?)", 
                           (nome, telefone, quantidade, forma_pagamento))
            conexao.commit()
            conexao.close()
            self.carregar_registros()
            messagebox.showinfo("Sucesso", "Registro adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def editar_registro(self):
        selected_item = self.tree.selection()[0]
        valores = self.tree.item(selected_item, "values")
        registro_id = valores[0]
        
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        quantidade = int(self.entry_quantidade.get())
        forma_pagamento = self.combo_pagamento.get()
        
        if nome and telefone and quantidade and forma_pagamento:
            conexao = sqlite3.connect('marmitas.db')
            cursor = conexao.cursor()
            cursor.execute("UPDATE registros SET nome=?, telefone=?, quantidade=?, forma_pagamento=? WHERE id=?", 
                           (nome, telefone, quantidade, forma_pagamento, registro_id))
            conexao.commit()
            conexao.close()
            self.carregar_registros()
            messagebox.showinfo("Sucesso", "Registro editado com sucesso!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def apagar_registro(self):
        selected_item = self.tree.selection()[0]
        valores = self.tree.item(selected_item, "values")
        registro_id = valores[0]
        
        conexao = sqlite3.connect('marmitas.db')
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM registros WHERE id=?", (registro_id,))
        conexao.commit()
        conexao.close()
        self.carregar_registros()
        messagebox.showinfo("Sucesso", "Registro apagado com sucesso!")

    def total_vendido(self):
        conexao = sqlite3.connect('marmitas.db')
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, quantidade FROM registros")
        registros = cursor.fetchall()
        conexao.close()
        
        mensagem = "Total de marmitas vendidas:\n"
        for nome, quantidade in registros:
            valor_total = quantidade * 15  # Valor de cada marmita é R$ 15,00
            mensagem += f"{nome}: {quantidade} marmitas, R$ {valor_total:.2f}\n"
        
        messagebox.showinfo("Total Vendido", mensagem)

    def total_arrecadado(self):
        conexao = sqlite3.connect('marmitas.db')
        cursor = conexao.cursor()
        cursor.execute("SELECT forma_pagamento, SUM(quantidade * 15) FROM registros GROUP BY forma_pagamento")
        totais = cursor.fetchall()
        conexao.close()
        
        mensagem = "Total arrecadado por forma de pagamento:\n"
        for forma, total in totais:
            mensagem += f"{forma.capitalize()}: R$ {total:.2f}\n"
        
        messagebox.showinfo("Total Arrecadado", mensagem)


if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    app = App(root)
    root.mainloop()