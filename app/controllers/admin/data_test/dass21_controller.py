from flask import render_template, request, redirect, url_for
from app.models.Dass21Question import Dass21Question
from app.helpers.response_factory import response_data
from app.config import session

def dass21_index_page():
    return render_template("admin/data_test/dass21/index.html")

def dass21_json_data():
    dass21 = session.query(Dass21Question).all()
    data = list(map(lambda l: l.to_dict(), dass21))
    session.close()
    return response_data(data)