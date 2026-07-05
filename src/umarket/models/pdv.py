from umarket.extensions import db


class Pdv(db.Model):
    __tablename__ = "pdv"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    endereco = db.Column(db.Text)

    estoques = db.relationship("Estoque", back_populates="pdv", lazy="dynamic")
    vendas = db.relationship("Venda", back_populates="pdv", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Pdv {self.id} {self.nome}>"
