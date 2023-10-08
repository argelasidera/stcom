import datetime
from sqlalchemy import DateTime
from app.extensions import db


role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey(
        'roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey(
        'permissions.id'), primary_key=True),
)


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Roles "{self.title}">'


class Permissions(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Permissions "{self.title}">'
