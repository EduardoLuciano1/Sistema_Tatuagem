# ============================================================
# database.py — Conexão com o MySQL
# Descrição: Centraliza a criação da conexão com o banco
#            usando variáveis do arquivo .env.
# ============================================================

import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    # Cria e retorna uma conexão com o banco de dados do projeto
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "estudio_tatuagem"),
        port=int(os.getenv("DB_PORT", "3306")),
        autocommit=False,
    )
