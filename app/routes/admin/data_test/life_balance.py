from app.config import app
from app.controllers.admin.data_test.life_balance_controller import *

@app.get("/admin/data-test/life-balance")
def life_balance_index():
    return life_balance_index_page()

@app.get('/admin/data-test/life-balance/data')
def life_balance_json():
    return life_balance_json_data()