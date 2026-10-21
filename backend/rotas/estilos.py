# ============================================================
# rotas/estilos.py — CRUD de Estilos
# Descrição: Endpoints para gerenciar os estilos de tatuagem.
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel

from database import conectar

router = APIRouter()


class Estilo(BaseModel):
    descricao: str


@router.get("")
def listar_estilos():
    # Retorna todos os estilos cadastrados
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estilo ORDER BY idestilo")
    estilos = cursor.fetchall()
    conn.close()
    return estilos


@router.get("/{id}")
def buscar_estilo(id: int):
    # Busca um estilo pelo ID
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estilo WHERE idestilo = %s", (id,))
    estilo = cursor.fetchone()
    conn.close()
    if not estilo:
        return {"erro": "Estilo não encontrado"}
    return estilo


@router.post("")
def criar_estilo(estilo: Estilo):
    # Cadastra um novo estilo de tatuagem
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estilo (descricao) VALUES (%s)", (estilo.descricao,))
    conn.commit()
    conn.close()
    return {"mensagem": "Estilo cadastrado com sucesso"}


@router.put("/{id}")
def atualizar_estilo(id: int, estilo: Estilo):
    # Atualiza um estilo existente
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE estilo SET descricao=%s WHERE idestilo=%s", (estilo.descricao, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Estilo atualizado com sucesso"}


@router.delete("/{id}")
def deletar_estilo(id: int):
    # Remove um estilo, se ele não estiver relacionado a tatuadores
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM estilo WHERE idestilo = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Estilo deletado com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este estilo. Verifique se algum tatuador já foi marcado com ele."}
