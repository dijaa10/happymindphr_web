from app.config import app
from app.controllers.admin.mahasiswa_controller import show_mahasiswa_data,mahasiswa_json_data,edit_mahasiswa,mahasiswa_curhat_result_data
from flask_login import login_required

@app.get('/admin/mahasiswa')
@login_required
def mahasiswa_index():
    return show_mahasiswa_data()


@app.get('/admin/mahasiswa/detail/')
@app.get('/admin/mahasiswa/detail/<string:mahasiswa_id>')
@login_required
def mahasiswa_edit(mahasiswa_id=None):
    return edit_mahasiswa(mahasiswa_id)

@app.get('/admin/mahasiswa/data')
@login_required
def mahasiswa_json():
    return mahasiswa_json_data()

@app.get('/admin/mahasiswa/curhat/data/')
@app.get('/admin/mahasiswa/curhat/data/<string:mahasiswa_id>')
@login_required
def curhat_mahasiswa_json(mahasiswa_id=None):
    return mahasiswa_curhat_result_data(mahasiswa_id)