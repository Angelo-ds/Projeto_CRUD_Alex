import ttkbootstrap as ttk                 # Biblioteca para tema moderno no Tkinter
from ttkbootstrap.constants import *       # Importa constantes (ex: LEFT, RIGHT, END)
from tkinter import messagebox             # Para exibir alertas e mensagens
import database as db                      # Importa o módulo de banco de dados

# Classe principal da aplicação
class Projetos(ttk.Window):
    def __init__(self):
        super().__init__(themename="cyborg")     # Define o tema visual 
        self.title("Gerenciador de Projetos Freelancer")  # Título da janela
        self.geometry("950x600")                 # Define tamanho fixo da janela
        self.resizable(False, False)             # Impede redimensionamento

        self.id_projeto = None                   # Guarda o ID do projeto selecionado
        self.criar_botoes()                    # Cria todos os elementos da interface
        self.carregar_projetos()                 # Carrega os projetos do banco
        self.atualizar_clientes()                # Preenche o combobox com os clientes

    # Cria todos os widgets da interface
    def criar_botoes(self):
        # ======== FORMULÁRIO DE CADASTRO ========
        form_frame = ttk.Frame(self, padding=10)
        form_frame.pack(fill=X)

        ttk.Label(form_frame, 
                  text="Nome do Projeto:").grid(row=0, 
                                                column=0, 
                                                padx=5, 
                                                pady=5)
        
        self.nome_entry = ttk.Entry(form_frame)

        self.nome_entry.grid(row=0, 
                             column=1, 
                             padx=5, 
                             pady=5)

        ttk.Label(form_frame, 
                  text="Cliente:").grid(row=0, 
                                        column=2, 
                                        padx=5, 
                                        pady=5)
        
        self.cliente_entry = ttk.Entry(form_frame)

        self.cliente_entry.grid(row=0, 
                                column=3, 
                                padx=5, 
                                pady=5)

        ttk.Label(form_frame, text="Prazo Entrega:").grid(row=1, 
                                                          column=0, 
                                                          padx=5, 
                                                          pady=5)
        
        self.prazo_entry = ttk.Entry(form_frame)
        self.prazo_entry.grid(row=1, 
                              column=1, 
                              padx=5, 
                              pady=5)

        ttk.Label(form_frame, text="Valor:").grid(row=1, 
                                                  column=2, 
                                                  padx=5, 
                                                  pady=5)
        
        self.valor_entry = ttk.Entry(form_frame)
        self.valor_entry.grid(row=1, 
                              column=3, 
                              padx=5, 
                              pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=2, 
                                                   column=0, 
                                                   padx=5, 
                                                   pady=5)
        # Combobox para escolher o status do projeto
        self.status_combo = ttk.Combobox(
            form_frame,
            values=["Proposta", "Em Andamento", "Concluído"],
            state="readonly"
        )
        self.status_combo.current(0)
        self.status_combo.grid(row=2, 
                               column=1, 
                               padx=5, 
                               pady=5)

        # ======== BOTÕES DE AÇÃO ========
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=X, pady=5)
        ttk.Button(btn_frame, 
                   text="Adicionar", 
                   command=self.adicionar, 
                   bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Atualizar", 
                   command=self.atualizar, 
                   bootstyle=INFO).pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Excluir", 
                   command=self.excluir, 
                   bootstyle=DANGER).pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Limpar",
                    command=self.limpar_campos, 
                    bootstyle=SECONDARY).pack(side=LEFT, padx=5)

        # ======== LISTA DE PROJETOS (TREEVIEW) ========
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nome", "Cliente", "Prazo", "Valor", "Status"),
            show="headings"
        )
        # Define cabeçalhos e larguras
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Nome" else 200)
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_item)  # Ao clicar em um item → carrega nos campos

