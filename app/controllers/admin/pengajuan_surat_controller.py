from flask import render_template, request, redirect, url_for
from app.models.Mahasiswa import Mahasiswa
from urllib.parse import quote_plus
from app.models.LifeBalanceTest import LifeBalanceTest
from sqlalchemy import select
from app.models.Dass21Test import Dass21Test
from app.helpers.response_factory import response_data
from app.config import session


def index():
    return render_template("admin/pengajuan_surat/index.html")


def pengajuan_surat_json_data():
    statment = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Dass21Test.total_nilai,
            Dass21Test.waktu_mulai,
            Dass21Test.waktu_selesai,
            LifeBalanceTest.total_nilai
        )
        .select_from(Mahasiswa)
        .group_by(Mahasiswa.id,Dass21Test.total_nilai,Dass21Test.waktu_mulai,LifeBalanceTest.total_nilai,Dass21Test.waktu_selesai)
        .where(Dass21Test.waktu_mulai == LifeBalanceTest.waktu_mulai)
        .where(Dass21Test.waktu_selesai == LifeBalanceTest.waktu_selesai)
        .join(Dass21Test, Mahasiswa.id == Dass21Test.id_mahasiswa)
        .join(LifeBalanceTest, Mahasiswa.id == LifeBalanceTest.id_mahasiswa)
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
                "life_balance_total": row[5],
            }
        )
    session.close()
    return response_data(data)

def pengajuan_surat_detail(id_mahasiswa,waktu_mulai):
    print(waktu_mulai)
    statment = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Dass21Test.total_nilai,
            Dass21Test.waktu_mulai,
            Dass21Test.waktu_selesai,
            LifeBalanceTest.total_nilai,
            Mahasiswa.no_hp
        )
        .select_from(Mahasiswa)
        .group_by(Mahasiswa.id,Dass21Test.total_nilai,Dass21Test.waktu_mulai,LifeBalanceTest.total_nilai,Dass21Test.waktu_selesai)
        .join(Dass21Test, Mahasiswa.id == Dass21Test.id_mahasiswa)
        .join(LifeBalanceTest, Mahasiswa.id == LifeBalanceTest.id_mahasiswa)
        .where(Dass21Test.waktu_selesai == LifeBalanceTest.waktu_selesai)
        .where(Mahasiswa.id == id_mahasiswa)
        .where(Dass21Test.waktu_mulai == waktu_mulai)
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
                "life_balance_total": row[5],
                "mahasiswa_no_hp": row[6],
                "message":quote_plus(f"Halo. {row[1]} kamu bisa mengambil surat pada [tanggal]")
            }
        )
    session.close()
    return render_template("admin/pengajuan_surat/detail.html",data=data)
