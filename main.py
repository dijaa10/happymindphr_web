from app.config import app
from app.routes import urls 

if __name__ == '__main__':
    app.run(
        # uncomment below line and change the host to local ip
        # get local ip with ipconfig(windows) ifconfig(linux)
        host='192.168.1.3'
    )