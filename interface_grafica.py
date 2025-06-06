import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class SistemaDoacoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Doações - ONG Solidária")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')

        # Conexão com o banco de dados
        self.conn = sqlite3.connect('doacoes.db')
        self.criar_tabela()

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))

        # Criar widgets
        self.criar_widgets()

    def criar_tabela(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS doacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_doador TEXT NOT NULL,
                contato TEXT,
                tipo_doacao TEXT NOT NULL,
                quantidade REAL NOT NULL,
                data TEXT NOT NULL
            );
            """)
            self.conn.commit()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {e}")

    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Cabeçalho
        header = ttk.Label(main_frame, text="Sistema de Gerenciamento de Doações", style='Header.TLabel')
        header.pack(pady=(0, 20))

        # Abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Aba de Cadastro
        cadastro_frame = ttk.Frame(self.notebook)
        self.notebook.add(cadastro_frame, text="Nova Doação")

        # Formulário de cadastro
        ttk.Label(cadastro_frame, text="Nome do Doador:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nome_entry = ttk.Entry(cadastro_frame, width=40)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(cadastro_frame, text="Contato:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.contato_entry = ttk.Entry(cadastro_frame, width=40)
        self.contato_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(cadastro_frame, text="Tipo de Doação:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.tipo_combobox = ttk.Combobox(cadastro_frame, values=["Alimentos", "Roupas", "Dinheiro", "Medicamentos", "Outros"])
        self.tipo_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(cadastro_frame, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.quantidade_entry = ttk.Entry(cadastro_frame, width=40)
        self.quantidade_entry.grid(row=3, column=1, padx=5, pady=5)

        cadastrar_btn = ttk.Button(cadastro_frame, text="Cadastrar Doação", command=self.cadastrar_doacao)
        cadastrar_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Aba de Consulta
        consulta_frame = ttk.Frame(self.notebook)
        self.notebook.add(consulta_frame, text="Consultar Doações")

        # Treeview para exibir as doações
        columns = ('id', 'nome', 'contato', 'tipo', 'quantidade', 'data')
        self.tree = ttk.Treeview(consulta_frame, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome do Doador')
        self.tree.heading('contato', text='Contato')
        self.tree.heading('tipo', text='Tipo')
        self.tree.heading('quantidade', text='Quantidade')
        self.tree.heading('data', text='Data')

        self.tree.column('id', width=50)
        self.tree.column('nome', width=150)
        self.tree.column('contato', width=100)
        self.tree.column('tipo', width=100)
        self.tree.column('quantidade', width=80)
        self.tree.column('data', width=120)

        scrollbar = ttk.Scrollbar(consulta_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        consulta_frame.grid_rowconfigure(0, weight=1)
        consulta_frame.grid_columnconfigure(0, weight=1)

        atualizar_btn = ttk.Button(consulta_frame, text="Atualizar Lista", command=self.carregar_doacoes)
        atualizar_btn.grid(row=1, column=0, pady=10)

        # Carregar doações inicialmente
        self.carregar_doacoes()

    def cadastrar_doacao(self):
        nome = self.nome_entry.get()
        contato = self.contato_entry.get()
        tipo = self.tipo_combobox.get()
        quantidade = self.quantidade_entry.get()

        if not nome or not tipo or not quantidade:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return

        try:
            quantidade = float(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número!")
            return

        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO doacoes(nome_doador, contato, tipo_doacao, quantidade, data)
                VALUES(?,?,?,?,?)
            """, (nome, contato, tipo, quantidade, data))
            self.conn.commit()

            messagebox.showinfo("Sucesso", "Doação cadastrada com sucesso!")
            self.limpar_campos()
            self.carregar_doacoes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar doação: {e}")

    def carregar_doacoes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM doacoes ORDER BY data DESC")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar doações: {e}")

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.contato_entry.delete(0, tk.END)
        self.tipo_combobox.set('')
        self.quantidade_entry.delete(0, tk.END)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaDoacoes(root)
    root.mainloop()
