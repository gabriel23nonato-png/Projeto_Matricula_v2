from flask import Flask, abort, render_template, request, redirect, url_for
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
        dados = request.form.to_dict()

        # ⚠️ DEBUG TEMPORÁRIO (não apague ainda)
        print("DADOS RECEBIDOS:", dados)

        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["?"] * len(dados))
        valores = list(dados.values())

        conn = sqlite3.connect("database\\database\\alunosv3.db")
        cursor = conn.cursor()

        cursor.execute(
            f"INSERT INTO alunos_v3 ({colunas}) VALUES ({placeholders})", valores
        )

        conn.commit()
        conn.close()

        return redirect(url_for("alunos_matriculados"))

    return render_template("nova_matricula.html", modo="novo", edicao_habilitada=True)


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

    cursor.execute("SELECT * FROM alunos_v3 WHERE id = ?", (id,))
    aluno = cursor.fetchone()

    if not aluno:
        conn.close()
        abort(404)

    # 🔓 Habilitar edição via ?editar=1
    edicao_habilitada = request.args.get("editar") == "1"

    if request.method == "POST":
        dados = request.form.to_dict()

        # ⚠️ DEBUG
        print("EDITANDO ID:", id)
        print("DADOS:", dados)

        campos = ", ".join([f"{k}=?" for k in dados.keys()])
        valores = list(dados.values())
        valores.append(id)

        cursor.execute(f"UPDATE alunos SET {campos} WHERE id = ?", valores)

        conn.commit()
        conn.close()

        return redirect(url_for("resumo_matricula", id=id))

    conn.close()

    return render_template(
        "nova_matricula.html",
        aluno=aluno,
        modo="editar",
        edicao_habilitada=edicao_habilitada,
    )


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
