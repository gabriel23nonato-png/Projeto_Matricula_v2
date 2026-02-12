from flask import Blueprint, render_template, request, redirect
from app.services.aluno_service import criar_aluno

alunos_bp = Blueprint("alunos", __name__)


@alunos_bp.route("/")
def index():
    return render_template("index.html")


@alunos_bp.route("/nova_matricula", methods=["POST"])
def nova_matricula():
    aluno_id = criar_aluno(request.form)
    return redirect(f"/aluno/{aluno_id}")


@alunos_bp.route("/aluno/<int:id>")
def aluno(id):
    return f"Aluno criado com ID {id}"


from app.services.aluno_service import listar_alunos


@alunos_bp.route("/alunos")
def listar():
    alunos = listar_alunos()
    return render_template("alunos_list.html", alunos=alunos)


from app.services.aluno_service import obter_aluno, editar_aluno


@alunos_bp.route("/aluno/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        editar_aluno(id, request.form)
        return redirect(f"/aluno/{id}")

    aluno = obter_aluno(id)
    return render_template("aluno_editar.html", aluno=aluno)
