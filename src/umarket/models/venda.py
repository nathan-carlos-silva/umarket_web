from datetime import datetime

from umarket.extensions import db


class Venda(db.Model):
    __tablename__ = "vendas"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    valor = db.Column(db.Numeric(10, 2))
    forma_pagamento = db.Column(db.String(20))
    id_pdv = db.Column(db.Integer, db.ForeignKey("pdv.id"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    pdv = db.relationship("Pdv", back_populates="vendas")
    usuario = db.relationship("Usuario", back_populates="vendas")
    itens = db.relationship(
        "VendaProduto",
        back_populates="venda",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Venda {self.id} usuario={self.id_usuario} valor={self.valor}>"
