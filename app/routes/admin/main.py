from app.models.Admin import Admin
from flask import render_template,request
import base64
from app.config import login_manager,session,db
from . import auth_route
from . import mahasiswa
from . import musik
from . import artikel
from . import data_admin
from . import pengajuan_surat
from .data_test import pertanyaan_screening,dass21,qol,life_balance
from app.config import app

@login_manager.user_loader
def load_user_from_request(id):
    # Implement logic to load user from request headers, tokens, etc.
    # Example: user_id = request.headers.get('X-User-ID')
    # return User.query.get(int(user_id))
    data = db.session.query(Admin).filter_by(id=id).first()
    # session.close()
    return data

@login_manager.unauthorized_handler
def unauthorized_handler():
    redirect_url = base64.b64encode(request.path.encode("utf-8"))
    return render_template('admin/error/403.html',redirect_url=redirect_url.decode('utf-8'))

@app.errorhandler(404)
def not_found(e):
    return render_template('admin/error/404.html')