from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from umarket.extensions import db
from umarket.models.pdv import Pdv
from umarket.models.produto import Produto
from umarket.models.venda import Venda
from umarket.services import carrinho_service, venda_service

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/")
def index():
    destaques = Produto.query.limit(4).all()
    return render_template("cliente/index.html", destaques=destaques)


@cliente_bp.route("/catalogo")
def catalogo():
    busca = request.args.get("q", "").strip()
    classificacao = request.args.get("classificacao", "").strip()

    query = Produto.query
    if busca:
        query = query.filter(Produto.nome.ilike(f"%{busca}%"))
    if classificacao:
        query = query.filter(Produto.classificacao == classificacao)

    produtos = query.order_by(Produto.nome).all()
    classificacoes = [
        c[0] for c in db.session.query(Produto.classificacao).distinct() if c[0]
    ]

    return render_template(
        "cliente/catalogo.html",
        produtos=produtos,
        classificacoes=classificacoes,
        busca=busca,
        classificacao_atual=classificacao,
    )


@cliente_bp.route("/produto/<int:id_produto>")
def produto_detalhe(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    return render_template("cliente/produto.html", produto=produto)


@cliente_bp.route("/carrinho")
def carrinho():
    itens = carrinho_service.montar_itens_detalhados()
    total = carrinho_service.calcular_total(itens)
    return render_template("cliente/carrinho.html", itens=itens, total=total)


@cliente_bp.route("/carrinho/adicionar/<int:id_produto>", methods=["POST"])
def carrinho_adicionar(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    quantidade = max(1, int(request.form.get("quantidade", 1)))
    carrinho_service.adicionar_item(produto.id, quantidade)
    flash(f'"{produto.nome}" adicionado ao carrinho.', "success")
    return redirect(request.referrer or url_for("cliente.catalogo"))


@cliente_bp.route("/carrinho/atualizar/<int:id_produto>", methods=["POST"])
def carrinho_atualizar(id_produto):
    quantidade = int(request.form.get("quantidade", 1))
    carrinho_service.atualizar_quantidade(id_produto, quantidade)
    return redirect(url_for("cliente.carrinho"))


@cliente_bp.route("/carrinho/remover/<int:id_produto>", methods=["POST"])
def carrinho_remover(id_produto):
    carrinho_service.remover_item(id_produto)
    flash("Item removido do carrinho.", "info")
    return redirect(url_for("cliente.carrinho"))


@cliente_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    itens = carrinho_service.montar_itens_detalhados()
    if not itens:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("cliente.catalogo"))

    total = carrinho_service.calcular_total(itens)
    pdvs = Pdv.query.order_by(Pdv.nome).all()

    if request.method == "POST":
        id_pdv = request.form.get("id_pdv", type=int)
        forma_pagamento = request.form.get("forma_pagamento", "").strip()

        if not id_pdv or not forma_pagamento:
            flash("Selecione o ponto de venda e a forma de pagamento.", "danger")
            return render_template(
                "cliente/checkout.html", itens=itens, total=total, pdvs=pdvs
            )

        try:
            venda = venda_service.finalizar_compra(
                id_usuario=current_user.id,
                id_pdv=id_pdv,
                forma_pagamento=forma_pagamento,
                itens_detalhados=itens,
            )
        except venda_service.EstoqueInsuficienteError as erro:
            db.session.rollback()
            flash(str(erro), "danger")
            return render_template(
                "cliente/checkout.html", itens=itens, total=total, pdvs=pdvs
            )

        carrinho_service.limpar_carrinho()
        flash(f"Compra #{venda.id} finalizada com sucesso!", "success")
        return redirect(url_for("cliente.historico"))

    return render_template("cliente/checkout.html", itens=itens, total=total, pdvs=pdvs)


@cliente_bp.route("/historico")
@login_required
def historico():
    vendas = (
        Venda.query.filter_by(id_usuario=current_user.id)
        .order_by(Venda.data.desc())
        .all()
    )
    return render_template("cliente/historico.html", vendas=vendas)


@cliente_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    if request.method == "POST":
        current_user.nome = request.form.get("nome", current_user.nome).strip()
        nova_senha = request.form.get("nova_senha", "").strip()
        if nova_senha:
            current_user.set_senha(nova_senha)
        db.session.commit()
        flash("Dados atualizados com sucesso.", "success")
        return redirect(url_for("cliente.perfil"))

    return render_template("cliente/perfil.html")
