# ============================================================
# rotas/clientes.py — CRUD de Clientes
# Descrição: Endpoints para gerenciar clientes do estúdio.
# ============================================================

from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from database import conectar

router = APIRouter()


class Cliente(BaseModel):
    nome: str
    cpf: str
    telefone: Optional[str] = None
    datacadastro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None


@router.get("")
def listar_clientes():
    # Retorna todos os clientes cadastrados no banco
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente ORDER BY idcliente")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


@router.get("/{id}")
def buscar_cliente(id: int):
    # Busca um cliente pelo ID
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente WHERE idcliente = %s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    if not cliente:
        return {"erro": "Cliente não encontrado"}
    return cliente


@router.post("")
def criar_cliente(cliente: Cliente):
    # Insere um novo cliente no banco
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO cliente (nome, cpf, telefone, datacadastro, cidade, uf)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (cliente.nome, cliente.cpf, cliente.telefone, cliente.datacadastro, cliente.cidade, cliente.uf),
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente cadastrado com sucesso"}


@router.put("/{id}")
def atualizar_cliente(id: int, cliente: Cliente):
    # Atualiza os dados de um cliente existente
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE cliente
           SET nome=%s, cpf=%s, telefone=%s, datacadastro=%s, cidade=%s, uf=%s
           WHERE idcliente=%s""",
        (cliente.nome, cliente.cpf, cliente.telefone, cliente.datacadastro, cliente.cidade, cliente.uf, id),
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Cliente atualizado com sucesso"}


@router.delete("/{id}")
def deletar_cliente(id: int):
    # Remove um cliente, se ele não estiver associado a agendamentos
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM cliente WHERE idcliente = %s", (id,))
        conn.commit()
        conn.close()
        return {"mensagem": "Cliente deletado com sucesso"}
    except Exception:
        conn.rollback()
        conn.close()
        return {"erro": "Não foi possível excluir este cliente. Verifique se ele possui agendamentos."}
