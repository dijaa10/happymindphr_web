# from dataclasses import dataclass
from sqlalchemy.orm import mapped_column, Mapped
from app.config import BaseModel
import ulid
import datetime


class OTPCode(BaseModel):
    __tablename__ = "otp_code"

    id: Mapped[int] = mapped_column("id", primary_key=True,autoincrement=True)
    mahasiswa_id: Mapped[str] = mapped_column("mahasiswa_id")
    code: Mapped[str] = mapped_column("code")
    issued_time: Mapped[datetime.datetime] = mapped_column("issued_time")
    expired_time: Mapped[datetime.datetime] = mapped_column("expired_time")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res