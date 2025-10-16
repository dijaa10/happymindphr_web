from app.config import app
from app.controllers.admin.data_test.pertanyaan_screening_controller import *
@app.get("/admin/data-test/screening")
def pertanyaan_screening_index():
    return pertanyaan_screening_index_page()

@app.get('/admin/data-test/screening/data')
def pertanyaan_screening_json():
    return screening_json_data()