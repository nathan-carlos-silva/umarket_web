"""
Define a senha "123456" (hash) para todos os usuarios de seed que ainda
nao possuem senha_hash preenchido. Rode uma unica vez, depois de aplicar
a migration 001_alter_usuarios_auth.sql.

Uso:
    poetry run python scripts/seed_senhas.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from werkzeug.security import generate_password_hash

from umarket.app import create_app
from umarket.extensions import db
from umarket.models.usuario import Usuario

SENHA_PADRAO = "123456"

app = create_app()

with app.app_context():
    usuarios = Usuario.query.filter(
        (Usuario.senha_hash.is_(None)) | (Usuario.senha_hash == "")
    ).all()

    if not usuarios:
        print("Nenhum usuario pendente de senha. Nada a fazer.")
    else:
        for usuario in usuarios:
            usuario.senha_hash = generate_password_hash(SENHA_PADRAO)
            print(f"Senha definida para: {usuario.email}")

        db.session.commit()
        print(f"\n{len(usuarios)} usuario(s) atualizado(s).")
        print(f'Todos podem logar com a senha: "{SENHA_PADRAO}"')
        print("Admin de teste: nathan@umarket.com")
