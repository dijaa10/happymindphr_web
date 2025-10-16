from flask import render_template, request, redirect, url_for,flash
from app.config import session
import sqlalchemy as db
from app.models.Admin import Admin
from app.helpers.response_factory import response_data

def data_admin_index_page():
    return render_template("admin/data_admin/index.html")

def data_admin_json_data():
    if request.is_json:
        admin = session.execute(db.select(
            Admin.id,
            Admin.nama,
            Admin.username,
            Admin.role,
        )).fetchall()
        data = list()
        for item in admin:
            data.append( {
                "id": item[0],
                "nama": item[1],
                "username": item[2],
                "role": item[3],
            })
        session.close()
        return response_data(data)

def data_admin_insert():
    return render_template("admin/data_admin/insert.html")

def data_admin_store():
    data = request.form
    search_if_exist = session.query(Admin).filter_by(nama=data['nama']).count() > 0
    if search_if_exist:
        flash(f"Data dengan username {data['username']} telah ada",category="error")
        return redirect(url_for('insert_data_admin_page'))
    session.add(
        Admin(
            nama=data['nama'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
        )
    )
    session.commit()
    session.close()
    return redirect(url_for('data_admin_index'))

def data_admin_edit(admin_id):
    data = session.query(Admin).filter_by(id=admin_id).first()
    session.close()
    # data = []
    return render_template('admin/data_admin/edit.html',data=data)

def data_admin_update(admin_id):
    data = request.form
    admin_data = session.query(Admin).filter_by(id=admin_id).first()
    if not admin_data:
        flash(f"Data tidak ditemukan",category="error")
        return redirect(url_for('page_data_admin_edit'))
    admin_data.nama = data['nama']
    admin_data.username = data['username']
    admin_data.password = data['password']
    admin_data.role = data['role']
    session.commit()
    session.close()
    return redirect(url_for('data_admin_index'))

def data_admin_delete(admin_id):
    admin_data = session.query(Admin).filter_by(id=admin_id).first()
    if not admin_data:
        flash(f"Data tidak ditemukan",category="error")
        return redirect(url_for('page_data_admin_edit'))
    session.delete(admin_data)
    session.commit()
    session.close()
    return redirect(url_for('data_admin_index'))
