# from dataclasses import dataclass
from sqlalchemy.orm import mapped_column, Mapped, deferred
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
import enum
from dotenv import dotenv_values


class Status(str,enum.Enum):
    aktif = 'aktif'
    nonaktif = 'nonaktif'


class PertanyaanCurhat(BaseModel):
    __tablename__ = "pertanyaan_curhat"

    id: Mapped[str] = mapped_column("id", primary_key=True)
    urutan: Mapped[int] = mapped_column("urutan")
    status = Column(Enum(Status))
    topik: Mapped[str] = mapped_column("topik")
    pertanyaan: Mapped[str] = mapped_column("pertanyaan")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
