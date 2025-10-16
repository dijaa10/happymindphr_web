from flask import render_template, request, redirect, url_for
from app.config import db,session
from app.helpers.response_factory import response_data
from app.models.Artikel import Artikel

def artikel_index():
    artikel = db.session.query(Artikel).all()
    data = list(map(lambda l: l.to_dict(), artikel))
    session.close()
    return response_data(data)