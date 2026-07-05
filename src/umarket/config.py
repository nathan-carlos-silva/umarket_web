import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-nao-use-em-producao")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/umarket"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Nome da chave de sessao usada para guardar o carrinho de compras
    CARRINHO_SESSION_KEY = "carrinho"
