from app.requests.mahasiswa_register_schema import MahasiswaRegisterRequest
from app.requests.mahasiswa_login_schema import MahasiswaLoginRequest
from app.requests.mahasiswa_update_account_schema import MahasiswaUpdateRequest
from pydantic import ValidationError
from app.models.Mahasiswa import Mahasiswa
from sqlalchemy import or_
from app.models.OTPCode import OTPCode
from flask import request
from flask_jwt_extended import current_user,jwt_required
from app.helpers.send_email import send_email
from app.helpers.convert_type import object_as_dict
import datetime
import random
from app.config import session, bcrypt,db
from app.helpers.response_factory import (
    response_data,
    validation_error_response,
    response_message,
)


def mahasiswa_register():
    # TODO Validate when data is already exist
    try:
        data = MahasiswaRegisterRequest(**request.json).model_dump()
        check_if_data_already_exist = (
            session.query(Mahasiswa)
            .filter(
                or_(
                    Mahasiswa.nik == data["nik"],
                    Mahasiswa.nim == data["nim"],
                    Mahasiswa.email == data["email"],
                )
            )
            .count()
            > 0
        )
        if check_if_data_already_exist:
            return validation_error_response("Data telah ada", 400)
        session.add(
            Mahasiswa(
                nama=data["nama"],
                nik=data["nik"],
                tanggal_lahir=data["tanggal_lahir"],
                nim=data["nim"],
                alamat=data["alamat"],
                no_hp=data["no_hp"],
                password=data["password"],
                jenis_kelamin=data["jenis_kelamin"],
                email=data["email"],
            )
        )
        session.commit()
        return response_message("Berhasil daftar")
    except ValidationError as e:
        return validation_error_response(e.errors(), 400)


def mahasiswa_login():
    try:
        data = MahasiswaLoginRequest(**request.json).model_dump()
        mahasiswa = session.query(Mahasiswa).filter_by(email=data["email"]).first()
        check_password = bcrypt.check_password_hash(
            mahasiswa.password, data["password"]
        )
        if mahasiswa and check_password:
            token = mahasiswa.encode_auth_token(mahasiswa.id)
            data = {
                "user": {
                    "id": mahasiswa.id,
                    "nama": mahasiswa.nama,
                    "nim": mahasiswa.nim,
                    "nik": mahasiswa.nik,
                    "no_hp": mahasiswa.no_hp,
                    "email": mahasiswa.email,
                    "alamat": mahasiswa.alamat,
                    "jenis_kelamin": mahasiswa.jenis_kelamin,
                    "avatar": mahasiswa.avatar,
                    "tanggal_lahir": mahasiswa.tanggal_lahir.strftime("%Y-%m-%d"),
                },
                "token": token,
            }
            session.close()
            return response_data(data)
        else:
            return validation_error_response(
                "Please check your email and password again", 401
            )

    except ValidationError as e:
        return validation_error_response(e.errors(), 400)


def generate_otp():
    data = request.json
    print(data["email"])
    mahasiswa_data = session.query(Mahasiswa).filter_by(email=data["email"]).first()
    mahasiswa_search = (
        session.query(Mahasiswa).filter_by(email=data["email"]).count() == 0
    )
    now = datetime.datetime.now()

    # otp code is 4 digits random integer
    otp_code = random.randint(1000, 9999)

    # check if email is already exist on database
    if mahasiswa_search:
        return response_message("Email tidak ditemukan", 404)

    # save to database
    save_otp = session.add(
        OTPCode(
            mahasiswa_id=mahasiswa_data.id,
            issued_time=now,
            expired_time=now + datetime.timedelta(minutes=15),
            code=otp_code,
        )
    )
    session.commit()
    session.close()

    message_data = {"mahasiswa_email": data["email"], "token": otp_code}
    send_email(message_data)
    return response_message("Berhasil terkirim")


