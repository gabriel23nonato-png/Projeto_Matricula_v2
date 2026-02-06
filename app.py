from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/alunos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    return sqlite3.connect("database\\database\\alunosv3.db")


def salvar_uploads(aluno_id, arquivos):
    base = f"uploads/alunos/aluno_{aluno_id}"

    secoes = {
        "identificacao": ["doc_cpf_aluno", "doc_sus", "doc_certidao"],
        "responsavel": ["doc_cpf_mae", "doc_cpf_pai"],
        "endereco": ["doc_cep"],
        "saude": ["doc_laudo", "doc_carteira_vacinacao", "doc_comprovante_vacinacao"],
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

        conn = sqlite3.connect("database\\database\\alunosv3.db")
        cursor = conn.cursor()

        cursor.execute(
            """
        INSERT INTO alunos_v3 (
    ra,
    rm,
    responsavel_matricula,
    nome_completo,
    data_nascimento,
    rg_aluno,
    cpf_aluno,
    uf_aluno,
    expedicao_aluno,
    rne_aluno,
    doc_cpf_aluno,
    cartao_sus,
    certidao_nascimento,
    municipio_nascimento,
    distrito,
    expedicao_rg_aluno,
    nacionalidade,
    doc_cartao_sus,
    doc_certidao_nascimento,
    sexo,
    raca_cor,
    peso,
    altura,
    uniforme,
    calcado,
    tipo_sanguineo,
    alergico,
    diabetico,
    lactose,
    aplv,
    cid,
    doc_carteira_vacinacao,
    doc_comprovante_vacinacao,
    doc_laudo,
    observacoes,
    nome_mae,
    profissao_mae,
    email_mae,
    cpf_mae,
    rg_mae,
    uf_rg_mae,
    expedicao_rg_mae,
    estado_civil_mae,
    doc_cpf_mae,
    nome_pai,
    profissao_pai,
    email_pai,
    cpf_pai,
    rg_pai,
    uf_rg_pai,
    expedicao_rg_pai,
    estado_civil_pai,
    doc_cpf_pai,
    telefone1,
    telefone2,
    telefone3,
    telefone4,
    pessoa1,
    pessoa2,
    pessoa3,
    pessoa4,
    bolsa_familia,
    nis,
    plano,
    app_bolsa,
    escola_anterior,
    ano,
    cidade,
    estado,
    logradouro,
    numero,
    bairro,
    cidade_endereco,
    cep,
    doc_cep,
    permite_edfisica,
    permite_fotos,
    permite_passeios,
    nivel,
    integral,
    transferencia,
    contribuicao,
    tipo_contribuicao
)
VALUES (
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    ?, ?, ?
);

""",  # 47 campos Nem todos os campos de anexo de documentos funcionam
            (
                d.get("ra"),
                d.get("rm"),
                d.get("responsavel_matricula"),
                d.get("nome_completo"),
                d.get("data_nascimento"),
                d.get("rg_aluno"),
                d.get("cpf_aluno"),
                d.get("uf_aluno"),
                d.get("expedicao_aluno"),
                d.get("rne_aluno"),
                d.get("doc_cpf_aluno"),
                d.get("cartao_sus"),
                d.get("certidao_nascimento"),
                d.get("municipio_nascimento"),
                d.get("distrito"),
                d.get("expedicao_rg_aluno"),
                d.get("nacionalidade"),
                d.get("doc_cartao_sus"),
                d.get("doc_certidao_nascimento"),
                d.get("sexo"),
                d.get("raca_cor"),
                d.get("peso"),
                d.get("altura"),
                d.get("uniforme"),
                d.get("calcado"),
                d.get("tipo_sanguineo"),
                d.get("alergico"),
                d.get("diabetico"),
                d.get("lactose"),
                d.get("aplv"),
                d.get("cid"),
                d.get("doc_carteira_vacinacao"),
                d.get("doc_comprovante_vacinacao"),
                d.get("doc_laudo"),
                d.get("observacoes"),
                d.get("nome_mae"),
                d.get("profissao_mae"),
                d.get("email_mae"),
                d.get("cpf_mae"),
                d.get("rg_mae"),
                d.get("uf_rg_mae"),
                d.get("expedicao_rg_mae"),
                d.get("estado_civil_mae"),
                d.get("doc_cpf_mae"),
                d.get("nome_pai"),
                d.get("profissao_pai"),
                d.get("email_pai"),
                d.get("cpf_pai"),
                d.get("rg_pai"),
                d.get("uf_rg_pai"),
                d.get("expedicao_rg_pai"),
                d.get("estado_civil_pai"),
                d.get("doc_cpf_pai"),
                d.get("telefone1"),
                d.get("telefone2"),
                d.get("telefone3"),
                d.get("telefone4"),
                d.get("pessoa1"),
                d.get("pessoa2"),
                d.get("pessoa3"),
                d.get("pessoa4"),
                d.get("bolsa_familia"),
                d.get("nis"),
                d.get("plano"),
                d.get("app_bolsa"),
                d.get("escola_anterior"),
                d.get("ano"),
                d.get("cidade"),
                d.get("estado"),
                d.get("logradouro"),
                d.get("numero"),
                d.get("bairro"),
                d.get("cidade_endereco"),
                d.get("cep"),
                d.get("doc_cep"),
                d.get("permite_edfisica"),
                d.get("permite_fotos"),
                d.get("permite_passeios"),
                d.get("nivel"),
                d.get("integral"),
                d.get("transferencia"),
                d.get("contribuicao"),
                d.get("tipo_contribuicao"),
                # datetime.now().strftime("%d/%m/%Y"),
            ),
        )
        aluno_id = cursor.lastrowid
        conn.commit()
        conn.close()

        salvar_uploads(aluno_id, f)

        return redirect(url_for("resumo_matricula", aluno_id=aluno_id))

    return render_template("nova_matricula.html")


@app.route("/resumo/<int:aluno_id>")
def resumo_matricula(aluno_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos_v3 WHERE id=?", (aluno_id,))
    aluno = cursor.fetchone()
    conn.close()

    return render_template("resumo_matricula.html", aluno=aluno)


@app.route("/alunos")
def alunos_matriculados():
    q = request.args.get("q", "").strip()
    nivel = request.args.get("nivel", "")
    sala = request.args.get("sala", "")

    conn = sqlite3.connect("database\\database\\alunosv3.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM alunos_v3 WHERE 1=1"
    params = []

    if q:
        query += """
            AND (
                nome_completo LIKE ?
                OR nome_mae LIKE ?
                OR cpf_aluno LIKE ?
            )
        """
        like = f"%{q}%"
        params.extend([like, like, like])

    if nivel:
        query += " AND nivel = ?"
        params.append(nivel)

    if sala:
        query += " AND sala = ?"
        params.append(sala)

    query += " ORDER BY nome_completo"

    cursor.execute(query, params)
    alunos = cursor.fetchall()
    conn.close()

    return render_template("alunos.html", alunos=alunos, q=q, nivel=nivel, sala=sala)


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_matricula(id):
    conn = sqlite3.connect("database\\database\\alunosv3.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        d = request.form

        cursor.execute(
            """
            UPDATE alunos_v3
            SET
                ra = ?,
                rm = ?,
                responsavel_matricula = ?,
                nome_completo = ?,
                data_nascimento = ?,
                rg_aluno = ?,
                cpf_aluno = ?,
                uf_aluno = ?,
                expedicao_aluno = ?,
                rne_aluno = ?,
                doc_cpf_aluno = ?,
                cartao_sus = ?,
                certidao_nascimento = ?,
                municipio_nascimento = ?,
                distrito = ?,
                expedicao_rg_aluno = ?,
                nacionalidade = ?,
                doc_cartao_sus = ?,
                doc_certidao_nascimento = ?,
                sexo = ?,
                raca_cor = ?,
                peso = ?,
                altura = ?,
                uniforme = ?,
                calcado = ?,
                tipo_sanguineo = ?,
                alergico = ?,
                diabetico = ?,
                lactose = ?,
                aplv = ?,
                cid = ?,
                doc_carteira_vacinacao = ?,
                doc_comprovante_vacinacao = ?,
                doc_laudo = ?,
                observacoes = ?,
                nome_mae = ?,
                profissao_mae = ?,
                email_mae = ?,
                cpf_mae = ?,
                rg_mae = ?,
                uf_rg_mae = ?,
                expedicao_rg_mae = ?,
                estado_civil_mae = ?,
                doc_cpf_mae = ?,
                nome_pai = ?,
                profissao_pai = ?,
                email_pai = ?,
                cpf_pai = ?,
                rg_pai = ?,
                uf_rg_pai = ?,
                expedicao_rg_pai = ?,
                estado_civil_pai = ?,
                doc_cpf_pai = ?,
                telefone1 = ?,
                telefone2 = ?,
                telefone3 = ?,
                telefone4 = ?,
                pessoa1 = ?,
                pessoa2 = ?,
                pessoa3 = ?,
                pessoa4 = ?,
                bolsa_familia = ?,
                nis = ?,
                plano = ?,
                app_bolsa = ?,
                escola_anterior = ?,
                ano = ?,
                cidade = ?,
                estado = ?,
                logradouro = ?,
                numero = ?,
                bairro = ?,
                cidade_endereco = ?,
                cep = ?,
                doc_cep = ?,
                permite_edfisica = ?,
                permite_fotos = ?,
                permite_passeios = ?,
                nivel = ?,
                integral = ?,
                transferencia = ?,
                contribuicao = ?,
                tipo_contribuicao = ?
            WHERE id = ?
        """,
            (
                d.get("ra"),
                d.get("rm"),
                d.get("responsavel_matricula"),
                d.get("nome_completo"),
                d.get("data_nascimento"),
                d.get("rg_aluno"),
                d.get("cpf_aluno"),
                d.get("uf_aluno"),
                d.get("expedicao_aluno"),
                d.get("rne_aluno"),
                d.get("doc_cpf_aluno"),
                d.get("cartao_sus"),
                d.get("certidao_nascimento"),
                d.get("municipio_nascimento"),
                d.get("distrito"),
                d.get("expedicao_rg_aluno"),
                d.get("nacionalidade"),
                d.get("doc_cartao_sus"),
                d.get("doc_certidao_nascimento"),
                d.get("sexo"),
                d.get("raca_cor"),
                d.get("peso"),
                d.get("altura"),
                d.get("uniforme"),
                d.get("calcado"),
                d.get("tipo_sanguineo"),
                d.get("alergico"),
                d.get("diabetico"),
                d.get("lactose"),
                d.get("aplv"),
                d.get("cid"),
                d.get("doc_carteira_vacinacao"),
                d.get("doc_comprovante_vacinacao"),
                d.get("doc_laudo"),
                d.get("observacoes"),
                d.get("nome_mae"),
                d.get("profissao_mae"),
                d.get("email_mae"),
                d.get("cpf_mae"),
                d.get("rg_mae"),
                d.get("uf_rg_mae"),
                d.get("expedicao_rg_mae"),
                d.get("estado_civil_mae"),
                d.get("doc_cpf_mae"),
                d.get("nome_pai"),
                d.get("profissao_pai"),
                d.get("email_pai"),
                d.get("cpf_pai"),
                d.get("rg_pai"),
                d.get("uf_rg_pai"),
                d.get("expedicao_rg_pai"),
                d.get("estado_civil_pai"),
                d.get("doc_cpf_pai"),
                d.get("telefone1"),
                d.get("telefone2"),
                d.get("telefone3"),
                d.get("telefone4"),
                d.get("pessoa1"),
                d.get("pessoa2"),
                d.get("pessoa3"),
                d.get("pessoa4"),
                d.get("bolsa_familia"),
                d.get("nis"),
                d.get("plano"),
                d.get("app_bolsa"),
                d.get("escola_anterior"),
                d.get("ano"),
                d.get("cidade"),
                d.get("estado"),
                d.get("logradouro"),
                d.get("numero"),
                d.get("bairro"),
                d.get("cidade_endereco"),
                d.get("cep"),
                d.get("doc_cep"),
                d.get("permite_edfisica"),
                d.get("permite_fotos"),
                d.get("permite_passeios"),
                d.get("nivel"),
                d.get("integral"),
                d.get("transferencia"),
                d.get("contribuicao"),
                d.get("tipo_contribuicao"),
                id,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("alunos_matriculados"))

    cursor.execute("SELECT * FROM alunos_v3 WHERE id = ?", (id,))
    aluno = cursor.fetchone()
    conn.close()

    if not aluno:
        os.abort(404)

    return render_template("nova_matricula.html", aluno=aluno, modo="editar")


@app.route("/financeiro")
def financeiro():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT turma, SUM(contribuicao)
        FROM alunos_v3
        GROUP BY turma
    """
    )
    totais = cursor.fetchall()
    conn.close()

    return render_template("financeiro.html", totais=totais)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
