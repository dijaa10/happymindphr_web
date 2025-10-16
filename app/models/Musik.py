# from dataclasses import dataclass
from sqlalchemy.orm import mapped_column, Mapped
from app.config import BaseModel
import ulid


class Musik(BaseModel):
    __tablename__ = "musik"

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    judul: Mapped[str] = mapped_column("judul")
    genre: Mapped[str] = mapped_column("genre")
    penyanyi: Mapped[str] = mapped_column("penyanyi")
    file: Mapped[str] = mapped_column("file")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
