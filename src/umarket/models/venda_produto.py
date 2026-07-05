from umarket.extensions import db


class VendaProduto(db.Model):
    __tablename__ = "vendas_produtos"

    id = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(
        db.Integer, db.ForeignKey("vendas.id", ondelete="CASCADE")
    )
    id_produto = db.Column(db.Integer, db.ForeignKey("produtos.id"))
    qtd_produto = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    venda = db.relationship("Venda", back_populates="itens")
    produto = db.relationship("Produto", back_populates="itens_venda")

    def __repr__(self) -> str:
        return f"<VendaProduto venda={self.id_venda} produto={self.id_produto}>"
