from flask import jsonify
from app.config import session


def response_message(message=str, status_code=200):
    """

    :param status_code:
    :param message str:
    :return jsonify:
    """
    res = {
        'status': 'success',
        'message': message
    }
    return res, status_code


def response_data(data=None, status_code=200):
    """

    :param status_code:
    :param list data:
    :return jsonify:
    """
    if data is None:
        data = {}
    res = {
        'status': 'success',
        'data': data
    }
    return res, status_code


def response_with_data(data=None, status_code=200):
    """

    :param status_code:
    :param list data:
    :return jsonify:
    """
    if data is None:
        data = {}
    res = {
        'status': 'success',
        'data': jsonify(data)
    }
    return jsonify(res), status_code


def err_response(message='', status_code=401):
    """

    :param status_code:
    :param message:
    :return:
    """
    res = {
        'error': 'true',
        'message': message
    }
    return jsonify(res), status_code

def validation_error_response(error_info='', status_code=401):
    """

    :param status_code:
    :param error_info:
    :return:
    """
    res = {
        'error': 'true',
        'error_info': error_info
    }
    return jsonify(res), status_code

