from flask import render_template, request, redirect, url_for, flash
from app.config import session,db
import string
import os
import random
import app.helpers.parser.halodoc as halodoc
import app.helpers.parser.detikhealth as detikhealth
import app.helpers.parser.alodokter as alodokter
from app.models.Artikel import Artikel
from app.helpers.compress_image import convert_to_webp
from app.helpers.response_factory import response_data


def upload_file():
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(15))
    file = request.files["image_file"]
    filename = random_string.upper() + ".webp"
    converted_image = convert_to_webp(file, filename)
    # filename = file.filename
    # file_ext = os.path.splitext(filename)[1]
    # file.save(os.path.join("app/static/music",filename))
    return filename


def remove_file(filename):
    file_path = os.path.join("app/static/images/artikel/", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return "", 200
    return "", 200
    # print(filename+"slkdas")
    # os.remove("app/storage/music/"+filename)


def artikel_index_page():
    return render_template("admin/artikel/index.html")


def artikel_insert():
    return render_template("admin/artikel/insert.html")


def artikel_json_data():
    artikel = db.session.query(Artikel).all()
    data = list(map(lambda l: l.to_dict(), artikel))
    db.session.close()
    return response_data(data)


def artikel_store():
    data = request.form
    new_article = Artikel(
        judul=data["judul"],
        isi=data["isi_artikel"],
        sumber=data["sumber"],
        gambar=data["image_file"],
    )
    new_article.generate_slug()
    session.add(new_article)
    session.commit()
    session.close()
    return redirect(url_for("artikel_index"))


def artikel_edit(artikel_id):
    data = session.query(Artikel).filter_by(id=artikel_id).first()
    session.close()
    return render_template("admin/artikel/edit.html", data=data)


def artikel_update(artikel_id):
    req_form = request.form
    artikel_data = session.query(Artikel).filter_by(id=artikel_id).first()
    if artikel_data:
        if req_form["image_file"]:
            file_path = os.path.join("app/static/images/artikel/", artikel_data.file)
            if os.path.exists(file_path):
                os.remove(file_path)
            artikel_data.file = req_form["image_file"]
        artikel_data.judul = req_form["judul"]
        artikel_data.sumber = req_form["sumber"]
        artikel_data.isi = req_form["isi_artikel"]
        artikel_data.generate_slug()
        session.commit()
    return redirect(url_for("artikel_index"))


def artikel_delete(artikel_id):
    artikel_data = session.query(Artikel).filter_by(id=artikel_id).first()
    if artikel_data:
        file_path = os.path.join("app/static/images/artikel/", artikel_data.gambar)
        if os.path.exists(file_path):
            os.remove(file_path)
        session.delete(artikel_data)
        session.commit()
        session.close()
    return redirect(url_for("artikel_index"))


def artikel_scraping():
    rule = [
        "halodoc.com",
        "health.detik.com",
        "alodokter.com",
    ]  # define the only website can be scraped
    data = request.form
    if not any(word in data["url"] for word in rule):
        flash(f"Url tidak didukung", category="error")
        return redirect(url_for("artikel_insert_page"))
    match (data["url"]):
        case val if rule[0] in val:
            process = halodoc.parse(data["url"])
            flash(f"Data berhasil di scraping", category="success")
            return redirect(url_for("artikel_insert_page"))
        case val if rule[1] in val:
            process = detikhealth.parse(data["url"])
            flash(f"Data berhasil di scraping", category="success")
            return redirect(url_for("artikel_insert_page"))
        case val if rule[2] in val:
            process = alodokter.parse(data["url"])
            # if process is not True:
            #     flash(e, category="error")
            #     return redirect(url_for("artikel_insert_page"))
            flash(f"Data berhasil di scraping", category="success")
            return redirect(url_for("artikel_insert_page"))
