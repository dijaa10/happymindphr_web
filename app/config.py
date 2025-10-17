import os.path
from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv,dotenv_values
import locale

BaseModel = declarative_base()
load_dotenv() #load env

app = Flask(__name__)
app.debug = True
env_val = dotenv_values() #load env val

login_manager = LoginManager()
login_manager.init_app(app)

app.config['MYSQL_HOST'] = env_val['mysql_host']
app.config['MYSQL_USER'] = env_val['mysql_username']
app.config['MYSQL_PASSWORD'] = env_val['mysql_password']
app.config['MYSQL_DB'] = env_val['mysql_db']
mysql = MySQL(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{env_val['mysql_username']}:{env_val['mysql_password']}@localhost/{env_val['mysql_db']}"
app.config['SECRET_KEY'] = env_val['secret_key']
app.config['JWT_SECRET_KEY'] = env_val['secret_key']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

jwt = JWTManager(app)

db = SQLAlchemy(model_class=BaseModel)
db.init_app(app)
bcrypt = Bcrypt(app)

engine = create_engine(f"mysql://{env_val['mysql_username']}:{env_val['mysql_password']}@localhost/{env_val['mysql_db']}")
Session = sessionmaker(bind=engine)
# session = Session()
session = scoped_session(Session)
# session_factory = sessionmaker(bind=engine)
# session = scoped_session(session_factory)




