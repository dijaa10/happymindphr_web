from pydantic import ValidationError
from app.models.Mahasiswa import Mahasiswa
from sqlalchemy import asc
from app.models.PertanyaanCurhat import PertanyaanCurhat
from app.models.CurhatDetail import CurhatDetail
from app.helpers.seach_curhat_category import find_highest_category
from app.models.Curhat import Curhat
import datetime
from flask import request
from flask_jwt_extended import jwt_required, current_user
from app.helpers.convert_type import object_as_dict, get_string_word_total
from app.config import db, session, bcrypt, jwt
from app.helpers.response_factory import (
    response_data,
    validation_error_response,
    response_message,
)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return identity


@jwt_required()
def mulai_curhat():
    if Mahasiswa.mahasiswa_header_check(request):
        waktu_selesai_curhat_is_empty = (
            db.session.query(Curhat)
            .filter_by(id_mahasiswa=current_user, waktu_selesai=None)
            .count()
            == 0
        )
        print(waktu_selesai_curhat_is_empty)
        if waktu_selesai_curhat_is_empty:
            db.session.add(
                Curhat(
                    id_mahasiswa=current_user
                )
            )
            
        pertanyaan = (
            db.session.query(PertanyaanCurhat).filter_by(topik="awalan", urutan=1).first()
        )
        db.session.commit()
        data = object_as_dict(pertanyaan)
        db.session.close()
        return response_data(data)


@jwt_required()
def kirim_awalan_curhat():
    if Mahasiswa.mahasiswa_header_check(request):
        
        data = request.get_json()
        message = data["message"]
        # insert curhat detail
        pertanyaan = (
            db.session.query(PertanyaanCurhat).filter_by(topik="awalan", urutan=1).first()
        )
        curhat = (
            db.session.query(Curhat)
            .filter_by(id_mahasiswa=current_user, waktu_selesai=None)
            .first()
        )
        print(curhat)
        db.session.add(
            CurhatDetail(
                id_curhat=curhat.id, id_pertanyaan_curhat=pertanyaan.id, jawaban=message
            )
        )
        db.session.commit()
        # session.close()
        word_highest, count = find_highest_category(message)
        pertanyaan = (
            db.session.query(PertanyaanCurhat)
            .filter_by(topik=word_highest)
            .order_by(asc(PertanyaanCurhat.urutan))
            .all()
        )
        data = list(map(lambda l: l.to_dict(), pertanyaan))
        res = {
            "status": "success",
            "curhat_response": f"Jadi, sepertinya kamu lagi ada masalah tentang keadaan {word_highest.replace('_',' ')} kamu, yaa 😌. Tenang, hal kayak gini tuh wajar banget kok, apalagi kalau lagi banyak pikiran atau adaptasi. Yuk, coba jawab beberapa pertanyaan berikut biar aku bisa bantu kamu nemuin cara terbaik buat ngatasinnya 🌱",
            "data": data,
        }
        db.session.close()
        return res, 200


@jwt_required()
def batal_curhat():
    if Mahasiswa.mahasiswa_header_check(request):
        db.session.query(Curhat).filter_by(
            id_mahasiswa=current_user, waktu_selesai=None
        ).delete()
        db.session.commit()
        return response_message("Curhat dibatalkan")


@jwt_required()
def kirim_pesan_screening():
    if Mahasiswa.mahasiswa_header_check(request):
        data = request.get_json()
        q_data_input = data["question_data"]
        curhat = (
            db.session.query(Curhat)
            .filter_by(id_mahasiswa=current_user, waktu_selesai=None)
            .first()
        )
        for q_data in q_data_input:
            db.session.add(
                CurhatDetail(
                    id_curhat=curhat.id,
                    id_pertanyaan_curhat=q_data["question_id"],
                    jawaban=q_data["answer"],
                )
            )
            db.session.commit()
        curhat.waktu_mulai = data['waktu_mulai']
        curhat.waktu_selesai = data['waktu_selesai']
        db.session.commit()
        return response_message("Data telah terkirim")
