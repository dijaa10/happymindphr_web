from app.config import app
from app.routes.api import dass21
from app.controllers.api.musik_controller import data_musik
from app.controllers.api.mahasiswa_auth_controller import mahasiswa_register,mahasiswa_login,generate_otp,send_otp,reset_password,update_account,update_password
from app.controllers.api.mahasiswa_curhat_controller import mulai_curhat,kirim_awalan_curhat,batal_curhat,kirim_pesan_screening

# Route mahasiswa register
@app.post("/api/mahasiswa/register")
def register():
    return mahasiswa_register()

# Route mahasiswa OTP
@app.post("/api/mahasiswa/otp/generate")
def otp_generate():
    return generate_otp()

# Route mahasiswa send OTP
@app.post("/api/mahasiswa/otp/send")
def otp_send():
    return send_otp()

# Route mahasiswa password reset
@app.post("/api/mahasiswa/password/reset")
def password_reset():
    return reset_password()

# Route mahasiswa login
@app.post("/api/mahasiswa/login")
def login():
    return mahasiswa_login()

# Route mahasiswa ubah profil
@app.put("/api/mahasiswa/account/update/")
def update():
    return update_account()

# Route mahasiswa ubah password
@app.put("/api/mahasiswa/password/update/")
def pw_update():
    return update_password()

# Route awalan curhat
@app.get("/api/mahasiswa/curhat/mulai")
def curhat():
    return mulai_curhat()

# Route kirim awalan curhat
@app.post("/api/mahasiswa/curhat/mulai/kirim")
def curhat_kirim():
    return kirim_awalan_curhat()

# Route curhat cancel
@app.get('/api/mahasiswa/curhat/cancel')
def batal_curhat_api():
    return batal_curhat()

# Route data musik
@app.get('/api/musik')
def get_musik_data():
    return data_musik()

# Route kirim curhat
@app.post('/api/mahasiswa/curhat/kirim')
def post_pesan_screening():
    return kirim_pesan_screening()
