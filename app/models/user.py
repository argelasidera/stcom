from sqlalchemy import *
from app.extensions import db
import datetime


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

    def __repr__(self):
        return f'<Users "{self.email}">'
