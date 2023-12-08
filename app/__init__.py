import os
from flask import Flask, send_from_directory
from config import Config
from dotenv import load_dotenv
from flask_cors import CORS
from app.extensions import db, migrate, bcrypt, seeder
from app import models


# Blueprints
from app.routes import auth_bp, users_bp, roles_bp, categories_bp, permissions_bp

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app._static_folder = "static"
    app.config.from_object(config_class)
    CORS(app)

    # Initialize Flask extensions here

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    seeder.init_app(app, db)

    # Register blueprints here
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(roles_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(permissions_bp)

    @app.route("/uploads/<path:name>")
    def serve_static(name):
        print(os.getcwd())
        root_dir = os.path.dirname(os.getcwd())
        return send_from_directory(
            os.path.join(root_dir, "stcom-api", "static", "uploads"), name
        )

    @app.route("/")
    def index():
        return "<h1>STCOM API</h1>"

    return app
