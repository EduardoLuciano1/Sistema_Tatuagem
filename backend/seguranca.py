# ============================================================
# seguranca.py — Verificação do token JWT
# Descrição: Funções usadas nas rotas protegidas para validar
#            autenticação e autorização por tipo de usuário.
# ============================================================

import os

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITMO = "HS256"

esquema_token = HTTPBearer()


def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(esquema_token)):
    # Valida o token JWT vindo no cabeçalho Authorization
    token = credenciais.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado, faça login de novo")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def verificar_admin(payload: dict = Depends(verificar_token)):
    # Garante que o usuário autenticado é administrador
    if payload.get("tipo") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return payload
