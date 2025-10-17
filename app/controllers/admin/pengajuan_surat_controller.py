from flask import render_template, request, redirect, url_for
from app.models.Mahasiswa import Mahasiswa
from urllib.parse import quote_plus
from app.models.LifeBalanceTest import LifeBalanceTest
from sqlalchemy import select
from app.models.Dass21Test import Dass21Test
from app.helpers.response_factory import response_data
from app.config import session
from datetime import datetime


def index():
    return render_template("admin/pengajuan_surat/index.html")


def pengajuan_surat_json_data():
    statment = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Mahasiswa.nim,
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
                "mahasiswa_nim": row[2],
                "dass21_total": row[3],
                "dass21_test_start_time": row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "dass21_test_end_time": row[5].strftime("%Y-%m-%d %H:%M:%S"),
                "life_balance_total": row[6],
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


def print_surat_kesehatan(id_mahasiswa, waktu_mulai):
    # Query data mahasiswa, hasil test DASS21 & Life Balance
    statment = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Mahasiswa.nim,
            Mahasiswa.tanggal_lahir,
            Mahasiswa.alamat,
            LifeBalanceTest.total_nilai.label('life_balance_total'),
            LifeBalanceTest.waktu_selesai.label('lb_waktu_selesai')
        )
        .select_from(Mahasiswa)
        .join(Dass21Test, Mahasiswa.id == Dass21Test.id_mahasiswa)
        .join(LifeBalanceTest, Mahasiswa.id == LifeBalanceTest.id_mahasiswa)
        .where(Dass21Test.waktu_mulai == waktu_mulai)
        .where(Dass21Test.waktu_mulai == LifeBalanceTest.waktu_mulai)
        .where(Dass21Test.waktu_selesai == LifeBalanceTest.waktu_selesai)
        .where(Mahasiswa.id == id_mahasiswa)
    )

    result = session.execute(statment).first()
    session.close()

    if not result:
        return "Data tidak ditemukan", 404

    # Ambil data hasil query
    mahasiswa_id = result[0]
    mahasiswa_nama = result[1]
    mahasiswa_nim = result[2]
    tanggal_lahir_obj = result[3]
    mahasiswa_alamat = result[4]
    life_balance_total = result[5]
    lb_waktu_selesai_obj = result[6]

    # Format bulan dalam Bahasa Indonesia
    bulan_indonesia = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }

    # Konversi tanggal lahir
    if isinstance(tanggal_lahir_obj, str):
        parts = tanggal_lahir_obj.split('-')
        tanggal_lahir_obj = datetime(int(parts[0]), int(parts[1]), int(parts[2]))

    tanggal_lahir_formatted = "{} {} {}".format(
        tanggal_lahir_obj.day,
        bulan_indonesia[tanggal_lahir_obj.month],
        tanggal_lahir_obj.year
    )

    # Usia
    today = datetime.now()
    usia = today.year - tanggal_lahir_obj.year - (
        (today.month, today.day) < (tanggal_lahir_obj.month, tanggal_lahir_obj.day)
    )

    # tanggal pemeriksaan dari waktu selesai LifeBalanceTest
    if isinstance(lb_waktu_selesai_obj, str):
        lb_waktu_selesai_obj = datetime.strptime(lb_waktu_selesai_obj, "%Y-%m-%d %H:%M:%S")

    tanggal_pemeriksaan = "{} {} {}".format(
        lb_waktu_selesai_obj.day,
        bulan_indonesia[lb_waktu_selesai_obj.month],
        lb_waktu_selesai_obj.year
    )

    # Tanggal surat hari ini
    tanggal_surat = "{} {} {}".format(today.day, bulan_indonesia[today.month], today.year)

    # Data untuk halaman print
    data = {
        'nama': mahasiswa_nama,
        'nim': mahasiswa_nim,
        'alamat': mahasiswa_alamat, 
        'tanggal_lahir': tanggal_lahir_formatted,
        'usia': usia,
        'tanggal_pemeriksaan': tanggal_pemeriksaan,
        'tanggal_surat': tanggal_surat,
        'life_balance_total': life_balance_total
    }

    return render_template('admin/pengajuan_surat/pengajuan_surat_print.html', data=data)
