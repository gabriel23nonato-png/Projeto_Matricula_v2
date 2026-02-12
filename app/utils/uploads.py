import os
from flask import current_app
from werkzeug.utils import secure_filename


def salvar_uploads(aluno_id, arquivos):
    base_path = os.path.join(current_app.config["UPLOAD_FOLDER"], str(aluno_id))

    os.makedirs(base_path, exist_ok=True)

    for campo, arquivo in arquivos.items():
        if arquivo and arquivo.filename:
            filename = secure_filename(arquivo.filename)
            arquivo.save(os.path.join(base_path, f"{campo}_{filename}"))
