from flask import jsonify


# 200 OK
def res_success(data=None, message='Successful'):
    if data is None:
        return jsonify({
            'message': message,
        }), 200

    return jsonify({
        'message': message,
        'data': data
    }), 200


# 400 Bad Request
def res_bad_request(errors=None, message='Bad Request.'):
    return jsonify({
        'message': message,
        'errors': errors
    }), 400


# 422 Unprocessable Entity
def res_unprocessable_entity(errors, message='Unprocessable Entity.'):
    return jsonify({
        'message': message,
        'errors': errors
    }), 422


# 500 Server Error
def res_server_error(message="Internal Server Error"):
    return jsonify({
        'message': message,
    }), 500
