import sqlite3
import os

def inicializar_banco():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "banco.db")

    try:
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                profissional TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aguardando',
                prioridade TEXT NOT NULL DEFAULT 'Eletivo',
                data_consulta TEXT
            )
        """)
        
        conexao.commit()
        print("✅ Banco de dados estruturado com a coluna data_consulta!")
        
    except Exception as e:
        print(f"❌ Erro ao estruturar o banco: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    inicializar_banco()