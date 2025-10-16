from app.config import app
from app.controllers.admin.musik_controller import *
from app.helpers.decorators.role_decorator import must_super_admin
from flask_login import login_required


@app.post("/admin/music/file/post")
@login_required
def upload_musik_file():
    return upload_file()

@app.route('/admin/music/file/delete/',methods=['GET'])
@app.route('/admin/music/file/delete/<string:filename>',methods=['GET'])
@login_required
def remove_musik_file(filename):
    return remove_file(filename)

@app.route("/admin/music/edit/",methods=['GET'])
@app.route("/admin/music/edit/<musik_id>",methods=['GET'])
@login_required
def musik_edit_page(musik_id):
    return musik_edit(musik_id)

@app.route("/admin/music/update/",methods=['POST'])
@app.route("/admin/music/update/<musik_id>",methods=['POST'])
@login_required
def musik_update_data(musik_id):
    return musik_update(musik_id)

@app.route("/admin/music/delete/",methods=['GET'])
@app.route("/admin/music/delete/<musik_id>",methods=['GET'])
@login_required
def musik_delete_data(musik_id):
    return musik_delete(musik_id)
    

@app.get("/admin/music/")
@login_required
def musik_index():
    return musik_data()


@app.get("/admin/music/data")
@login_required
def musik_json():
    return musik_json_data()


@app.get("/admin/music/insert")
@login_required
def insert_musik_page():
    return musik_insert()


@app.post("/admin/music/store")
@login_required
def store_musik_data():
    return musik_store()
