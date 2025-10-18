from flask import render_template, request, redirect, url_for, jsonify
from app.models.Mahasiswa import Mahasiswa
from app.models.DataKesehatan import DataKesehatan
from urllib.parse import quote_plus
from app.models.LifeBalanceTest import LifeBalanceTest
from sqlalchemy import select
from app.models.Dass21Test import Dass21Test
from app.helpers.response_factory import response_data
from app.config import session
from datetime import datetime, date
import json


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


def save_data_kesehatan():
    """Endpoint untuk menyimpan data kesehatan dari modal"""
    try:
        data = request.get_json()
        
        if not data or not data.get('mahasiswa_id'):
            return jsonify({'success': False, 'message': 'Data mahasiswa tidak valid'}), 400
        
        today = date.today()
        
        existing = session.query(DataKesehatan).filter(
            DataKesehatan.mahasiswa_id == data['mahasiswa_id'],
            DataKesehatan.tanggal == today
        ).first()
        
        if existing:
            existing.tinggi_badan = float(data.get('tinggi_badan', 0))
            existing.berat_badan = float(data.get('berat_badan', 0))
            existing.tensi_sistolik = int(data.get('tensi_sistolik', 0))
            existing.tensi_diastolik = int(data.get('tensi_diastolik', 0))
        else:
            data_kesehatan = DataKesehatan(
                mahasiswa_id=data['mahasiswa_id'],
                tinggi_badan=float(data.get('tinggi_badan', 0)),
                berat_badan=float(data.get('berat_badan', 0)),
                tensi_sistolik=int(data.get('tensi_sistolik', 0)),
                tensi_diastolik=int(data.get('tensi_diastolik', 0)),
                tanggal=today
            )
            session.add(data_kesehatan)
        
        session.commit()
        session.close()
        
        return jsonify({
            'success': True, 
            'message': 'Data kesehatan berhasil disimpan'
        })
        
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({
            'success': False, 
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500


def print_surat_kesehatan(id_mahasiswa, waktu_mulai):
    statement = (
        select(
            Mahasiswa.id,
            Mahasiswa.nama,
            Mahasiswa.nim,
            Mahasiswa.tanggal_lahir,
            Mahasiswa.alamat,
            Dass21Test.total_nilai,
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

    result = session.execute(statement).first()
    
    if not result:
        session.close()
        return "Data tidak ditemukan", 404

    mahasiswa_nama = result[1]
    mahasiswa_nim = result[2]
    tanggal_lahir_obj = result[3]
    mahasiswa_alamat = result[4]
    dass21_total_json = result[5]
    life_balance_total = result[6]
    lb_waktu_selesai_obj = result[7]

    try:
        if isinstance(dass21_total_json, str):
            dass21_data = json.loads(dass21_total_json)
        else:
            dass21_data = dass21_total_json or {}
    except Exception as e:
        print(f"Error parsing DASS21 JSON: {e}")
        dass21_data = {}
    
    print(f"DASS21 Data: {dass21_data}")
    print(f"Life Balance Total: {life_balance_total}, Type: {type(life_balance_total)}")

    def safe_get_dass21_score(dass21_data, key):
        """
        Ambil nilai score dari DASS21 JSON dengan struktur:
        {"stress": {"level": "Parah", "s_score": 28}, ...}
        """
        if not isinstance(dass21_data, dict):
            return 0
        
        score_field_map = {
            "depression": "d_score",
            "anxiety": "a_score", 
            "stress": "s_score"
        }
        
        score_field = score_field_map.get(key)
        if not score_field:
            return 0
            
        data_item = dass21_data.get(key)
        if isinstance(data_item, dict):
            score = data_item.get(score_field, 0)
            try:
                return float(score) if score else 0
            except:
                return 0
        return 0

    dass21_depression = safe_get_dass21_score(dass21_data, "depression")
    dass21_anxiety = safe_get_dass21_score(dass21_data, "anxiety")
    dass21_stress = safe_get_dass21_score(dass21_data, "stress")

    today_date = date.today()
    data_kesehatan = session.query(DataKesehatan).filter(
        DataKesehatan.mahasiswa_id == id_mahasiswa,
        DataKesehatan.tanggal == today_date
    ).order_by(DataKesehatan.created_at.desc()).first()
    
    if data_kesehatan:
        print(f"Data Kesehatan ditemukan: TB={data_kesehatan.tinggi_badan}, BB={data_kesehatan.berat_badan}, Tensi={data_kesehatan.tensi_lengkap}")
    else:
        print(f"Data Kesehatan TIDAK ditemukan untuk mahasiswa_id={id_mahasiswa} pada tanggal={today_date}")
    
    session.close()

    bulan_indonesia = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }

    if isinstance(tanggal_lahir_obj, str):
        y, m, d = map(int, tanggal_lahir_obj.split('-'))
        tanggal_lahir_obj = datetime(y, m, d)

    tanggal_lahir_formatted = f"{tanggal_lahir_obj.day} {bulan_indonesia[tanggal_lahir_obj.month]} {tanggal_lahir_obj.year}"

    today = datetime.now()
    usia = today.year - tanggal_lahir_obj.year - (
        (today.month, today.day) < (tanggal_lahir_obj.month, tanggal_lahir_obj.day)
    )

    if isinstance(lb_waktu_selesai_obj, str):
        lb_waktu_selesai_obj = datetime.strptime(lb_waktu_selesai_obj, "%Y-%m-%d %H:%M:%S")

    tanggal_pemeriksaan = f"{lb_waktu_selesai_obj.day} {bulan_indonesia[lb_waktu_selesai_obj.month]} {lb_waktu_selesai_obj.year}"
    
    tanggal_surat = f"{today.day} {bulan_indonesia[today.month]} {today.year}"

    def get_dass21_category(score, type_test):
        try:
            score = float(score) * 2 
        except Exception:
            score = 0

        if type_test == 'depression':
            if score <= 9: return "Normal"
            elif score <= 13: return "Ringan"
            elif score <= 20: return "Sedang"
            elif score <= 27: return "Berat"
            else: return "Sangat Berat"
        elif type_test == 'anxiety':
            if score <= 7: return "Normal"
            elif score <= 9: return "Ringan"
            elif score <= 14: return "Sedang"
            elif score <= 19: return "Berat"
            else: return "Sangat Berat"
        elif type_test == 'stress':
            if score <= 14: return "Normal"
            elif score <= 18: return "Ringan"
            elif score <= 25: return "Sedang"
            elif score <= 33: return "Berat"
            else: return "Sangat Berat"
        return "Normal"

    def get_burnout_category(score):
        """Kategori burnout berdasarkan skor life balance"""
        try:
            if isinstance(score, dict):
                score = score.get('total', 0) or score.get('nilai', 0) or 0
            score = float(score) if score else 0
        except:
            score = 0
            
        if score <= 40:
            return "Risiko Rendah"
        elif score <= 60:
            return "Risiko Sedang"
        else:
            return "Risiko Tinggi"

    depression_level = get_dass21_category(dass21_depression, 'depression')
    anxiety_level = get_dass21_category(dass21_anxiety, 'anxiety')
    stress_level = get_dass21_category(dass21_stress, 'stress')
    burnout_level = get_burnout_category(life_balance_total)

    is_psychologically_healthy = (
        depression_level == "Normal" and 
        anxiety_level == "Normal" and 
        stress_level == "Normal" and
        burnout_level == "Risiko Rendah"
    )
    
    psychological_status = "SEHAT" if is_psychologically_healthy else "PERLU PERHATIAN"

    data = {
        'nama': mahasiswa_nama,
        'nim': mahasiswa_nim,
        'alamat': mahasiswa_alamat, 
        'tanggal_lahir': tanggal_lahir_formatted,
        'usia': usia,
        'tanggal_pemeriksaan': tanggal_pemeriksaan,
        'tanggal_surat': tanggal_surat,
        'tinggi_badan': float(data_kesehatan.tinggi_badan) if data_kesehatan and data_kesehatan.tinggi_badan else None,
        'berat_badan': float(data_kesehatan.berat_badan) if data_kesehatan and data_kesehatan.berat_badan else None,
        'tensi_sistolik': int(data_kesehatan.tensi_sistolik) if data_kesehatan and data_kesehatan.tensi_sistolik else None,
        'tensi_diastolik': int(data_kesehatan.tensi_diastolik) if data_kesehatan and data_kesehatan.tensi_diastolik else None,
        'tensi': data_kesehatan.tensi_lengkap if data_kesehatan else None,
        'depression_level': depression_level,
        'anxiety_level': anxiety_level,
        'stress_level': stress_level,
        'burnout_level': burnout_level,
        'physical_status': 'SEHAT',
        'psychological_status': psychological_status
    }

    return render_template('admin/pengajuan_surat/pengajuan_surat_print.html', data=data)