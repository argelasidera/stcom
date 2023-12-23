import uuid
import os
from flask import Blueprint, request
from app.utils import private_route, res_bad_request, res_success, res_server_error

bp = Blueprint("upload-file", __name__)

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
            # filename = secure_filename(file.filename)
            file_ext = file.filename.rsplit(".", 1)[1]
            filename = f"{uuid.uuid4()}.{file_ext}"
            file.save(os.path.join(UPLOADS_PATH, filename))

            return res_success(
                message="File successfully uploaded.",
                data={"file_name": filename},
            )

        return res_bad_request(message="No file found.")
    except Exception as e:
        print(e)
        return res_server_error()
