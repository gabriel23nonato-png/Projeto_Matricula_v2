from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/alunos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect("escola.db")

def salvar_uploads(aluno_id, arquivos):
    base = f"uploads/alunos/aluno_{aluno_id}"

    secoes = {
        "identificacao": ["doc_cpf_aluno", "doc_sus", "doc_certidao"],
        "responsavel": ["doc_cpf_mae", "doc_cpf_pai"],
        "endereco": ["doc_cep"],
        "saude": ["doc_laudo", "doc_carteira_vacinacao", "doc_comprovante_vacinacao"]
    }

    for secao, campos in secoes.items():
        pasta = os.path.join(base, secao)
        os.makedirs(pasta, exist_ok=True)

        for campo in campos:
            arquivo = arquivos.get(campo)
            if arquivo and arquivo.filename:
                arquivo.save(os.path.join(pasta, arquivo.filename))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nova_matricula", methods=["GET", "POST"])
def nova_matricula():
    if request.method == "POST":
        d = request.form
        f = request.files

        conn = sqlite3.connect("escola.db")
        cursor = conn.cursor()

        cursor.execute("""
INSERT INTO alunos_v2 (
    ra, nome_completo, data_nascimento, rg_aluno, cpf_aluno,
    cartao_sus, certidao_nascimento, sexo, raca_cor, nacionalidade,

    nome_mae, cpf_mae, rg_mae, nome_pai, cpf_pai, rg_pai,
    telefone1, telefone2, telefone3, telefone4, responsavel_matricula,

    retirada_pessoa1, retirada_numero1,
    retirada_pessoa2, retirada_numero2,
    retirada_pessoa3, retirada_numero3,
    escola_anterior, permite_fotos, permite_postar,

    logradouro, numero, bairro, cidade, cep,

    peso, altura, uniforme, calcado,
    alergico, diabetico, lactose, aplv,
    necessidades_especiais,

    contribuicao, tipo_contribuicao, data_matricula
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); 
""", # 47 campos Nem todos os campos de anexo de documentos funcionam
    (
    # 1–10 Identificação
    d.get("ra"),
    d["nome_completo"],
    d["data_nascimento"],
    d.get("rg_aluno"),
    d.get("cpf_aluno"),
    d.get("cartao_sus"),
    d.get("certidao_nascimento"),
    d["sexo"],
    d.get("raca_cor"),
    d.get("nacionalidade"),

    # 11–21 Responsável
    d["nome_mae"],
    d["cpf_mae"],
    d["rg_mae"],
    d.get("nome_pai"),
    d.get("cpf_pai"),
    d.get("rg_pai"),
    d["telefone1"],
    d.get("telefone2"),
    d.get("telefone3"),
    d.get("telefone4"),
    d.get("responsavel_matricula"),

    # 22–30 Informações escolares
    d.get("retirada_pessoa1"),
    d.get("retirada_numero1"),
    d.get("retirada_pessoa2"),
    d.get("retirada_numero2"),
    d.get("retirada_pessoa3"),
    d.get("retirada_numero3"),
    d.get("escola_anterior"),
    d.get("permite_fotos"),
    d.get("permite_postar"),

    # 31–35 Endereço
    d.get("logradouro"),
    d.get("numero"),
    d.get("bairro"),
    d.get("cidade"),
    d.get("cep"),

    # 36–44 Saúde
    d.get("peso"),
    d.get("altura"),
    d.get("uniforme"),
    d.get("calcado"),
    d.get("alergico"),
    d.get("diabetico"),
    d.get("lactose"),
    d.get("aplv"),
    d.get("necessidades_especiais"),

    # 45–47 Financeiro
    d.get("contribuicao"),
    d.get("tipo_contribuicao"),
    datetime.now().strftime("%d/%m/%Y")
))
        aluno_id = cursor.lastrowid
        conn.commit()
        conn.close()

        salvar_uploads(aluno_id, f)

        return redirect(url_for("resumo_matricula", aluno_id=aluno_id))

    return render_template("nova_matricula.html")


@app.route("/resumo/<int:aluno_id>")
def resumo_matricula(aluno_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE id=?", (aluno_id,))
    aluno = cursor.fetchone()
    conn.close()

    return render_template("resumo_matricula.html", aluno=aluno)

@app.route("/alunos")
def alunos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    conn.close()

    return render_template("alunos.html", alunos=alunos)

@app.route("/financeiro")
def financeiro():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT turma, SUM(contribuicao)
        FROM alunos
        GROUP BY turma
    """)
    totais = cursor.fetchall()
    conn.close()

    return render_template("financeiro.html", totais=totais)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
