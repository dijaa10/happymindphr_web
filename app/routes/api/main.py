from app.config import app
from app.routes.api import mahasiswa
from . import qol
from . import artikel
from . import life_balance
from app.helpers import response_factory

@app.route("/api/login")
def list_all():
    return response_factory.response_message("Login Page")
