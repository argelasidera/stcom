from flask import Flask
from config import Config
from dotenv import load_dotenv
from app.extensions import db

load_dotenv()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return '<h1>STCOM API</h1>'

    return app
