from app.config import session
import os
import random
from app.form_validations.musik_validation import MusikValidation
import string
from flask import render_template,request,redirect, url_for
from app.models.Musik import Musik
from app.helpers.response_factory import response_with_data,response_data,response_message


def upload_file():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(10))
    file = request.files['mp3_file']
    filename = file.filename
    file_ext = os.path.splitext(filename)[1]
    filename = random_string.upper()+file_ext
    file.save(os.path.join("app/static/music",filename))
    return filename

def remove_file(filename):
    file_path = os.path.join("app/static/music/", filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return "",200
    return "",200
    # print(filename+"slkdas")
    # os.remove("app/storage/music/"+filename)

def musik_data():
    return render_template('admin/musik/index.html')

def musik_json_data():
    musik = session.query(Musik).all()
    data = list(map(lambda l: l.to_dict(), musik))
    session.close()
    return response_data(data)

def musik_insert():
    form = MusikValidation()
    return render_template("admin/musik/insert.html",form=form)

def musik_store():
    data = request.form
    session.add(
        Musik(
            genre=data['genre'],
            judul=data['judul'],
            penyanyi=data['penyanyi'],
            file=data['mp3_file'],
        )
    )
    session.commit()
    session.close()
    return redirect(url_for('musik_index'))

def musik_edit(musik_id):
    data = session.query(Musik).filter_by(id=musik_id).first()
    session.close()
    return render_template('admin/musik/edit.html',data=data)

def musik_update(musik_id):
    req_form = request.form
    print(req_form)
    music_data = session.query(Musik).filter_by(id=musik_id).first()
    if music_data:
        if req_form['mp3_file']:
            file_path = os.path.join("app/static/music/",  music_data.file)
            if os.path.exists(file_path):
                os.remove(file_path)
            music_data.file = req_form['mp3_file']
        music_data.genre = req_form['genre']
        music_data.judul = req_form['judul']
        music_data.penyanyi = req_form['penyanyi']
        session.commit()
        session.close()
    return redirect(url_for('musik_index'))

def musik_delete(musik_id):
    music_data = session.query(Musik).filter_by(id=musik_id).first()
    if music_data:
        file_path = os.path.join("app/static/music/",  music_data.file)
        if os.path.exists(file_path):
            os.remove(file_path)
        session.delete(music_data)
        session.commit()
        session.close()
    return redirect(url_for('musik_index'))
    