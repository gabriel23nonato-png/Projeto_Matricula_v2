from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/alunos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return sqlite3.connect("escola.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nova_matricula", methods=["GET", "POST"])
def nova_matricula():
    if request.method == "POST":
        dados = request.form
        arquivos = request.files

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO alunos (
                nome_aluno, data_nascimento, sexo, turma,
                endereco, responsavel_nome, responsavel_cpf,
                responsavel_telefone, contribuicao, data_matricula
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados["nome_aluno"],
            dados["data_nascimento"],
            dados["sexo"],
            dados["turma"],
            dados["endereco"],
            dados["responsavel_nome"],
            dados["responsavel_cpf"],
            dados["responsavel_telefone"],
            dados["contribuicao"],
            datetime.now().strftime("%d/%m/%Y")
        ))

        aluno_id = cursor.lastrowid
        conn.commit()
        conn.close()

        pasta_aluno = os.path.join(UPLOAD_FOLDER, f"aluno_{aluno_id}")
        os.makedirs(pasta_aluno, exist_ok=True)

        for arquivo in arquivos.values():
            if arquivo.filename:
                arquivo.save(os.path.join(pasta_aluno, arquivo.filename))

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
