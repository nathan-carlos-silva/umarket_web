"""
O carrinho de compras nao existe como tabela no banco (e nao deveria: e um
estado transitorio). Ele fica guardado na sessao do Flask como um dicionario
{ "id_produto (str)": quantidade }. So vira registro persistente (VENDAS +
VENDAS_PRODUTOS) quando o cliente finaliza a compra -> ver venda_service.py
"""
from flask import session

from umarket.config import Config
from umarket.models.produto import Produto

CHAVE = Config.CARRINHO_SESSION_KEY


def _carrinho_bruto() -> dict:
    return session.setdefault(CHAVE, {})


def adicionar_item(id_produto: int, quantidade: int = 1) -> None:
    carrinho = _carrinho_bruto()
    chave = str(id_produto)
    carrinho[chave] = carrinho.get(chave, 0) + quantidade
    session[CHAVE] = carrinho
    session.modified = True


def atualizar_quantidade(id_produto: int, quantidade: int) -> None:
    carrinho = _carrinho_bruto()
    chave = str(id_produto)
    if quantidade <= 0:
        carrinho.pop(chave, None)
    else:
        carrinho[chave] = quantidade
    session[CHAVE] = carrinho
    session.modified = True


def remover_item(id_produto: int) -> None:
    carrinho = _carrinho_bruto()
    carrinho.pop(str(id_produto), None)
    session[CHAVE] = carrinho
    session.modified = True


def limpar_carrinho() -> None:
    session[CHAVE] = {}
    session.modified = True


def contar_itens() -> int:
    return sum(_carrinho_bruto().values())


def montar_itens_detalhados() -> list[dict]:
    """
    Retorna uma lista de dicts prontos para o template do carrinho:
    [{ "produto": Produto, "quantidade": int, "subtotal": Decimal }, ...]
    Produtos que nao existem mais no banco sao ignorados silenciosamente.
    """
    carrinho = _carrinho_bruto()
    if not carrinho:
        return []

    ids = [int(k) for k in carrinho.keys()]
    produtos = Produto.query.filter(Produto.id.in_(ids)).all()
    produtos_por_id = {p.id: p for p in produtos}

    itens = []
    for id_str, quantidade in carrinho.items():
        produto = produtos_por_id.get(int(id_str))
        if produto is None:
            continue
        itens.append(
            {
                "produto": produto,
                "quantidade": quantidade,
                "subtotal": produto.preco * quantidade,
            }
        )
    return itens


def calcular_total(itens_detalhados: list[dict]):
    return sum((item["subtotal"] for item in itens_detalhados), start=0)
