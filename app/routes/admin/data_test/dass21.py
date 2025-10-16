from app.config import app
from app.controllers.admin.data_test.dass21_controller import *

@app.get("/admin/data-test/dass21")
def dass21_index():
    return dass21_index_page()

@app.get('/admin/data-test/dass21/data')
def dass21_json():
    return dass21_json_data()