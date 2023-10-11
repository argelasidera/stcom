from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_seeder import FlaskSeeder


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
seeder = FlaskSeeder()
