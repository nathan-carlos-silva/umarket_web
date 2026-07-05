"""
Testes de smoke: garantem que as rotas publicas respondem sem erro de servidor.
Requer um banco de testes configurado via DATABASE_URL (pode ser o mesmo banco
de desenvolvimento em ambiente academico).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from umarket.app import create_app
from umarket.config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client


def test_index_ok(client):
    resposta = client.get("/")
    assert resposta.status_code == 200


def test_catalogo_ok(client):
    resposta = client.get("/catalogo")
    assert resposta.status_code == 200


def test_login_get_ok(client):
    resposta = client.get("/login")
    assert resposta.status_code == 200


def test_checkout_exige_login(client):
    resposta = client.get("/checkout")
    assert resposta.status_code in (302, 401)
