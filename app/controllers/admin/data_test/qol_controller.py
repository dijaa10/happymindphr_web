from flask import render_template, request, redirect, url_for
from app.models.QOLQuestion import QOLQuestion
from app.helpers.response_factory import response_data
from app.config import session

def qol_index_page():
    return render_template("admin/data_test/qol/index.html")

def qol_json_data():
    qol = session.query(QOLQuestion).all()
    data = list(map(lambda l: l.to_dict(), qol))
    session.close()
    return response_data(data)