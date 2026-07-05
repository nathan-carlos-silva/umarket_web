from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from umarket.extensions import db
from umarket.models.estoque import Estoque
from umarket.models.pdv import Pdv
from umarket.models.produto import Produto
from umarket.models.usuario import Usuario
from umarket.models.venda import Venda

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    total_produtos = Produto.query.count()
    total_usuarios = Usuario.query.count()
    total_vendas = Venda.query.count()
    faturamento_total = db.session.query(db.func.sum(Venda.valor)).scalar() or 0
    ultimas_vendas = Venda.query.order_by(Venda.data.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_produtos=total_produtos,
        total_usuarios=total_usuarios,
        total_vendas=total_vendas,
        faturamento_total=faturamento_total,
        ultimas_vendas=ultimas_vendas,
    )


# ---------- Produtos (RF10, RF11, RF12, RF13) ----------

@admin_bp.route("/produtos")
@admin_required
def produtos():
    lista = Produto.query.order_by(Produto.nome).all()
    return render_template("admin/produtos.html", produtos=lista)


@admin_bp.route("/produtos/novo", methods=["POST"])
@admin_required
def produto_criar():
    produto = Produto(
        imagem_url=request.form.get("imagem_url", "").strip() or None,
        nome=request.form.get("nome", "").strip(),
        classificacao=request.form.get("classificacao", "").strip(),
        preco=request.form.get("preco", type=float, default=0),
    )
    db.session.add(produto)
    db.session.commit()
    flash(f'Produto "{produto.nome}" cadastrado.', "success")
    return redirect(url_for("admin.produtos"))


@admin_bp.route("/produtos/<int:id_produto>/editar", methods=["POST"])
@admin_required
def produto_editar(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    produto.nome = request.form.get("nome", produto.nome).strip()
    produto.classificacao = request.form.get("classificacao", produto.classificacao).strip()
    produto.preco = request.form.get("preco", type=float, default=produto.preco)
    produto.imagem_url=request.form.get("imagem_url", "").strip() or None,
    db.session.commit()
    flash(f'Produto "{produto.nome}" atualizado.', "success")
    return redirect(url_for("admin.produtos"))


@admin_bp.route("/produtos/<int:id_produto>/excluir", methods=["POST"])
@admin_required
def produto_excluir(id_produto):
    produto = Produto.query.get_or_404(id_produto)
    nome = produto.nome
    db.session.delete(produto)
    db.session.commit()
    flash(f'Produto "{nome}" removido.', "info")
    return redirect(url_for("admin.produtos"))


# ---------- Categorias (RF15) ----------
# Nao existe tabela "categorias" no dump: classificacao e um campo texto
# livre em PRODUTOS. Renomear uma "categoria" = atualizar em lote todos os
# produtos que compartilham aquele valor de classificacao.

@admin_bp.route("/categorias")
@admin_required
def categorias():
    resultado = (
        db.session.query(Produto.classificacao, db.func.count(Produto.id))
        .group_by(Produto.classificacao)
        .all()
    )
    lista = [{"nome": nome or "Sem categoria", "qtd_produtos": qtd} for nome, qtd in resultado]
    return render_template("admin/categorias.html", categorias=lista)


@admin_bp.route("/categorias/renomear", methods=["POST"])
@admin_required
def categoria_renomear():
    nome_atual = request.form.get("nome_atual", "").strip()
    nome_novo = request.form.get("nome_novo", "").strip()
    if nome_atual and nome_novo:
        Produto.query.filter_by(classificacao=nome_atual).update(
            {"classificacao": nome_novo}
        )
        db.session.commit()
        flash(f'Categoria "{nome_atual}" renomeada para "{nome_novo}".', "success")
    return redirect(url_for("admin.categorias"))


# ---------- Estoque (RF14) ----------

@admin_bp.route("/estoque")
@admin_required
def estoque():
    id_pdv_filtro = request.args.get("id_pdv", type=int)
    query = Estoque.query
    if id_pdv_filtro:
        query = query.filter_by(id_pdv=id_pdv_filtro)

    lista = query.join(Produto).order_by(Produto.nome).all()
    pdvs = Pdv.query.order_by(Pdv.nome).all()
    return render_template(
        "admin/estoque.html", estoques=lista, pdvs=pdvs, id_pdv_filtro=id_pdv_filtro
    )


@admin_bp.route("/estoque/<int:id_pdv>/<int:id_produto>/atualizar", methods=["POST"])
@admin_required
def estoque_atualizar(id_pdv, id_produto):
    registro = Estoque.query.get_or_404((id_pdv, id_produto))
    nova_qtd = request.form.get("qtd_atual", type=int)
    nova_capacidade = request.form.get("capacidade", type=int)

    if nova_qtd is not None:
        registro.qtd_atual = max(0, nova_qtd)
    if nova_capacidade is not None:
        registro.capacidade = max(1, nova_capacidade)

    db.session.commit()
    flash("Estoque atualizado.", "success")
    return redirect(url_for("admin.estoque"))


# ---------- Usuários (RF17) ----------

@admin_bp.route("/usuarios")
@admin_required
def usuarios():
    lista = Usuario.query.order_by(Usuario.nome).all()
    return render_template("admin/usuarios.html", usuarios=lista)


@admin_bp.route("/usuarios/<int:id_usuario>/alternar-admin", methods=["POST"])
@admin_required
def usuario_alternar_admin(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    if usuario.id == current_user.id:
        flash("Você não pode alterar sua própria permissão de administrador.", "warning")
    else:
        usuario.is_admin = not usuario.is_admin
        db.session.commit()
        flash(f'Permissão de administrador de "{usuario.nome}" atualizada.', "success")
    return redirect(url_for("admin.usuarios"))


# ---------- Pedidos (RF16) ----------

@admin_bp.route("/pedidos")
@admin_required
def pedidos():
    id_pdv_filtro = request.args.get("id_pdv", type=int)
    query = Venda.query
    if id_pdv_filtro:
        query = query.filter_by(id_pdv=id_pdv_filtro)

    vendas = query.order_by(Venda.data.desc()).all()
    pdvs = Pdv.query.order_by(Pdv.nome).all()
    return render_template(
        "admin/pedidos.html", vendas=vendas, pdvs=pdvs, id_pdv_filtro=id_pdv_filtro
    )
