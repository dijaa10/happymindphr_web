from app.config import BaseModel
from sqlalchemy.dialects.postgresql import JSON
import ulid
from sqlalchemy.orm import mapped_column, Mapped
import datetime
class Dass21DetailTest(BaseModel):
    __tablename__ = "detail_dass_test"
    id: Mapped[int] = mapped_column("id",primary_key=True,autoincrement=True)
    id_test: Mapped[str] = mapped_column("id_test")
    no_dass_21_q: Mapped[str] = mapped_column("no_dass_21_q")
    no_dass_21_a: Mapped[str] = mapped_column("no_dass_21_a")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res