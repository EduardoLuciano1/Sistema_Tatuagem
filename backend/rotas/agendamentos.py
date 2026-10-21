# ============================================================
# rotas/agendamentos.py — CRUD de Agendamentos
# Descrição: Endpoints para gerenciar agendamentos de tatuagem.
# ============================================================

import os
from typing import Optional

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel

from database import conectar

router = APIRouter()


class Agendamento(BaseModel):
    idcliente: int
    idtatuador: int
    dataagendamento: str
    horaagendamento: str
    descricaotatuagem: Optional[str] = None
    valortatuagem: Optional[float] = None
    status: Optional[str] = None


@router.get("")
def listar_agendamentos():
    # Retorna todos os agendamentos com o nome do cliente e do tatuador
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT agendamento.*, cliente.nome AS cliente, tatuador.nometatuador AS tatuador
        FROM agendamento
        JOIN cliente ON agendamento.idcliente = cliente.idcliente
        JOIN tatuador ON agendamento.idtatuador = tatuador.idtatuador
        ORDER BY agendamento.idagendamento
        """
    )
    agendamentos = cursor.fetchall()
    conn.close()

    for agendamento in agendamentos:
        if agendamento["horaagendamento"] is not None:
            if hasattr(agendamento["horaagendamento"], "total_seconds"):
                total_segundos = int(agendamento["horaagendamento"].total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return agendamentos


@router.get("/{id}")
def buscar_agendamento(id: int):
    # Busca um agendamento pelo ID
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM agendamento WHERE idagendamento = %s", (id,))
    agendamento = cursor.fetchone()
    conn.close()
    if not agendamento:
        return {"erro": "Agendamento não encontrado"}

    if agendamento["horaagendamento"] is not None and hasattr(agendamento["horaagendamento"], "total_seconds"):
        total_segundos = int(agendamento["horaagendamento"].total_seconds())
        horas, resto = divmod(total_segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        agendamento["horaagendamento"] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return agendamento


@router.post("")
def criar_agendamento(agendamento: Agendamento):
    # Cria um agendamento e devolve o ID gerado
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO agendamento (idcliente, idtatuador, dataagendamento, horaagendamento, descricaotatuagem, valortatuagem)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            agendamento.idcliente,
            agendamento.idtatuador,
            agendamento.dataagendamento,
            agendamento.horaagendamento,
            agendamento.descricaotatuagem,
            agendamento.valortatuagem,
        ),
    )
    novo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento cadastrado com sucesso", "idagendamento": novo_id}


@router.put("/{id}")
def atualizar_agendamento(id: int, agendamento: Agendamento):
    # Atualiza um agendamento existente
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE agendamento
           SET idcliente=%s, idtatuador=%s, dataagendamento=%s, horaagendamento=%s,
               descricaotatuagem=%s, valortatuagem=%s, status=%s
           WHERE idagendamento=%s""",
        (
            agendamento.idcliente,
            agendamento.idtatuador,
            agendamento.dataagendamento,
            agendamento.horaagendamento,
            agendamento.descricaotatuagem,
            agendamento.valortatuagem,
            agendamento.status,
            id,
        ),
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento atualizado com sucesso"}


@router.delete("/{id}")
def deletar_agendamento(id: int):
    # Remove um agendamento do banco
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM agendamento WHERE idagendamento = %s", (id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Agendamento deletado com sucesso"}


@router.post("/{id}/desenho")
async def upload_desenho(id: int, arquivo: UploadFile = File(...)):
    # Salva a imagem do desenho aprovado em uploads/ e vincula ao agendamento
    nome_arquivo = f"{id}_{arquivo.filename}"
    caminho = os.path.join("uploads", nome_arquivo)

    conteudo = await arquivo.read()
    with open(caminho, "wb") as f:
        f.write(conteudo)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE agendamento SET desenhoaprovado=%s WHERE idagendamento=%s", (nome_arquivo, id))
    conn.commit()
    conn.close()
    return {"mensagem": "Desenho enviado com sucesso", "arquivo": nome_arquivo}
