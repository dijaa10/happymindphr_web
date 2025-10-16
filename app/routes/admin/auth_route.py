from app.controllers.admin.auth_controller import *
from app.config import app
from flask_login import login_required,logout_user
from app.models.Admin import Admin


@app.get("/", endpoint="admin_login")
def login():
    return show_login_page()


@app.post("/admin/login_process")
def admin_login_process():
    return login_function()


@app.get("/admin/dashboard")
@login_required
def dashboard():
    return show_dashboard()

@app.route("/logout")
@login_required
def logout():
    return logout_function()
