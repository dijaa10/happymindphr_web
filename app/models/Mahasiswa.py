from sqlalchemy.orm import mapped_column, Mapped, deferred, relationship
from app.config import BaseModel
from sqlalchemy.sql import func
from app.enums.gender import Gender
from sqlalchemy import Column, Enum, TIMESTAMP, Date, String
from app.config import bcrypt,session
from sqlalchemy import event
from werkzeug.security import generate_password_hash
import ulid
from flask_jwt_extended import create_access_token
import datetime
import jwt
from dotenv import dotenv_values


class Mahasiswa(BaseModel):
    __tablename__ = "mahasiswa"

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    nama: Mapped[str] = mapped_column("nama")
    nik: Mapped[str] = mapped_column("nik")
    nim: Mapped[str] = mapped_column("nim")
    avatar: Mapped[str] = mapped_column("avatar")
    tanggal_lahir = Column(Date)
    no_hp : Mapped[str] = mapped_column("no_hp")
    # password: Mapped[str] = mapped_column(String)
    password = deferred(mapped_column(String))
    alamat: Mapped[str] = mapped_column("alamat")
    jenis_kelamin = Column(Enum(Gender))
    email: Mapped[str] = mapped_column("email")
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.current_timestamp())
    dass21_test = relationship("Dass21Test",back_populates="mahasiswa")

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return create_access_token(user_id)
            # return jwt.encode(
            #     payload,
            #     app.config.get('SECRET_KEY'),
            #     algorithm='HS256'
            # )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            env_val = dotenv_values() #load env val
            payload = jwt.decode(
                auth_token, env_val['secret_key'], algorithms="HS256"
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return 1
        except jwt.InvalidTokenError:
            return 2

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    def mahasiswa_header_check(request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        resp = Mahasiswa.decode_auth_token(auth_token)
        if not isinstance(resp, int):
            user = session.query(Mahasiswa).filter_by(id=resp).first()
            data = {
                'user_id': Mahasiswa.id,
                'email': Mahasiswa.email,
            }
            return True
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return False

# Mahasiswa.__mapper__.add_property('password', deferred(Mahasiswa.__table__.c.password))
@event.listens_for(Mahasiswa.password, "set", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value)
    return value
