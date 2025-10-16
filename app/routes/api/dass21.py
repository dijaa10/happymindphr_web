from app.config import app
from app.controllers.api.dass21_test_controller import get_q_data,get_a_data,send_question_data

@app.get("/api/mahasiswa/test/dass21/question/")
def data_pertanyaan():
    return get_q_data()

@app.get("/api/mahasiswa/test/dass21/answer/")
def data_jawaban():
    return get_a_data()

@app.post("/api/mahasiswa/test/dass21/kirim/")
def post_q_data():
    return send_question_data()
