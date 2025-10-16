from app.config import app
from app.controllers.api.artikel_controller import artikel_index

@app.get("/api/artikel")
def data_artikel():
    return artikel_index()