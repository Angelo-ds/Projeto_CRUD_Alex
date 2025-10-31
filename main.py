import ttkbootstrap as ttk                 # Biblioteca para tema moderno no Tkinter
from ttkbootstrap.constants import *       # Importa constantes (ex: LEFT, RIGHT, END)
from ttkbootstrap.widgets import DateEntry # Importa DateEntry
from tkinter import messagebox             # Para exibir alertas e mensagens
from datetime import date                  # Para trabalhar com datas corretamente
import database as db                      # Importa o módulo de banco de dados


# Classe principal da aplicação
class Projetos(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")     # Define o tema visual 
        self.title("Gerenciador de Projetos Freelancer")  # Título da janela
        self.geometry("950x600")                 # Define tamanho fixo da janela
        self.resizable(False, False)             # Impede redimensionamento

        self.id_projeto = None                   # Guarda o ID do projeto selecionado
        self.criar_botoes()                      # Cria todos os elementos da interface
        self.carregar_projetos()                 # Carrega os projetos do banco
        self.atualizar_clientes()                # Preenche o combobox com os clientes

    # Cria todos os widgets da interface
    def criar_botoes(self):
        # ======== FORMULÁRIO DE CADASTRO ========
        form_frame = ttk.Frame(self, padding=10)
        form_frame.pack(fill=X)

        ttk.Label(form_frame, text="Nome do Projeto:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Cliente:").grid(row=0, column=2, padx=5, pady=5)
        self.cliente_entry = ttk.Entry(form_frame)
        self.cliente_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Prazo Entrega:").grid(row=1, column=0, padx=5, pady=5)
        # Usa DateEntry em vez de Entry
        self.prazo_entry = DateEntry(
            form_frame,
            dateformat="%d/%m/%Y",
            bootstyle="info"
        )
        self.prazo_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Valor:").grid(row=1, column=2, padx=5, pady=5)
        self.valor_entry = ttk.Entry(form_frame)
        self.valor_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(
            form_frame,
            values=["Proposta", "Em Andamento", "Concluído"],
            state="readonly"
        )
        self.status_combo.current(0)
        self.status_combo.grid(row=2, column=1, padx=5, pady=5)

        # ======== BOTÕES DE AÇÃO ========
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=X, pady=5)
        
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Atualizar", command=self.atualizar, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos, bootstyle=SECONDARY).pack(side=LEFT, padx=5)

        # ======== LISTA DE PROJETOS (TREEVIEW) ========
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nome", "Cliente", "Prazo", "Valor", "Status"),
            show="headings"
        )
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Nome" else 200)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item)

        # ======== TOTALIZADOR POR CLIENTE ========
        total_frame = ttk.Labelframe(self, text="Totalizador por Cliente", padding=10)
        total_frame.pack(fill=X, padx=10, pady=5)

        self.cliente_combo = ttk.Combobox(total_frame, state="readonly")
        self.cliente_combo.pack(side=LEFT, padx=5)

        ttk.Button(total_frame, text="Calcular Total", command=self.calcular_total, bootstyle=PRIMARY).pack(side=LEFT, padx=5)
        self.label_total = ttk.Label(total_frame, text="Total: R$ 0.00", font=("Helvetica", 12, "bold"))
        self.label_total.pack(side=LEFT, padx=15)

    # === Função para adicionar um novo projeto ===
    def adicionar(self):
        if not self.nome_entry.get() or not self.cliente_entry.get():
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        prazo = self.prazo_entry.get_date()
        if not prazo:
            messagebox.showwarning("Atenção", "O campo de prazo é obrigatório.")
            return

        prazo_str = prazo.strftime("%d/%m/%Y")

        try:
            db.inserir_projeto(
                self.nome_entry.get(),
                self.cliente_entry.get(),
                prazo_str,
                float(self.valor_entry.get() or 0),
                self.status_combo.get()
            )
            messagebox.showinfo("Sucesso", "Projeto adicionado com sucesso!")
            self.carregar_projetos()
            self.limpar_campos()
            self.atualizar_clientes()  # Atualiza combobox de clientes automaticamente
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível adicionar o projeto:\n{erro}")

    # === Carrega todos os projetos do banco e mostra na tabela ===
    def carregar_projetos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for projeto in db.listar_projetos():
            id_, nome, cliente, prazo, valor, status = projeto
            self.tree.insert("", END, values=(id_, nome, cliente, prazo, f"{float(valor):.2f}", status))

    # === Preenche os campos ao clicar em um item da lista ===
    def selecionar_item(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado[0], "values")
        self.id_projeto = item[0]

        self.nome_entry.delete(0, END)
        self.cliente_entry.delete(0, END)
        self.valor_entry.delete(0, END)

        self.nome_entry.insert(0, item[1])
        self.cliente_entry.insert(0, item[2])

        # Corrigido: set_date com objeto datetime.date
        prazo_split = list(map(int, item[3].split("/")))
        data_prazo = date(prazo_split[2], prazo_split[1], prazo_split[0])
        self.prazo_entry.set_date(data_prazo)

        self.valor_entry.insert(0, item[4])
        self.status_combo.set(item[5])

    # === Atualiza os dados do projeto selecionado ===
    def atualizar(self):
        if not self.id_projeto:
            messagebox.showinfo("Info", "Selecione um projeto para atualizar.")
            return

        prazo = self.prazo_entry.get_date()
        prazo_str = prazo.strftime("%d/%m/%Y")

        db.atualizar_projeto(
            self.id_projeto,
            self.nome_entry.get(),
            self.cliente_entry.get(),
            prazo_str,
            float(self.valor_entry.get() or 0),
            self.status_combo.get()
        )
        self.carregar_projetos()
        self.limpar_campos()
        self.atualizar_clientes()

    # === Exclui o projeto selecionado ===
    def excluir(self):
        if not self.id_projeto:
            messagebox.showinfo("Info", "Selecione um projeto para excluir.")
            return
        db.excluir_projeto(self.id_projeto)
        self.carregar_projetos()
        self.limpar_campos()
        self.atualizar_clientes()

    # === Limpa os campos do formulário ===
    def limpar_campos(self):
        self.id_projeto = None
        self.nome_entry.delete(0, END)
        self.cliente_entry.delete(0, END)
        self.prazo_entry.entry.delete(0, END)  # Limpa o DateEntry manualmente
        self.valor_entry.delete(0, END)
        self.status_combo.current(0)

    # === Atualiza a lista de clientes no combobox ===
    def atualizar_clientes(self):
        clientes = db.clientes_unicos()
        self.cliente_combo["values"] = clientes
        if clientes:
            self.cliente_combo.current(0)

    # === Calcula o total de valores "Concluídos" do cliente selecionado ===
    def calcular_total(self):
        cliente = self.cliente_combo.get().strip()
        if not cliente:
            messagebox.showinfo("Info", "Selecione um cliente.")
            return
        total = db.total_por_cliente(cliente)
        self.label_total.config(
            text=f"Total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )


# Executa a aplicação
if __name__ == "__main__":
    projetos = Projetos()
    projetos.mainloop()
