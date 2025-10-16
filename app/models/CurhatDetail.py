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



class CurhatDetail(BaseModel):
    __tablename__ = "curhat_detail"

    id_curhat: Mapped[str] = mapped_column("id_curhat", primary_key=True)
    id_pertanyaan_curhat : Mapped[str] = mapped_column("id_pertanyaan_curhat")
    jawaban: Mapped[str] = mapped_column("jawaban")
