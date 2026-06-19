import sqlite3
import os
import sys

# ==================================================
# CAMINHOS COMPATÍVEIS COM PYTHON E EXE
# ==================================================
def caminho_base():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

banco = os.path.join(caminho_base(), "banco.db")

if os.path.exists(banco):
    os.remove(banco)
    print("🗑️ Banco de dados antigo removido.")

try:
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            profissional TEXT,
            status TEXT,
            prioridade TEXT,
            atendimento_tipo TEXT DEFAULT 'Primeira Vez',
            data_consulta TEXT
        )
    """)

    conexao.commit()
    print("✅ Banco de dados recriado com sucesso na mesma pasta do script!")

except Exception as erro:
    print("❌ Erro ao criar o banco:", erro)
finally:
    conexao.close()