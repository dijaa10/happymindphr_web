from app.helpers.convert_to_slug import slugify
from sqlalchemy.orm import mapped_column, Mapped
from app.config import BaseModel
from app.config import session
import ulid
from sqlalchemy import event


class Artikel(BaseModel):
    __tablename__ = "artikel"

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", ulid.new())
        super().__init__(**kwargs)

    def generate_slug(self):
        if self.id:
            self.slug = slugify(self.judul)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    judul: Mapped[str] = mapped_column("judul")
    slug: Mapped[str] = mapped_column("slug")
    isi: Mapped[str] = mapped_column("isi")
    sumber: Mapped[str] = mapped_column("sumber")
    gambar: Mapped[str] = mapped_column("gambar")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res


# @event.listens_for(Artikel, 'before_insert')
# @event.listens_for(Artikel, 'before_update')
# def convert_to_slug(target, value, oldvalue):
#     if target.judul:
#         target.generate_slug()
