import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "dev-secret-key"
    DATABASE_PATH = os.path.join(BASE_DIR, "..", "database", "database", "alunosv3.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "static", "uploads")
