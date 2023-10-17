import os
from os import path
from flask import Blueprint, request
from werkzeug.utils import secure_filename
from app.utils import res_bad_request, res_success, res_not_found, res_server_error
from app.utils import post, put, private_route
from app.models import Category, category_schema_factory
from app.dto import createCategoryDTO, updateCategoryDTO
from app.extensions import db


bp = Blueprint("categories", __name__, url_prefix="/categories")


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
UPLOADS_PATH = "./static/uploads"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/file", methods=["POST"])
@private_route()
def upload_category_file():
    try:
        print(request.files)
        if "file" not in request.files:
            return res_bad_request(message="No file found.")

        file = request.files["file"]

        if file.filename == "":
            return res_bad_request(message="No file found.")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOADS_PATH, filename))

        return res_success(message="File successfully uploaded.")
    except Exception as e:
        print(e)
        return res_server_error()


@bp.route("", methods=["GET"])
@private_route("view-category")
def get_categories():
    schema = category_schema_factory(many=True)
    categories = Category.query.all()
    return res_success(data={"categories": schema.dump(categories)})


@bp.route("/<int:id>", methods=["GET"])
@private_route("view-category")
def get_category(id):
    schema = category_schema_factory()
    category = Category.query.filter_by(id=id).first()
    if not category:
        return res_not_found(message="Category not found.")
    return res_success(data={"category": schema.dump(category)})


@bp.route("", methods=["POST"])
@private_route("add-category", show_loggedin_user=True)
@post(createCategoryDTO)
def create_category(payload, loggedin_user):
    category = Category(
        title=payload.get("title"),
        date=payload.get("date"),
        tag=payload.get("tag"),
        description=payload.get("description"),
        file_name=payload.get("file_name"),
        created_by=loggedin_user.id,
    )

    db.session.add(category)
    db.session.commit()

    return res_success(message="Category successfully created.")


@bp.route("/<int:id>", methods=["PUT"])
@private_route("edit-user")
@put(updateCategoryDTO)
def update_category(payload, id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return res_not_found("Category not found.")

    category.title = payload.get("title")
    category.date = payload.get("date")
    category.tag = payload.get("tag")
    category.description = payload.get("description")
    category.file_name = payload.get("file_name")
    db.session.commit()

    return res_success(message="Category updated successfully.")


@bp.route("/<int:id>", methods=["PUT"])
@private_route("delete-category")
def delete_category(id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return res_not_found("Category not found.")

    db.session.delete(category)
    db.session.commit()

    return res_success(message="Category delete successfully.")
