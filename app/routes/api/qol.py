from app.config import app
from app.controllers.api.qol_test_controller import *

@app.get("/api/mahasiswa/test/qol/answer/")
def qol_test():
    return get_a_data()

@app.get("/api/mahasiswa/test/qol/question/")
def qol_test_question():
    return get_q_data()

@app.post("/api/mahasiswa/test/qol/kirim/")
def qol_send_data():
    return send_question_data()