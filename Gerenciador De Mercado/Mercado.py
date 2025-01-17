import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import datetime
import os

def carregar_configuracoes():
    """Carrega as configurações do arquivo .env."""
    load_dotenv()
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')
    return host, port, user, password, database

def conectar_mysql(host, port, user, password, database):
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        conexao = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        if conexao.is_connected():
            print("Conexão ao MySQL estabelecida com sucesso.")
        return conexao
    except Error as e:
        print(f"Erro ao conectar no MySQL: {e}")
        return None

def criar_banco_e_tabelas(conexao, database):
    """Cria o banco de dados e as tabelas necessárias."""
    try:
        cursor = conexao.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        cursor.execute(f"USE {database};")

        # Tabela de Funcionários
        tabela_funcionarios = """
        CREATE TABLE IF NOT EXISTS Funcionarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(50),
            salario DECIMAL(10, 2),
            data_contratacao DATE
        );
        """
        cursor.execute(tabela_funcionarios)

        # Tabela de Produtos
        tabela_produtos = """
        CREATE TABLE IF NOT EXISTS Produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            preco DECIMAL(10, 2) NOT NULL,
            quantidade INT DEFAULT 0,
            categoria VARCHAR(50)
        );
        """
        cursor.execute(tabela_produtos)

        print("Banco de dados e tabelas criados/verificados com sucesso.")
    except Error as e:
        print(f"Erro ao criar banco ou tabelas: {e}")

def cadastrar_funcionario(conexao):
    """Cadastrar um novo funcionário no banco de dados."""
    nome = input("Digite o nome do funcionário: ")
    cargo = input("Digite o cargo do funcionário: ")
    salario = float(input("Digite o salário do funcionário: "))
    data_contratacao = datetime.now().date()  # Data automática

    try:
        cursor = conexao.cursor()
        query = "INSERT INTO Funcionarios (nome, cargo, salario, data_contratacao) VALUES (%s, %s, %s, %s)"
        valores = (nome, cargo, salario, data_contratacao)
        cursor.execute(query, valores)
        conexao.commit()
        print(f"Funcionário {nome} cadastrado com sucesso!")
    except Error as e:
        print(f"Erro ao cadastrar funcionário: {e}")

def cadastrar_produto(conexao):
    """Cadastrar um novo produto no banco de dados."""
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    categoria = input("Digite a categoria do produto: ")

    try:
        cursor = conexao.cursor()
        query = "INSERT INTO Produtos (nome, preco, quantidade, categoria) VALUES (%s, %s, %s, %s)"
        valores = (nome, preco, quantidade, categoria)
        cursor.execute(query, valores)
        conexao.commit()
        print(f"Produto {nome} cadastrado com sucesso!")
    except Error as e:
        print(f"Erro ao cadastrar produto: {e}")

def alterar_dados(conexao, tabela):
    """Alterar dados de um registro existente."""
    id_registro = int(input(f"Digite o ID do registro na tabela {tabela}: "))
    coluna = input(f"Digite o nome da coluna que deseja alterar na tabela {tabela}: ")
    novo_valor = input(f"Digite o novo valor para a coluna {coluna}: ")

    try:
        cursor = conexao.cursor()
        query = f"UPDATE {tabela} SET {coluna} = %s WHERE id = %s"
        cursor.execute(query, (novo_valor, id_registro))
        conexao.commit()
        print(f"Registro {id_registro} atualizado com sucesso!")
    except Error as e:
        print(f"Erro ao alterar dados: {e}")

def atualizar_estoque(conexao):
    """Atualizar a quantidade de um produto no estoque."""
    id_produto = int(input("Digite o ID do produto: "))
    nova_quantidade = int(input("Digite a nova quantidade do produto: "))

    try:
        cursor = conexao.cursor()
        query = "UPDATE Produtos SET quantidade = %s WHERE id = %s"
        cursor.execute(query, (nova_quantidade, id_produto))
        conexao.commit()
        print(f"Estoque do produto {id_produto} atualizado para {nova_quantidade}.")
    except Error as e:
        print(f"Erro ao atualizar estoque: {e}")

