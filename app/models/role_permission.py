import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import DateTime
from app.extensions import db
from marshmallow import fields


role_permissions = db.Table(
    "role_permissions",
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id"),
        primary_key=True,
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id"),
        primary_key=True,
    ),
)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), nullable=False)
    permissions = db.relationship("Permission", secondary=role_permissions)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name: str = None) -> None:
        super().__init__()
        self.name = name
        self.slug = name.lower().replace(" ", "-")

    def __repr__(self):
        return f'<Roles "{self.name}">'


class Permission(db.Model):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), nullable=False)

    def __init__(self, name: str = None) -> None:
        super().__init__()
        self.name = name
        self.slug = name.lower().replace(" ", "-")

    def __repr__(self):
        return f'<Permissions "{self.name}">'


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True

    id = auto_field()
    name = auto_field()
    slug = auto_field()


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    slug = auto_field()
    permissions = fields.Nested(PermissionSchema, many=True)
    created_at = auto_field()


def role_schema_factory(**kwargs):
    return RoleSchema(**kwargs)


def permission_schema_factory(**kwargs):
    return PermissionSchema(**kwargs)
