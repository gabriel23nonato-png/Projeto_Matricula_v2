from app.repositories.aluno_repository import inserir_aluno
from app.repositories.aluno_repository import buscar_todos
from app.repositories.aluno_repository import buscar_por_id, atualizar


def normalizar_dados(form_data):
    dados = {}

    for campo in form_data:
        valor = form_data.get(campo)

        if isinstance(valor, str):
            valor = valor.strip()

        dados[campo] = valor if valor not in ("", None) else None

    return dados


def criar_aluno(form_data):
    dados = normalizar_dados(form_data)
    aluno_id = inserir_aluno(dados)
    return aluno_id


def listar_alunos():
    return buscar_todos()


def obter_aluno(aluno_id):
    return buscar_por_id(aluno_id)


def editar_aluno(aluno_id, dados):
    atualizar(aluno_id, dados)
