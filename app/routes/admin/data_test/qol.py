from app.config import app
from app.controllers.admin.data_test.qol_controller import *

@app.get("/admin/data-test/qol")
def qol_index():
    return qol_index_page()

@app.get('/admin/data-test/qol/data')
def qol_json():
    return qol_json_data()