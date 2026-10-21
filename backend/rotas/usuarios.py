# ============================================================
# rotas/usuarios.py — Cadastro de Usuários
# Descrição: Endpoint para cadastrar novos usuários do sistema,
#            guardando a senha como hash (nunca em texto puro).
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel

import bcrypt

from database import conectar

router = APIRouter()


class Usuario(BaseModel):
    nome: str
    email: str
    senha: str


@router.post("")
def criar_usuario(usuario: Usuario):
    # Gera o hash da senha antes de guardar no banco
    senha_hash = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, senha_hash.decode("utf-8")),
        )
        conn.commit()
        conn.close()
        return {"mensagem": "Usuário cadastrado com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível cadastrar. Verifique se esse e-mail já está em uso."}
