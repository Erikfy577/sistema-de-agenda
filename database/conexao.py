import sqlite3
import os

def inicializar_banco():
    # Mantendo o SEU caminho original que funciona perfeitamente
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_banco = os.path.join(diretorio_atual, "banco.db")

    try:
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()

        # 1. A SUA TABELA ORIGINAL DE PACIENTES
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
        
        # 2. NOVA TABELA DE PROFISSIONAIS
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profissionais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        """)

        # 3. INSERINDO A EQUIPE (Jadson, Dr. Gerlando, etc)
        equipe = ['Dra. Jamile', 'Jadson', 'Dr. Gerlando', 'Dra. Laurice']
        for profissional in equipe:
            try:
                cursor.execute("INSERT INTO profissionais (nome) VALUES (?)", (profissional,))
            except sqlite3.IntegrityError:
                pass # Se o nome já existir, ele ignora silenciosamente
        
        conexao.commit()
        print("✅ Banco de dados estruturado com os pacientes e a equipe médica atualizada!")
        
    except Exception as e:
        print(f"❌ Erro ao estruturar o banco: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    inicializar_banco()