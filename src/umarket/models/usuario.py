from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from umarket.extensions import db


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    data_nasc = db.Column(db.Date)
    cpf = db.Column(db.Numeric(11, 0), unique=True, nullable=False)

    # Colunas adicionadas via migrations/001_alter_usuarios_auth.sql
    senha_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    vendas = db.relationship("Venda", back_populates="usuario", lazy="dynamic")

    def set_senha(self, senha_texto_puro: str) -> None:
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def checar_senha(self, senha_texto_puro: str) -> bool:
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha_texto_puro)

    def __repr__(self) -> str:
        return f"<Usuario {self.id} {self.email}>"
