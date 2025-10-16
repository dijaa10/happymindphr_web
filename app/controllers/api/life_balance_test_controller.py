from flask import request
from app.config import db,session,jwt
from app.formula.life_balance_test import calculate_test
from app.models.Mahasiswa import Mahasiswa
from app.models.LifeBalanceTest import LifeBalanceTest
from app.models.LifeBalanceDetailTest import LifeBalanceDetailTest
from app.models.LifeBalanceQuestion import LifeBalanceQuestion
from app.models.LifeBalanceAnswer import LifeBalanceAnswer
from app.helpers.response_factory import response_data
from flask_jwt_extended import jwt_required, current_user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    try:
        identity = jwt_data["sub"]
        return identity
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction on error


@jwt_required()
def get_q_data():
    """Get Dass21 Question """
    if Mahasiswa.mahasiswa_header_check(request):
        question = db.session.query(LifeBalanceQuestion).all()
        data = list(map(lambda l: l.to_dict(), question))
        session.close()
        return response_data(data)

@jwt_required()
def get_a_data():
    """Get Life Balance Answer """
    if Mahasiswa.mahasiswa_header_check(request):
        answer = db.session.query(LifeBalanceAnswer).all()
        data = list(map(lambda l: l.to_dict(), answer))
        session.close()
        return response_data(data)

@jwt_required()
def send_question_data():
    # Save the data into database
    if Mahasiswa.mahasiswa_header_check(request):
        data = request.json
        new_life_balance_test = LifeBalanceTest(
            id_mahasiswa=current_user,
            waktu_mulai=data["waktu_mulai"],
            waktu_selesai=data["waktu_selesai"],
        )
        session.add(new_life_balance_test)
        session.commit()
        new_id = new_life_balance_test.id
        
        session.close()

         #save to database 
        for item in data['question_data']:
            session.add(
                LifeBalanceDetailTest(
                    id_test=new_id,
                    no_life_balance_q=item['question_no'],
                    no_life_balance_a =item['answer_no'],
                )
            )
            session.commit()
        life_balance_test_data = calculate_test(data['question_data'])
        #update life balance test 
        update_data = session.query(LifeBalanceTest).filter_by(id=new_id).first()
        update_data.total_nilai = life_balance_test_data
        session.commit()
        session.close()
        # return response_message(f"Data berhasil di analisa")
        return response_data(life_balance_test_data)