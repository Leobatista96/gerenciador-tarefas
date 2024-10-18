
import sqlite3 as sql3
from tkinter import *
from tkinter import messagebox

# Classe principal da lógica de cadastro e login


class BackEnd():
    # Função de Abertura de conexão com o BD
    def conexao_bd(self):
        self.conexao = sql3.connect("tarefas.db")
        self.cursor = self.conexao.cursor()
        print("Banco de dados conectado")

    # Função de fechamento da conexão com o BD
    def desconexao_db(self):
        self.cursor.close()
        self.conexao.close()
        print("Banco desconectado")

    # Criação das tabelas

    def criar_tabela(self):
        self.conexao_bd()
        self.query_tabela_usuario = """CREATE TABLE IF NOT EXISTS usuarios (Id INTEGER PRIMARY KEY AUTOINCREMENT, Usuario TEXT NOT NULL, Email TEXT NOT NULL, Senha TEXT NOT NULL, Confirma_Senha TEXT NOT NULL);"""

        self.query_tabela_tarefa = """CREATE TABLE IF NOT EXISTS tarefas (ID INTEGER PRIMARY KEY AUTOINCREMENT, Tarefa TEXT NOT NULL, Data TEXT NOT NULL);"""

        self.cursor.execute(self.query_tabela_usuario)
        self.cursor.execute(self.query_tabela_tarefa)
        self.conexao.commit()
        print("Tabela Criada com Sucesso")
        self.desconexao_db()

    # CRUD cadastro de usuários
    def cadastrar_usuario(self):
        self.pegar_informacoes_usuario = self.cadastro_usuario.get()
        self.pegar_informacoes_email = self.cadastro_email.get()
        self.pegar_informacoes_senha = self.cadastro_senha.get()
        self.pegar_informacoes_confirma_senha = self.confirma_senha.get()

        try:
            self.conexao_bd()

            # verificação se os campos foram preenchidos
            if self.pegar_informacoes_usuario == "" or self.pegar_informacoes_email == "" or self.pegar_informacoes_senha == "" or self.pegar_informacoes_confirma_senha == "":
                messagebox.showwarning(
                    title="Sistema de Cadastro", message="Por favor preencha todos os campos")

            elif (len(str(self.pegar_informacoes_usuario)) < 4):
                messagebox.showwarning(
                    title="Sistema de Cadastro", message="O nome de usuário deve ter pelo menos 4 caracteres")

            elif (len(str(self.pegar_informacoes_senha)) < 4):
                messagebox.showwarning(
                    title="Sistema de Cadastro", message="A senha deve conter pelo menos 4 caracteres")

            elif (self.pegar_informacoes_senha != self.pegar_informacoes_confirma_senha):
                messagebox.showerror(
                    title="Sistema de Cadastro", message="Senhas colocadas não são iguais!")

            else:
                self.cursor.execute("""
                                    INSERT INTO usuarios (Usuario, Email, Senha, Confirma_Senha) VALUES(?,?,?,?)""",
                                    (self.pegar_informacoes_usuario, self.pegar_informacoes_email, self.pegar_informacoes_senha, self.pegar_informacoes_confirma_senha))
                self.conexao.commit()
                messagebox.showinfo(title="Sistema de Cadastro", message=f"Parabéns, {
                                    self.pegar_informacoes_usuario}, seus dados foram cadastrados!")
                self.desconexao_db()
                self.limpar_campos_cadastro()

        except:
            messagebox.showerror(title="Sistema de Cadastro",
                                 message="Erro na gravação dos dados")
            self.desconexao_db()
            self.limpar_campos_cadastro()

    # Pega informações digitadas pelo usuários e faz verificações com Banco de Dados
    def verificar_login(self):

        self.pegar_informacoeslogin = self.login_login.get()
        self.pegar_informacoes_senhalogin = self.senha_login.get()
        self.conexao_bd()

        self.cursor.execute("""SELECT * FROM usuarios WHERE (Usuario = ? AND Senha = ?)""",
                            (self.pegar_informacoeslogin, self.pegar_informacoes_senhalogin))
        self.verificar_dados = self.cursor.fetchone()

        if self.pegar_informacoeslogin == "" or self.pegar_informacoes_senhalogin == "":
            messagebox.showwarning(
                title="Sistema de Cadastro", message="Por favor preencha todos os campos")

        elif self.verificar_dados is None:
            messagebox.showerror(title="Sistema de Login",
                                 message="Dados não encontrados!")
            self.desconexao_db()

        else:
            messagebox.showinfo(title="Sistema de Login",
                                message=f"Login feito com Sucesso")
            self.desconexao_db()
            self.limpar_campos_login()
            self.open_toplevel()

    def inserir_dados_tarefas(self, tarefa, data):
        try:
            self.conexao_bd()
            self.cursor.execute("""INSERT INTO tarefas (Tarefa, Data) VALUES(?,?)""", (
                tarefa, data))
            self.conexao.commit()
            self.desconexao_db()
            print("Dados inseridos na tabela Tarefas com sucesso")
        except (Exception, sql3.Error) as error:
            print("Erro na inserção dos dados na tabela Tarefas, ", error)
            self.desconexao_db()

    def selecionar_dados(self):
        try:
            self.conexao_bd()
            self.cursor.execute("""SELECT * FROM tarefas""")
            self.registros = self.cursor.fetchall()
        except (Exception, sql3.Error) as error:
            print("Erro na seleção dos dados na tabela Tarefas, ", error)
            self.desconexao_db()
        return self.registros

    def excluir_dados(self, id):
        try:
            self.conexao_bd()
            self.cursor.execute(
                f"""DELETE FROM tarefas WHERE ID = {id}""")
            self.conexao.commit()
            self.desconexao_db()
            print("Registro excluído com sucesso!")
        except (Exception, sql3.Error) as error:
            print("Erro na exclusão dos dados, ", error)
            self.desconexao_db()
