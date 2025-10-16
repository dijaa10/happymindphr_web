from flask import render_template,request,redirect,url_for,flash
from flask import session as flask_session
from app.config import session,bcrypt,login_manager
from flask_login import login_user,logout_user,current_user
from app.models.Admin import Admin
import base64



def show_login_page():
    redirect_url = request.args.get('redirect_url', '')
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
    # if redirect_url != '':
    #     redirect_url = base64.b64decode(redirect_url).decode('utf-8')
        # print(redirect_url.decode('utf-8'))
        return render_template('auth/login.html',redirect_url=redirect_url)


def login_function():
    data = request.form
    next_url = request.form.get("next")
    admin_data = session.query(Admin).filter_by(username=data['username']).first()
    check_password = bcrypt.check_password_hash(admin_data.password,data['password'])
    if admin_data and check_password:
        login_user(admin_data)
        try:
            if next_url:
                redirect_url = base64.b64decode(next_url).decode('utf-8')
                return redirect(redirect_url)
        except Exception as e:
            flash(f"{e}", category="error")
            return redirect(url_for('admin_login'))
        return redirect(url_for('dashboard'))
    flash(f"Mohon cek kembali username dan password anda", category="error")
    return redirect(url_for('admin_login'))


def show_dashboard():
    return render_template('admin/dashboard.html')

def logout_function():
    logout_user()
    # flask_session.clear()
    return redirect(url_for('admin_login'))