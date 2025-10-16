from app.config import app
from app.controllers.admin.pengajuan_surat_controller import index,pengajuan_surat_json_data,pengajuan_surat_detail
from flask_login import login_required

@app.get('/admin/pengajuan_surat/')
@login_required
def pengajuan_surat_index():
    return index()

@app.get('/admin/pengajuan_surat/data')
@login_required
def pengajuan_surat_json():
    return pengajuan_surat_json_data()

@app.route('/admin/pengajuan_surat/data',methods=['GET'])
@app.route('/admin/pengajuan_surat/data/<id_mahasiswa>/<waktu_mulai>',methods=['GET'])
@login_required
def pengajuan_surat_edit(id_mahasiswa,waktu_mulai):
    return pengajuan_surat_detail(id_mahasiswa,waktu_mulai)
