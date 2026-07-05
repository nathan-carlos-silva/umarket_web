from umarket.extensions import db


class Estoque(db.Model):
    __tablename__ = "estoque"

    id_pdv = db.Column(db.Integer, db.ForeignKey("pdv.id"), primary_key=True)
    id_produto = db.Column(
        db.Integer, db.ForeignKey("produtos.id"), primary_key=True
    )
    qtd_atual = db.Column(db.Integer, nullable=False, default=0)
    capacidade = db.Column(db.Integer, nullable=False)

    pdv = db.relationship("Pdv", back_populates="estoques")
    produto = db.relationship("Produto", back_populates="estoques")

    def __repr__(self) -> str:
        return f"<Estoque pdv={self.id_pdv} produto={self.id_produto} qtd={self.qtd_atual}>"