def excluir_registro(conexao, tabela):
    """Excluir um registro de uma tabela."""
    id_registro = int(input(f"Digite o ID do registro na tabela {tabela} que deseja excluir: "))

    try:
        cursor = conexao.cursor()
        query = f"DELETE FROM {tabela} WHERE id = %s"
        cursor.execute(query, (id_registro,))
        conexao.commit()
        print(f"Registro {id_registro} excluído com sucesso da tabela {tabela}.")
    except Error as e:
        print(f"Erro ao excluir registro: {e}")

def gerar_relatorios(conexao):
    """Gerar relatórios detalhados de funcionários e produtos."""
    print("1. Relatório de Funcionários")
    print("2. Relatório de Produtos")
    escolha = input("Escolha o tipo de relatório: ")

    try:
        cursor = conexao.cursor()
        if escolha == '1':
            query = "SELECT * FROM Funcionarios"
            cursor.execute(query)
            resultados = cursor.fetchall()
            print("\n=== Relatório de Funcionários ===")
            for funcionario in resultados:
                print(funcionario)
        elif escolha == '2':
            query = "SELECT * FROM Produtos"
            cursor.execute(query)
            resultados = cursor.fetchall()
            print("\n=== Produtos em Estoque ===")
            for produto in resultados:
                print(produto)
        else:
            print("Opção inválida.")
    except Error as e:
        print(f"Erro ao gerar relatório: {e}")

def consultar_produtos(conexao):
    """Consultar produtos no banco de dados."""
    categoria = input("Digite a categoria para consultar ou deixe em branco para consultar todos: ")

    try:
        cursor = conexao.cursor()
        if categoria:
            query = "SELECT * FROM Produtos WHERE categoria = %s"
            cursor.execute(query, (categoria,))
        else:
            query = "SELECT * FROM Produtos"
            cursor.execute(query)

        resultados = cursor.fetchall()
        print("\n=== Produtos ===")
        for produto in resultados:
            print(produto)
    except Error as e:
        print(f"Erro ao consultar produtos: {e}")

def menu_principal(conexao):
    """Exibe o menu principal para interação com o usuário."""
    while True:
        print("\n=== SISTEMA DE GESTÃO DO MERCADO ===")
        print("1. Cadastrar Funcionário ou Produto")
        print("2. Alterar Dados")
        print("3. Atualizar Estoque")
        print("4. Excluir Registro")
        print("5. Gerar Relatórios")
        print("6. Consultar Produtos")
        print("7. Sair")

        escolha = input("Escolha uma opção: ")
        if escolha == '7':
            print("Saindo do sistema... Até mais!")
            break
        elif escolha == '1':
            print("Escolha a opção para cadastrar:")
            print("1. Cadastrar Funcionário")
            print("2. Cadastrar Produto")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                cadastrar_funcionario(conexao)
            elif opcao == '2':
                cadastrar_produto(conexao)
            else:
                print("Opção inválida. Tente novamente.")
        elif escolha == '2':
            tabela = input("Digite a tabela para alterar (Funcionarios ou Produtos): ")
            alterar_dados(conexao, tabela)
        elif escolha == '3':
            atualizar_estoque(conexao)
        elif escolha == '4':
            tabela = input("Digite a tabela para excluir registros (Funcionarios ou Produtos): ")
            excluir_registro(conexao, tabela)
        elif escolha == '5':
            gerar_relatorios(conexao)
        elif escolha == '6':
            consultar_produtos(conexao)
        else:
            print(f"Opção {escolha} inválida. Tente novamente.")

if __name__ == "__main__":
    # Carregar configurações do arquivo .env
    host, port, user, password, database = carregar_configuracoes()

    # Conectar ao MySQL
    conexao = conectar_mysql(host, port, user, password, database)

    if conexao:
        # Criar banco e tabelas
        criar_banco_e_tabelas(conexao, database)

        # Exibir menu principal
        menu_principal(conexao)

        # Fechar conexão
        conexao.close()