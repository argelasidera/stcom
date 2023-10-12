from sqlalchemy import DateTime
from app.extensions import db
import datetime
from app.extensions import bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields
from app.models.role_permission import RoleSchema


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="SET NULL"))
    role = db.relationship("Role")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
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


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        exclude = ("password",)

    id = auto_field()
    email = auto_field()
    name = auto_field()
    role_id = auto_field()
    created_by = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
    delete_at = auto_field()
    role = fields.Nested(RoleSchema)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