def send_otp():
    json_input = request.json
    now = datetime.datetime.now()

    # check if code valid
    code_not_found = (
        session.query(OTPCode).filter_by(code=json_input["code"]).count() == 0
    )
    if code_not_found:
        return response_message("Kode tidak valid", 401)

    # check if code expired
    data = session.query(OTPCode).filter_by(code=json_input["code"]).first()
    code_is_expired = now > data.expired_time
    if code_is_expired:
        session.delete(data)
        session.commit()
        session.close()
        return response_message("Kode telah expired", 401)

    session.delete(data)
    session.commit()
    session.close()
    return response_message("Data Valid")


def reset_password():
    input_json = request.json

    # check if new password != confirm password
    if input_json["new_password"] != input_json["confirm_password"]:
        return response_message("Konfirmasi password != password baru", 422)
    mahasiswa = session.query(Mahasiswa).filter_by(email=input_json["email"]).first()
    mahasiswa.password = input_json["new_password"]
    session.commit()
    session.close()
    return response_data("Password berhasil diubah")


@jwt_required()
def update_account():
    try:
        # 1. Validasi dan Konversi data request
        data = MahasiswaUpdateRequest(**request.json).model_dump()
        
        # 2. Ambil data mahasiswa yang sedang login
        mahasiswa = session.query(Mahasiswa).filter_by(id=current_user).first()
        
        if not mahasiswa:
            return validation_error_response("Akun tidak ditemukan.", 404)

        # --- PERBAIKAN LOGIKA KRUSIAL ---
        # 3. Cek apakah email BARU sudah digunakan oleh pengguna LAIN
        is_email_used_by_another = (
            session.query(Mahasiswa)
            .filter(
                Mahasiswa.email == data["email"], # Cari email yang sama
                Mahasiswa.id != current_user       # Tapi ID-nya berbeda dari user saat ini
            )
            .first() # Gunakan .first() untuk efisiensi
        )

        if is_email_used_by_another:
            # Mengembalikan error 409 Conflict
            return validation_error_response("Email sudah digunakan oleh pengguna lain.", 409) 
        
        # 4. (Opsional) Cek jika tidak ada kolom yang benar-benar diubah
        # Jika semua data sama persis, Anda bisa menghentikan proses
        if (mahasiswa.nama == data["nama"] and 
            mahasiswa.nim == data["nim"] and 
            mahasiswa.jenis_kelamin == data["jenis_kelamin"] and 
            mahasiswa.email == data["email"] and
            mahasiswa.avatar == data.get("avatar")):
            return response_message("Tidak ada perubahan yang dilakukan pada akun.", 200)


        # 5. Lakukan Pembaruan
        mahasiswa.nama = data["nama"]
        mahasiswa.nim = data["nim"]
        mahasiswa.jenis_kelamin = data["jenis_kelamin"]
        mahasiswa.email = data["email"]
        mahasiswa.avatar = data.get("avatar")
        
        # 6. Komit ke database
        session.commit()
        session.close()
        
        return response_message("Data akun berhasil diubah")
        
    except ValidationError as e:
        # Menangani kesalahan dari Pydantic (data input tidak valid)
        return validation_error_response(e.errors(), 400)
    
    except Exception as e:
        # Menangani kesalahan umum lainnya
        session.rollback() # Pastikan rollback jika terjadi error saat commit
        return validation_error_response(f"Terjadi kesalahan server: {e}", 500)


@jwt_required()
def update_password():
    input_json = request.json
    mahasiswa = session.query(Mahasiswa).filter_by(id=current_user).first()
    check_if_password_matched = bcrypt.check_password_hash(mahasiswa.password,input_json['current_password']) != True
    check_if_confirmation_password_matched = input_json['new_password'] != input_json['confirm_password']
    if check_if_password_matched:
        return validation_error_response("Password saat ini tidak cocok",422)
    if check_if_confirmation_password_matched:
        return validation_error_response("Konfirmasi password tidak sama",422)
    mahasiswa.password = input_json["new_password"]
    session.commit()
    session.close()
    return response_data("Password berhasil diubah")
    
