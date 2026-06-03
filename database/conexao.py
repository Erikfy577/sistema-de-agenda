import sqlite3
import os

def inicializar_banco():
    # Como o script já está na pasta database, pegamos o diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "banco.db")

    try:
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        # Criação da tabela com as colunas atualizadas (incluindo prioridade)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                profissional TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aguardando',
                prioridade TEXT NOT NULL DEFAULT 'Eletivo'
            )
        """)
        
        conexao.commit()
        print("✅ Banco de dados estruturado com sucesso!")
        print("Estrutura: id | nome | telefone | profissional | status | prioridade")
        
    except Exception as e:
        print(f"❌ Erro ao estruturar o banco: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    inicializar_banco()