# app.py
import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

from config import Config
from extensions import db, login_manager

# Importamos nuestros blueprints
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.graph_routes import graph_bp
from routes.admin_routes import admin_bp

def create_app():
    # Carga variables de entorno desde .env
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(graph_bp)
    app.register_blueprint(admin_bp)

    # Ruta raíz: redirige al login
    @app.route('/')
    def home():
        return redirect(url_for('auth_bp.login_view'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
