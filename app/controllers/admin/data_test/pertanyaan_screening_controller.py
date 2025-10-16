from flask import render_template, request, redirect, url_for
from app.models.PertanyaanCurhat import PertanyaanCurhat
from app.helpers.response_factory import response_data
from app.config import session

def pertanyaan_screening_index_page():
    return render_template("admin/data_test/pertanyaan_screening/index.html")

def screening_json_data():
    screening = session.query(PertanyaanCurhat).filter(PertanyaanCurhat.topik != "awalan").all()
    data = list(map(lambda l: l.to_dict(), screening))
    session.close()
    return response_data(data)
