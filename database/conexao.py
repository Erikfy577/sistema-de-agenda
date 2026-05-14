import sqlite3
import os

def criar_banco():
    # Pega a pasta atual (database) e cria o banco dentro dela
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "banco.db")
    
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            profissional TEXT NOT NULL,
            status TEXT DEFAULT 'Aguardando'
        )
    ''')

    conexao.commit()
    conexao.close()
    print(f"Banco de dados verificado/criado em: {caminho_banco}")

if __name__ == '__main__':
    criar_banco()