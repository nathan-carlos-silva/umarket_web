from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from umarket.extensions import db
from umarket.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        cpf = request.form.get("cpf", "").strip()
        data_nasc = request.form.get("data_nasc", "").strip()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        erros = []
        if not nome or not email or not cpf or not senha:
            erros.append("Preencha todos os campos obrigatórios.")
        if senha != confirmar_senha:
            erros.append("As senhas não coincidem.")
        if Usuario.query.filter_by(email=email).first():
            erros.append("Já existe uma conta com este e-mail.")
        if Usuario.query.filter_by(cpf=cpf).first():
            erros.append("Já existe uma conta com este CPF.")

        if erros:
            for erro in erros:
                flash(erro, "danger")
            return render_template("cliente/cadastro.html", form=request.form)

        usuario = Usuario(
            nome=nome,
            email=email,
            cpf=cpf,
            data_nasc=datetime.strptime(data_nasc, "%Y-%m-%d").date()
            if data_nasc
            else None,
        )
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("cliente/cadastro.html", form={})


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.checar_senha(senha):
            login_user(usuario)
            flash(f"Bem-vindo de volta, {usuario.nome}!", "success")
            destino = request.args.get("next") or url_for("cliente.index")
            return redirect(destino)

        flash("E-mail ou senha inválidos.", "danger")

    return render_template("cliente/login.html")


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.checar_senha(senha) and usuario.is_admin:
            login_user(usuario)
            flash(f"Bem-vindo ao painel administrativo, {usuario.nome}!", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Credenciais inválidas ou usuário sem permissão de administrador.", "danger")

    return render_template("admin/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    era_admin = current_user.is_admin
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("auth.admin_login") if era_admin else url_for("cliente.index"))
