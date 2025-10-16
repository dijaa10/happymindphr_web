from app.config import BaseModel
from sqlalchemy.dialects.postgresql import JSON
import ulid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
import datetime
class Dass21Test(BaseModel):
    __tablename__ = "dass_test"
    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    id_mahasiswa: Mapped[str] = mapped_column("id_mahasiswa",ForeignKey('mahasiswa.id'))
    total_nilai: Mapped[dict] = mapped_column(JSON)

    waktu_mulai: Mapped[datetime.datetime] = mapped_column("waktu_mulai")
    waktu_selesai: Mapped[datetime.datetime] = mapped_column("waktu_selesai")
    mahasiswa = relationship("Mahasiswa",back_populates='dass21_test')

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res