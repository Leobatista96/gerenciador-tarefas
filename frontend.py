import customtkinter as ctk
import tkinter as tk
from tkinter import END, ttk
from tkinter import messagebox
from backend import BackEnd

# Classe principal da tela de cadastro de tarefas


class JanelaPrincipal(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.bd = BackEnd()

        self.geometry("700x500")
        self.resizable(False, False)
        self.title("Cadastro de Tarefas")

        self.frame_principal = ctk.CTkFrame(self, width=550, height=500)
        self.frame_principal.place(x=150, y=3)

        self.label_tarefa = ctk.CTkLabel(
            self.frame_principal, text='Digite uma tarefa: ', font=('Arial', 16))
        self.label_tarefa.place(x=20, y=10)

        self.entry_tarefa = ctk.CTkEntry(self.frame_principal, width=150, font=(
            'Arial', 16))
        self.entry_tarefa.place(x=150, y=10)

        self.label_data = ctk.CTkLabel(
            self.frame_principal, text='Digite a data: ', font=('Arial', 16))
        self.label_data.place(x=20, y=50)

        self.entry_data = ctk.CTkEntry(self.frame_principal, width=150, font=(
            'Arial', 16))
        self.entry_data.place(x=150, y=50)

        self.lista_tarefas = ttk.Treeview(
            self.frame_principal, columns=['ID', 'Tarefa', 'Data'], show='headings', selectmode='browse')
        self.lista_tarefas.place(x=20, y=200)

        self.barra_rolagem = ctk.CTkScrollbar(self.lista_tarefas,
                                              orientation='vertical', command=self.lista_tarefas.yview, fg_color='white', button_color='black')
        self.barra_rolagem.place(x=485, y=25)

        self.lista_tarefas.configure(yscrollcommand=self.barra_rolagem.set)

        self.lista_tarefas.heading('Tarefa', text='Tarefa')
        self.lista_tarefas.heading('Data', text='Data')
        self.lista_tarefas.heading('ID', text='ID')

        self.lista_tarefas.column(
            'Tarefa', minwidth=0, width=350)
        self.lista_tarefas.column('Data', minwidth=0, width=100)
        self.lista_tarefas.column('ID', minwidth=0, width=50)

        self.botao_cadastrar_tarefas = ctk.CTkButton(
            self.frame_principal, text="Cadastrar Tarefa", command=self.cadastrar_produtos)
        self.botao_cadastrar_tarefas.place(x=100, y=150)

        self.botao_excluir_tarefas = ctk.CTkButton(
            self.frame_principal, text="Excluir Tarefa", command=(self.excluir_tarefas), fg_color='#FF0000', hover_color='#B22222')
        self.botao_excluir_tarefas.place(x=250, y=150)

        self.carregar_dados_tarefas()

    def cadastrar_produtos(self):
        self.tarefa = self.entry_tarefa.get()
        self.data = self.entry_data.get()

        if self.tarefa == '' or self.data == '':
            messagebox.showerror(
                title='Erro', message='Por favor, preencha todos os campos')
        else:
            self.bd.inserir_dados_tarefas(self.tarefa, self.data)
            self.id = self.bd.selecionar_dados()
            for registro in self.id:
                self.iid = registro[0]
            self.lista_tarefas.insert(
                '', 'end', values=(self.iid, self.tarefa, self.data))
            self.limpar_campos()

    def carregar_dados_tarefas(self):
        self.registros_retornados = self.bd.selecionar_dados()
        for registro in self.registros_retornados:
            self.id = registro[0]
            self.tarefa = registro[1]
            self.data = registro[2]
            self.lista_tarefas.insert(
                '', 'end', values=(self.id, self.tarefa, self.data))

    def excluir_tarefas(self):
        try:
            self.item_selecionado = self.lista_tarefas.selection()[0]
            self.valores_item_selecionado = self.lista_tarefas.item(
                self.item_selecionado, 'values')
            self.tarefa_selecionada = int(self.valores_item_selecionado[0])
            self.bd.excluir_dados(self.tarefa_selecionada)
            self.lista_tarefas.delete(self.item_selecionado)
        except:
            messagebox.showinfo(
                title="Erro", message="Selecione um registro para ser deletado")

    def limpar_campos(self):
        self.entry_tarefa.delete(0, END)
        self.entry_data.delete(0, END)

 # Classe principal da tela de login


class Login(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title("Tela de Login")
        self.resizable(False, False)
        self.tema = ctk.set_appearance_mode("dark")
        self.cor_tema = ctk.set_default_color_theme("dark-blue")
        self.criar_tabela()
        self.tela_login()
        self.toplevel_window = None

    def tela_login(self):
        # Frame do formulário de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=50, y=40)

        self.lbl_login = ctk.CTkLabel(
            self.frame_login, text="Faça seu Login", font=('Arial', 22))
        self.lbl_login.grid(row=0, column=0, pady=10, padx=10)

        # Campos com Labels e entrys do formulário de login
        self.login_login = ctk.CTkEntry(
            self.frame_login, placeholder_text="Digite seu nome de Usuário", width=300, font=('Roboto', 14))
        self.login_login.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login = ctk.CTkEntry(
            self.frame_login, placeholder_text="Digite sua Senha", width=300, font=('Roboto', 14), show="*")
        self.senha_login.grid(row=3, column=0, padx=10, pady=10)

        self.botao_login = ctk.CTkButton(self.frame_login, text="Fazer Login", width=300, font=(
            'Roboto', 16), fg_color="Blue", hover_color="#005", command=self.verificar_login)
        self.botao_login.grid(row=5, column=0, padx=10, pady=10)

        self.label_cadastrar = ctk.CTkLabel(
            self.frame_login, text="Caso não tenha cadastro,\n clique no botão abaixo", font=('Roboto', 12))
        self.label_cadastrar.grid(row=6, column=0, padx=10, pady=10)

        self.botao_cadastrar = ctk.CTkButton(self.frame_login, text="Fazer Cadastro", width=300, font=(
            'Roboto', 16), fg_color="Green", hover_color="#050", command=self.tela_cadastro)
        self.botao_cadastrar.grid(row=7, column=0, padx=10, pady=10)

    def tela_cadastro(self):
        # remover o fomrmulário de login
        self.frame_login.place_forget()

        # frame do formulário de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=50, y=40)

        # widgets no formulário de cadastro
        self.lbl_cadastro = ctk.CTkLabel(
            self.frame_cadastro, text="Faça seu Cadastro", font=('Arial', 22))
        self.lbl_cadastro.grid(row=0, column=0, padx=10, pady=5)

        self.cadastro_usuario = ctk.CTkEntry(
            self.frame_cadastro, placeholder_text="Digite seu usuario", width=300, font=('Roboto', 14))
        self.cadastro_usuario.grid(row=1, column=0, padx=10, pady=5)

        self.cadastro_email = ctk.CTkEntry(
            self.frame_cadastro, placeholder_text="Digite seu e-mail", width=300, font=('Roboto', 14))
        self.cadastro_email.grid(row=2, column=0, padx=10, pady=5)

        self.cadastro_senha = ctk.CTkEntry(
            self.frame_cadastro, placeholder_text="Digite sua senha", width=300, font=('Roboto', 14), show="*")
        self.cadastro_senha.grid(row=3, column=0, padx=10, pady=5)

        self.confirma_senha = ctk.CTkEntry(
            self.frame_cadastro, placeholder_text="Confirme sua Senha", width=300, font=('Roboto', 14), show="*")
        self.confirma_senha.grid(row=4, column=0, padx=10, pady=5)

        self.botao_tela_cadastro = ctk.CTkButton(self.frame_cadastro, text="Fazer Cadastro", width=300, font=(
            'Roboto', 16), fg_color="Green", hover_color="#050", command=self.cadastrar_usuario)
        self.botao_tela_cadastro.grid(row=5, column=0, padx=10, pady=5)

        self.botao_voltar_cadastro = ctk.CTkButton(
            self.frame_cadastro, text="Voltar", width=300, font=('Roboto', 16), command=self.tela_login)
        self.botao_voltar_cadastro.grid(row=6, column=0, padx=10, pady=5)

    def open_toplevel(self):
        self.withdraw()
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = JanelaPrincipal()

    # Limpeza dos campos do formulário de cadastro

    def limpar_campos_cadastro(self):
        self.cadastro_usuario.focus()
        self.cadastro_usuario.delete(0, END)
        self.cadastro_email.delete(0, END)
        self.cadastro_senha.delete(0, END)
        self.confirma_senha.delete(0, END)

    # limpeza dos campos de login
    def limpar_campos_login(self):
        self.login_login.delete(0, END)
        self.senha_login.delete(0, END)


if __name__ == "__main__":
    # tela_login = Login()
    # tela_login.mainloop()
    janela_principal = JanelaPrincipal()
    janela_principal.mainloop()
