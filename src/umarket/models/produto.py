from umarket.extensions import db

# Cor de destaque por categoria, usada no placeholder visual quando o
# produto ainda nao tem uma imagem cadastrada (imagem_url vazio)
CATEGORIA_CORES = {
    "Bebidas": "#0d6efd",
    "Alimentos": "#fd7e14",
    "Mercearia": "#6f42c1",
    "Doces": "#d63384",
    "Snacks": "#20c997",
    "Lanches": "#dc3545",
}
COR_PADRAO = "#6c757d"


class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    classificacao = db.Column(db.String(40))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    imagem_url = db.Column(db.String(255))  # adicionado via migrations/003

    estoques = db.relationship("Estoque", back_populates="produto", lazy="dynamic")
    itens_venda = db.relationship(
        "VendaProduto", back_populates="produto", lazy="dynamic"
    )

    @property
    def qtd_total_estoque(self) -> int:
        """Soma do estoque deste produto em todos os PDVs."""
        return sum(e.qtd_atual for e in self.estoques)

    @property
    def cor_categoria(self) -> str:
        return CATEGORIA_CORES.get(self.classificacao, COR_PADRAO)

    @property
    def iniciais(self) -> str:
        palavras = self.nome.split()
        letras = "".join(p[0] for p in palavras[:2] if p)
        return letras.upper() or "?"

    def __repr__(self) -> str:
        return f"<Produto {self.id} {self.nome}>"