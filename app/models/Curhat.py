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



class Curhat(BaseModel):
    __tablename__ = "curhat"

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    id_mahasiswa: Mapped[str] = mapped_column("id_mahasiswa")

    waktu_mulai: Mapped[datetime.datetime] = mapped_column("waktu_mulai")
    waktu_selesai: Mapped[datetime.datetime] = mapped_column("waktu_selesai")