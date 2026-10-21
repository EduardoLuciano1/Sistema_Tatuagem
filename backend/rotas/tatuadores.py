# ============================================================
# rotas/tatuadores.py — CRUD de Tatuadores
# Descrição: Endpoints para gerenciar os tatuadores do estúdio.
# ============================================================

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from database import conectar

router = APIRouter()


class Tatuador(BaseModel):
    nometatuador: str
    cpf: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    datacontratacao: Optional[str] = None
    idsenioridade: int


@router.get("")
def listar_tatuadores():
    # Retorna os tatuadores junto com o nome da senioridade
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT tatuador.*, senioridade.nome AS senioridade
        FROM tatuador
        JOIN senioridade ON tatuador.idsenioridade = senioridade.idsenioridade
        ORDER BY tatuador.idtatuador
        """
    )
    tatuadores = cursor.fetchall()
    conn.close()
    return tatuadores


@router.get("/{id}")
def buscar_tatuador(id: int):
    # Busca um tatuador pelo ID
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tatuador WHERE idtatuador = %s", (id,))
    tatuador = cursor.fetchone()
    conn.close()
    if not tatuador:
        return {"erro": "Tatuador não encontrado"}
    return tatuador


@router.post("")
def criar_tatuador(tatuador: Tatuador):
    # Insere um novo tatuador e retorna o ID gerado
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tatuador (nometatuador, cpf, email, telefone, datacontratacao, idsenioridade)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email, tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade),
    )
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador cadastrado com sucesso", "idtatuador": novo_id}


@router.put("/{id}")
def atualizar_tatuador(id: int, tatuador: Tatuador):
    # Atualiza os dados de um tatuador existente
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tatuador
           SET nometatuador=%s, cpf=%s, email=%s, telefone=%s, datacontratacao=%s, idsenioridade=%s
           WHERE idtatuador=%s""",
        (tatuador.nometatuador, tatuador.cpf, tatuador.email, tatuador.telefone, tatuador.datacontratacao, tatuador.idsenioridade, id),
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Tatuador atualizado com sucesso"}


@router.delete("/{id}")
def deletar_tatuador(id: int):
    # Remove um tatuador, se ele não estiver associado a agendamentos
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM tatuador WHERE idtatuador = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Tatuador deletado com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este tatuador. Verifique se ele está relacionado a algum agendamento ou estilo."}


@router.get("/{id}/estilos")
def listar_estilos_do_tatuador(id: int):
    # Retorna os estilos que este tatuador domina
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT estilo.idestilo, estilo.descricao
        FROM tatuador_estilo
        JOIN estilo ON tatuador_estilo.idestilo = estilo.idestilo
        WHERE tatuador_estilo.idtatuador = %s
        ORDER BY estilo.idestilo
        """,
        (id,),
    )
    estilos = cursor.fetchall()
    conn.close()
    return estilos


@router.put("/{id}/estilos")
def salvar_estilos_do_tatuador(id: int, estilos: list[int]):
    # Atualiza os estilos associados a um tatuador
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tatuador_estilo WHERE idtatuador = %s", (id,))

    for idestilo in estilos:
        cursor.execute(
            "INSERT INTO tatuador_estilo (idtatuador, idestilo, dataestilo) VALUES (%s, %s, CURDATE())",
            (id, idestilo),
        )

    conn.commit()
    conn.close()
    return {"mensagem": "Estilos do tatuador atualizados com sucesso"}
