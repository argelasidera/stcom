from sqlalchemy import DateTime
from app.extensions import db
import datetime
from app.extensions import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.id', ondelete='SET NULL'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(DateTime)
    delete_at = db.Column(DateTime)

    def __init__(self, email=None, name=None, password=None, role_id=None):
        super().__init__()
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password)
        self.role_id = role_id

    def __repr__(self):
        return f'<Users "{self.email}">'
