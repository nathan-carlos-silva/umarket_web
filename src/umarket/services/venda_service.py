from umarket.extensions import db
from umarket.models.estoque import Estoque
from umarket.models.venda import Venda
from umarket.models.venda_produto import VendaProduto


class EstoqueInsuficienteError(Exception):
    def __init__(self, nome_produto: str, disponivel: int, solicitado: int):
        self.nome_produto = nome_produto
        self.disponivel = disponivel
        self.solicitado = solicitado
        super().__init__(
            f'Estoque insuficiente para "{nome_produto}": '
            f"disponivel {disponivel}, solicitado {solicitado}."
        )


def finalizar_compra(
    id_usuario: int,
    id_pdv: int,
    forma_pagamento: str,
    itens_detalhados: list[dict],
) -> Venda:
    """
    Recebe os itens do carrinho ja resolvidos (produto + quantidade + subtotal)
    e o PDV escolhido pelo cliente. Faz tudo dentro de uma unica transacao:
      1. Verifica se ha saldo em ESTOQUE para cada produto naquele PDV.
      2. Cria a VENDA (cabecalho).
      3. Cria um VENDA_PRODUTO para cada item (detalhamento).
      4. Abate a quantidade comprada do ESTOQUE (RF18 - automatico).
    Se qualquer item nao tiver estoque suficiente, nada e gravado (rollback).
    """
    if not itens_detalhados:
        raise ValueError("O carrinho esta vazio.")

    # 1. Trava/consulta o estoque de cada produto neste PDV e valida saldo
    estoques_por_produto: dict[int, Estoque] = {}
    for item in itens_detalhados:
        produto = item["produto"]
        estoque = Estoque.query.filter_by(
            id_pdv=id_pdv, id_produto=produto.id
        ).with_for_update().first()

        if estoque is None or estoque.qtd_atual < item["quantidade"]:
            disponivel = estoque.qtd_atual if estoque else 0
            raise EstoqueInsuficienteError(
                produto.nome, disponivel, item["quantidade"]
            )
        estoques_por_produto[produto.id] = estoque

    # 2. Cria o cabecalho da venda
    valor_total_venda = sum(item["subtotal"] for item in itens_detalhados)
    venda = Venda(
        id_usuario=id_usuario,
        id_pdv=id_pdv,
        forma_pagamento=forma_pagamento,
        valor=valor_total_venda,
    )
    db.session.add(venda)
    db.session.flush()  # garante venda.id antes de criar os itens

    # 3. Cria os itens detalhados e 4. abate do estoque
    for item in itens_detalhados:
        produto = item["produto"]
        quantidade = item["quantidade"]

        db.session.add(
            VendaProduto(
                id_venda=venda.id,
                id_produto=produto.id,
                qtd_produto=quantidade,
                valor_unitario=produto.preco,
                valor_total=item["subtotal"],
            )
        )

        estoques_por_produto[produto.id].qtd_atual -= quantidade

    db.session.commit()
    return venda
