from app.config import BaseModel
from sqlalchemy.dialects.postgresql import JSON
import ulid
from sqlalchemy.orm import mapped_column, Mapped
import datetime
class QOLDetailTest(BaseModel):
    __tablename__ = "detail_qol_test"
    id: Mapped[int] = mapped_column("id",primary_key=True,autoincrement=True)
    id_test: Mapped[str] = mapped_column("id_test")
    no_qol_a: Mapped[str] = mapped_column("no_qol_a")
    no_qol_q: Mapped[str] = mapped_column("no_qol_q")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res