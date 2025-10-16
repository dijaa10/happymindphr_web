from app.config import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
class QOLAnswer(BaseModel):
    __tablename__ = "qol_test_a"
    no: Mapped[int] = mapped_column("no", primary_key=True)
    skala: Mapped[str] = mapped_column("skala")
    nilai: Mapped[int] = mapped_column("nilai")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

