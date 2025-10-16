from flask import request
import json
from app.config import db, session, jwt
from app.models.Mahasiswa import Mahasiswa
from app.models.QOLQuestion import QOLQuestion
from app.models.QOLTest import QOLTest
from app.models.QOLDetailTest import QOLDetailTest
from app.models.QOLAnswer import QOLAnswer
from app.formula.quality_of_life import calculate_test
from app.helpers.response_factory import response_data
from flask_jwt_extended import jwt_required, current_user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity


@jwt_required()
def get_q_data():
    """Get Quality of Life Question"""
    if Mahasiswa.mahasiswa_header_check(request):
        question = db.session.query(QOLQuestion).all()
        data = list(map(lambda l: l.to_dict(), question))
        session.close()
        return response_data(data)


@jwt_required()
def get_a_data():
    """Get Quality Of Life Answer"""
    if Mahasiswa.mahasiswa_header_check(request):
        answer = db.session.query(QOLAnswer).all()
        data = list(map(lambda l: l.to_dict(), answer))
        session.close()
        return response_data(data)


@jwt_required()
def send_question_data():
    data = request.json
    new_qol_test = QOLTest(
        id_mahasiswa=current_user,
        waktu_mulai=data["waktu_mulai"],
        waktu_selesai=data["waktu_selesai"],
    )
    session.add(new_qol_test)
    session.commit()
    new_id = new_qol_test.id
    session.close()

    for item in data['question_data']:
            session.add(
                QOLDetailTest(
                    id_test=new_id,
                    no_qol_q=item['question_no'],
                    no_qol_a =item['answer_no'],
                )
            )
            session.commit()
    qol_test_data = calculate_test(data['question_data'])
    #update quality of life test 
    update_data = session.query(QOLTest).filter_by(id=new_id).first()
    update_data.total_nilai = qol_test_data
    session.commit()
    session.close()
    # return response_message(f"Data berhasil di analisa")
    return response_data(qol_test_data)

