# ============================================================
# rotas/login.py — Login com Token JWT
# Descrição: Confere e-mail e senha, e devolve um token JWT
#            se estiverem corretos.
# ============================================================

import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter
from pydantic import BaseModel

from database import conectar

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITMO = "HS256"


class Login(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(dados: Login):
    # Confere o usuário e devolve um token JWT para autenticação
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE email = %s", (dados.email,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        return {"erro": "E-mail ou senha inválidos"}

    senha_confere = bcrypt.checkpw(dados.senha.encode("utf-8"), usuario["senha"].encode("utf-8"))
    if not senha_confere:
        return {"erro": "E-mail ou senha inválidos"}

    expira_em = datetime.now(timezone.utc) + timedelta(hours=2)
    payload = {
        "sub": usuario["email"],
        "tipo": usuario["tipo"],
        "exp": expira_em,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITMO)
    return {"access_token": token, "token_type": "bearer"}
