import sqlite3
from sqlite3 import Error
from datetime import datetime

# Criar conexão com o banco de dados
def criar_conexao():
    conn = None
    try:
        conn = sqlite3.connect('doacoes.db')
        print("Conexão com SQLite estabelecida!")
        return conn
    except Error as e:
        print(e)

    return conn

# Criar tabela de doações
def criar_tabela(conn):
    try:
        cursor = conn.cursor()
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
        print("Tabela 'doacoes' criada com sucesso!")
    except Error as e:
        print(e)

# Inserir nova doação
def inserir_doacao(conn, doacao):
    sql = """INSERT INTO doacoes(nome_doador, contato, tipo_doacao, quantidade, data)
             VALUES(?,?,?,?,?)"""
    cursor = conn.cursor()
    cursor.execute(sql, doacao)
    conn.commit()
    return cursor.lastrowid

# Listar todas as doações
def listar_doacoes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doacoes")
    return cursor.fetchall()

# Menu principal
def menu():
    print("\nSISTEMA DE DOAÇÕES PARA ONG")
    print("1. Cadastrar nova doação")
    print("2. Listar todas as doações")
    print("3. Sair")
    return input("Escolha uma opção: ")

# Programa principal
def main():
    conn = criar_conexao()
    if conn is not None:
        criar_tabela(conn)
    else:
        print("Erro! Não foi possível conectar ao banco de dados.")
        return

    while True:
        opcao = menu()

        if opcao == "1":
            print("\nNOVA DOAÇÃO")
            nome = input("Nome do doador: ")
            contato = input("Contato (telefone/email): ")
            tipo = input("Tipo de doação (alimento/roupa/dinheiro/etc): ")
            quantidade = float(input("Quantidade: "))
            data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            doacao = (nome, contato, tipo, quantidade, data)
            id_doacao = inserir_doacao(conn, doacao)
            print(f"Doação registrada com ID {id_doacao}!")

        elif opcao == "2":
            print("\nLISTA DE DOAÇÕES")
            doacoes = listar_doacoes(conn)
            for doacao in doacoes:
                print(f"ID: {doacao[0]}, Doador: {doacao[1]}, Contato: {doacao[2]}")
                print(f"Tipo: {doacao[3]}, Quantidade: {doacao[4]}, Data: {doacao[5]}")
                print("---")

        elif opcao == "3":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Tente novamente.")

    conn.close()

if __name__ == "__main__":
    main()
