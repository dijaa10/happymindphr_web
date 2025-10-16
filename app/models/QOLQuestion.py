from app.config import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
class QOLQuestion(BaseModel):
    __tablename__ = "qol_test_q"
    no: Mapped[int] = mapped_column("no", primary_key=True)
    pertanyaan: Mapped[str] = mapped_column("pertanyaan")
    domain: Mapped[str] = mapped_column("domain")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
