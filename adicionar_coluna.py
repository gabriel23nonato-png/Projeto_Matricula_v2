import sqlite3

# Conectar ao banco de dados (cria se não existir)
conn = sqlite3.connect("database\\database\\alunosv3.db")
cursor = conn.cursor()

# Comando SQL para adicionar a nova coluna
# Exemplo: Adicionar 'email' do tipo TEXT na tabela 'alunos_v3'
cursor.execute("ALTER TABLE alunos_v3 ADD COLUMN rne INTEGER")

# Salvar as alterações
conn.commit()

# Fechar conexão
conn.close()
print("Coluna adicionada com sucesso!")
