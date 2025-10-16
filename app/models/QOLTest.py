from app.config import BaseModel
from sqlalchemy.dialects.postgresql import JSON
import ulid
from sqlalchemy.orm import mapped_column, Mapped
import datetime
class QOLTest(BaseModel):
    __tablename__ = "qol_test"
    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    id_mahasiswa: Mapped[str] = mapped_column("id_mahasiswa")
    total_nilai: Mapped[dict] = mapped_column(JSON)

    waktu_mulai: Mapped[datetime.datetime] = mapped_column("waktu_mulai")
    waktu_selesai: Mapped[datetime.datetime] = mapped_column("waktu_selesai")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
