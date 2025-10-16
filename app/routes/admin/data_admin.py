from app.controllers.admin.data_admin_controller import (
    data_admin_index_page,
    data_admin_json_data,
    data_admin_insert,
    data_admin_store,
    data_admin_edit,
    data_admin_delete,
)
from flask_login import login_required
from app.config import app
from app.helpers.decorators.role_decorator import must_super_admin

@app.get("/admin/data_admin/")
@login_required
def data_admin_index():
    return data_admin_index_page()


@app.get("/admin/data_admin/data")
@login_required
def data_admin_json():
    return data_admin_json_data()


@app.get("/admin/data_admin/insert")
@login_required
@must_super_admin
def insert_data_admin_page():
    return data_admin_insert()


@app.post("/admin/data_admin/store")
@login_required
def store_data_admin_data():
    return data_admin_store()


@app.route("/admin/data_admin/edit/", methods=["GET"])
@app.route("/admin/data_admin/edit/<admin_id>", methods=["GET"])
@login_required
def page_data_admin_edit(admin_id=None):
    return data_admin_edit(admin_id)


@app.route("/admin/data_admin/delete/", methods=["GET"])
@app.route("/admin/data_admin/delete/<admin_id>", methods=["GET"])
@login_required
def data_admin_delete_data(admin_id):
    return data_admin_delete(admin_id)
