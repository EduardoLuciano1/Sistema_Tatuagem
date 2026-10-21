# ============================================================
# rotas/senioridade.py — CRUD de Senioridade
# Descrição: Endpoints para gerenciar os níveis de senioridade
#            dos tatuadores.
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel

from database import conectar

router = APIRouter()


class Senioridade(BaseModel):
    nome: str


@router.get("")
def listar_senioridade():
    # Retorna todas as senioridades cadastradas
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade ORDER BY idsenioridade")
    senioridades = cursor.fetchall()
    conn.close()
    return senioridades


@router.get("/{id}")
def buscar_senioridade(id: int):
    # Busca uma senioridade pelo ID
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM senioridade WHERE idsenioridade = %s", (id,))
    senioridade = cursor.fetchone()
    conn.close()
    if not senioridade:
        return {"erro": "Senioridade não encontrada"}
    return senioridade


@router.post("")
def criar_senioridade(senioridade: Senioridade):
    # Cadastra uma nova senioridade
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO senioridade (nome) VALUES (%s)", (senioridade.nome,))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade cadastrada com sucesso"}


@router.put("/{id}")
def atualizar_senioridade(id: int, senioridade: Senioridade):
    # Atualiza uma senioridade existente
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE senioridade SET nome=%s WHERE idsenioridade=%s", (senioridade.nome, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Senioridade atualizada com sucesso"}


@router.delete("/{id}")
def deletar_senioridade(id: int):
    # Remove uma senioridade, se ela não estiver sendo usada por tatuadores
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM senioridade WHERE idsenioridade = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Senioridade deletada com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir esta senioridade. Verifique se ela está sendo usada por algum tatuador."}
