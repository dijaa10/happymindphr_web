from app.controllers.admin.artikel_controller import *
from app.config import app
from flask_login import login_required


@app.post("/admin/artikel/file/post")
@login_required
def upload_artikel_file():
    return upload_file()

@app.route('/admin/artikel/file/delete/',methods=['GET'])
@app.route('/admin/artikel/file/delete/<string:filename>',methods=['GET'])
# @optional.routes("/admin/music/file/delete/<string:filename>?/")
def remove_artikel_file(filename):
    return remove_file(filename)


@app.route("/admin/artikel/edit/",methods=['GET'])
@app.route("/admin/artikel/edit/<artikel_id>",methods=['GET'])
@login_required
def artikel_edit_page(artikel_id):
    return artikel_edit(artikel_id)

@app.route("/admin/artikel/update/",methods=['POST'])
@app.route("/admin/artikel/update/<artikel_id>",methods=['POST'])
@login_required
def artikel_update_data(artikel_id):
    return artikel_update(artikel_id)

@app.route("/admin/artikel/delete/",methods=['GET'])
@app.route("/admin/artikel/delete/<artikel_id>",methods=['GET'])
@login_required
def artikel_delete_data(artikel_id):
    return artikel_delete(artikel_id)

@app.get("/admin/artikel/")
@login_required
def artikel_index():
    return artikel_index_page()


@app.get("/admin/artikel/data")
def artikel_json():
    return artikel_json_data()

@app.get("/admin/artikel/insert")
@login_required
def artikel_insert_page():
    return artikel_insert()

@app.post("/admin/artikel/store")
@login_required
def artikel_store_data():
    return artikel_store()

@app.post("/admin/artikel/scraping")
@login_required
def artikel_store_scraping():
    return artikel_scraping()
