from flask import Blueprint
from app.dto import login_schema
from app.utils import post
from app.utils.custom_response import res_success


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
@post(login_schema)
def login(payload):
    print('payload: ', payload)
    return res_success(message='Login Successful!')
