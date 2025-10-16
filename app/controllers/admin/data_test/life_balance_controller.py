from flask import render_template, request, redirect, url_for
from app.models.LifeBalanceQuestion import LifeBalanceQuestion
from app.helpers.response_factory import response_data
from app.config import session

def life_balance_index_page():
    return render_template("admin/data_test/life_balance/index.html")

def life_balance_json_data():
    life_balance = session.query(LifeBalanceQuestion).all()
    data = list(map(lambda l: l.to_dict(), life_balance))
    session.close()
    return response_data(data)