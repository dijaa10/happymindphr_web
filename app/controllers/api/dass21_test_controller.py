from flask import request
import json
from app.config import db,session, jwt,db
from app.models.Mahasiswa import Mahasiswa
from app.models.Dass21Question import Dass21Question
from app.models.Dass21Test import Dass21Test
from app.models.Dass21DetailTest import Dass21DetailTest
from app.models.Dass21Answer import Dass21Answer
from app.formula.dass_21_test import test_result
from app.helpers.response_factory import response_data, response_message
from flask_jwt_extended import jwt_required, current_user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        identity = jwt_data["sub"]
        return identity
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()  # Rollback the transaction on error
    finally:
        db.session.close()  # Always close the db.session


def get_q_data():
    """Get Dass21 Question"""
    if Mahasiswa.mahasiswa_header_check(request):
        question = db.session.query(Dass21Question).all()
        data = list(map(lambda l: l.to_dict(), question))
        db.session.close()
        return response_data(data)



def get_a_data():
    """Get Dass21 Answer"""
    answer = db.session.query(Dass21Answer).all()
    data = list(map(lambda l: l.to_dict(), answer))
    db.session.close()
    return response_data(data)


@jwt_required()
def send_question_data():
    # Save the data into database
    if Mahasiswa.mahasiswa_header_check(request):
        data = request.json
        new_dass21_test = Dass21Test(
            id_mahasiswa=current_user,
            waktu_mulai=data["waktu_mulai"],
            waktu_selesai=data["waktu_selesai"],
        )
        db.session.add(new_dass21_test)
        db.session.commit()
        new_id = new_dass21_test.id

        db.session.close()

        # save to database
        for item in data["question_data"]:
            db.session.add(
                Dass21DetailTest(
                    id_test=new_id,
                    no_dass_21_q=item["question_no"],
                    no_dass_21_a=item["answer_no"],
                )
            )
            db.session.commit()

        dass_21_test_data = test_result(data["question_data"])
        # update dass21 data
        update_data = db.session.query(Dass21Test).filter_by(id=new_id).first()
        update_data.total_nilai = dass_21_test_data
        db.session.commit()
        db.session.close()
        # return response_message(f"Data berhasil di analisa")
        return response_data(dass_21_test_data)
