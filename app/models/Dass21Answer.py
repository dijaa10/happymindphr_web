from app.config import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
class Dass21Answer(BaseModel):
    __tablename__ = "dass_21_a"
    no: Mapped[int] = mapped_column("no", primary_key=True)
    skala: Mapped[str] = mapped_column("skala")
    nilai: Mapped[int] = mapped_column("nilai")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
