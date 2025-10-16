from pydantic import ValidationError
from app.models.Mahasiswa import Mahasiswa
from app.models.Musik import Musik
from flask import request
from flask_jwt_extended import jwt_required, current_user
from app.helpers.convert_type import object_as_dict,get_string_word_total
from app.config import session,jwt
from app.helpers.response_factory import response_data,validation_error_response,response_message

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        identity = jwt_data["sub"]
        return session.query(Mahasiswa).filter_by(id=identity).first()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction on error


@jwt_required()
def data_musik():
    if Mahasiswa.mahasiswa_header_check(request):
        musik = session.query(Musik).all()
        data = list(map(lambda l: l.to_dict(), musik))
        return response_data(data)
