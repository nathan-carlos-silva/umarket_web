from flask import Flask
from flask_migrate import Migrate

from umarket.config import Config
from umarket.extensions import db, login_manager


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)

    from umarket.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from umarket.routes.admin import admin_bp
    from umarket.routes.auth import auth_bp
    from umarket.routes.cliente import cliente_bp

    app.register_blueprint(cliente_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def contexto_global():
        from umarket.services import carrinho_service

        return {"qtd_itens_carrinho": carrinho_service.contar_itens()}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
