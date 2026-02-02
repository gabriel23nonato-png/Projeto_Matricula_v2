import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "alunosv3.db")

# 🔥 cria a pasta database se não existir
os.makedirs(DB_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS alunos_v3 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    ra TEXT,
    rm TEXT,
    responsavel_matricula TEXT,
    nome_completo TEXT,
    data_nascimento TEXT,
    rg_aluno TEXT,
    cpf_aluno TEXT,
    uf_aluno TEXT,
    expedicao_aluno TEXT,
    rne_aluno TEXT,
    doc_cpf_aluno TEXT,
    cartao_sus TEXT,
    certidao_nascimento TEXT,
    municipio_nascimento TEXT,
    distrito TEXT,
    expedicao_rg_aluno TEXT,
    nacionalidade TEXT,
    doc_cartao_sus TEXT,
    doc_certidao_nascimento TEXT,

    sexo TEXT,
    raca_cor TEXT,
    peso TEXT,
    altura TEXT,
    uniforme TEXT,
    calcado TEXT,
    tipo_sanguineo TEXT,
    alergico TEXT,
    diabetico TEXT,
    lactose TEXT,
    aplv TEXT,
    cid TEXT,
    doc_carteira_vacinacao TEXT,
    doc_comprovante_vacinacao TEXT,
    doc_laudo TEXT,
    observacoes TEXT,

    nome_mae TEXT,
    profissao_mae TEXT,
    email_mae TEXT,
    cpf_mae TEXT,
    rg_mae TEXT,
    uf_rg_mae TEXT,
    expedicao_rg_mae TEXT,
    estado_civil_mae TEXT,
    doc_cpf_mae TEXT,

    nome_pai TEXT,
    profissao_pai TEXT,
    email_pai TEXT,
    cpf_pai TEXT,
    rg_pai TEXT,
    uf_rg_pai TEXT,
    expedicao_rg_pai TEXT,
    estado_civil_pai TEXT,
    doc_cpf_pai TEXT,

    telefone1 TEXT,
    telefone2 TEXT,
    telefone3 TEXT,
    telefone4 TEXT,

    pessoa1 TEXT,
    pessoa2 TEXT,
    pessoa3 TEXT,
    pessoa4 TEXT,

    bolsa_familia TEXT,
    nis TEXT,
    plano TEXT,
    app_bolsa TEXT,
    escola_anterior TEXT,
    ano TEXT,
    cidade TEXT,
    estado TEXT,

    logradouro TEXT,
    numero TEXT,
    bairro TEXT,
    cidade_endereco TEXT,
    cep TEXT,
    doc_cep TEXT,

    permite_edfisica TEXT,
    permite_fotos TEXT,
    permite_passeios TEXT,

    nivel TEXT,
    integral TEXT,
    transferencia TEXT,

    contribuicao TEXT,
    tipo_contribuicao TEXT
);
"""
)

conn.commit()
conn.close()

print("✅ Banco criado e tabela alunos_v3 criada com sucesso!")
