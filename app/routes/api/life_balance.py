from app.config import app
from app.controllers.api.life_balance_test_controller import *

@app.get("/api/mahasiswa/test/life_balance/question/")
def life_balance_q():
    return get_q_data()

@app.get("/api/mahasiswa/test/life_balance/answer/")
def life_balance_a():
    return get_a_data()

@app.post("/api/mahasiswa/test/life_balance/kirim/")
def life_balance_send():
    return send_question_data()