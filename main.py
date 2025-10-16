from app.config import app
from app.routes import urls 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)