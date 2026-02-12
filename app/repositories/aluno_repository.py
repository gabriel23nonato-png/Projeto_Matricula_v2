import sqlite3
from app.db import get_connection


def buscar_todos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nome_completo, rm, ra, data_nascimento
        FROM alunos_v3
        ORDER BY nome_completo
    """
    )

    alunos = cursor.fetchall()
    conn.close()
    return alunos


def inserir_aluno(dados):
    conn = get_connection()
    cursor = conn.cursor()

    colunas = ", ".join(dados.keys())
    placeholders = ", ".join(["?"] * len(dados))

    sql = f"""
        INSERT INTO alunos_v3 ({colunas})
        VALUES ({placeholders})
    """

    cursor.execute(sql, list(dados.values()))
    conn.commit()

    aluno_id = cursor.lastrowid
    conn.close()

    return aluno_id


def buscar_por_id(aluno_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos_v3 WHERE id = ?", (aluno_id,))

    aluno = cursor.fetchone()
    colunas = [col[0] for col in cursor.description]

    conn.close()

    if aluno:
        return dict(zip(colunas, aluno))
    return None


def atualizar(aluno_id, dados):
    conn = get_connection()
    cursor = conn.cursor()

    campos = []
    valores = []

    for campo, valor in dados.items():
        if campo != "id":
            campos.append(f"{campo} = ?")
            valores.append(valor)

    valores.append(aluno_id)

    sql = f"""
        UPDATE alunos_v3
        SET {', '.join(campos)}
        WHERE id = ?
    """

    cursor.execute(sql, valores)
    conn.commit()
    conn.close()
