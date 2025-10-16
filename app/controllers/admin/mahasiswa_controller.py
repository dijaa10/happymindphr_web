from flask import render_template, request
import datetime
from sqlalchemy import select
from app.models.Dass21Test import Dass21Test
from app.models.QOLTest import QOLTest
from app.config import session
import sqlalchemy as db
import json
from app.models.Mahasiswa import Mahasiswa
from app.helpers.response_factory import response_data


def show_mahasiswa_data():
    return render_template("admin/mahasiswa/index.html")


def edit_mahasiswa(mahasiswa_id, **kwargs):
    data = session.query(Mahasiswa).filter_by(id=mahasiswa_id).first()
    session.close()
    return render_template("admin/mahasiswa/edit.html", data=data)


def mahasiswa_json_data():
    if request.is_json:
        row_id = 0
        #  {
        #             "id":1+row_id,
        #             "nama": l.nama,
        #             "jenis_kelamin": l.jenis_kelamin,
        #             "nim": l.nim,
        #             "email": l.email,
        #             "tanggal_lahir": l.tanggal_lahir.strftime("%Y-%m-%d"),
        #         }
        mahasiswa = session.execute(
            db.select(
                Mahasiswa.nama,
                Mahasiswa.jenis_kelamin,
                Mahasiswa.nim,
                Mahasiswa.email,
                Mahasiswa.tanggal_lahir,
                Mahasiswa.id,
            )
        ).fetchall()
        print(mahasiswa)
        data = list()
        for item in mahasiswa:
            data.append(
                {
                    "id": item[5],
                    "nama": item[0],
                    "jenis_kelamin": item[1],
                    "nim": item[2],
                    "email": item[3],
                    "tanggal_lahir": (
                        item[4].strftime("%Y-%m-%d") if item[4] != None else ""
                    ),
                }
            )
        session.close()
        return response_data(data)


def mahasiswa_curhat_result_data(mahasiswa_id):
    statment = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Dass21Test.total_nilai,
            Dass21Test.waktu_mulai,
            Dass21Test.waktu_selesai,
            QOLTest.total_nilai,
        )
        .select_from(Mahasiswa)
        .group_by(
            Mahasiswa.id,
            Dass21Test.total_nilai,
            Dass21Test.waktu_mulai,
            QOLTest.total_nilai,
            Dass21Test.waktu_selesai,
        )
        .where(Dass21Test.waktu_mulai == QOLTest.waktu_mulai)
        .where(Mahasiswa.id == mahasiswa_id)
        .where(Dass21Test.waktu_selesai == QOLTest.waktu_selesai)
        .join(Dass21Test, Mahasiswa.id == Dass21Test.id_mahasiswa)
        .join(QOLTest, Mahasiswa.id == QOLTest.id_mahasiswa)
    )
    results = session.execute(statment)
    data = []
    for row in results:
        data.append(
            {
                "mahasiswa_id": row[0],
                "mahasiswa_nama": row[1],
                "dass21_total": row[2],
                "dass21_test_start_time": row[3].strftime("%Y-%m-%d %H:%M:%S"),
                "dass21_test_end_time": row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "qol_total": row[5],
            }
        )
    session.close()
    return response_data(data)
