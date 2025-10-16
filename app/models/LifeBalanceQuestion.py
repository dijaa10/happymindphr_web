from app.config import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
class LifeBalanceQuestion(BaseModel):
    __tablename__ = "life_balance_q"
    no: Mapped[int] = mapped_column("no", primary_key=True)
    pertanyaan: Mapped[str] = mapped_column("pertanyaan")
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
