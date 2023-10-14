import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from sqlalchemy import DateTime
from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)
    tag = db.Column(db.String(120))
    description = db.Column(db.Text())
    file_name = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(DateTime)

    def __init__(
        self,
        title=None,
        date=None,
        tag=None,
        description=None,
        file_name=None,
        created_by=None,
    ) -> None:
        super().__init__()
        self.title = title
        self.date = date
        self.tag = tag
        self.description = description
        self.file_name = file_name
        self.created_by = created_by

    def __repr__(self):
        return f'<Categories "{self.title}">'


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category

    id = auto_field()
    title = auto_field()
    date = auto_field()
    tag = auto_field()
    description = auto_field()
    file_name = auto_field()
    created_by = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
