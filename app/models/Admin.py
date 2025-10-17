from app.helpers.convert_to_slug import slugify
from sqlalchemy.orm import mapped_column, Mapped
from app.config import BaseModel
from flask_login import UserMixin
from app.config import session,bcrypt
import ulid
from sqlalchemy import event

class Admin(UserMixin, BaseModel):
    __tablename__ = "admin"

    def __init__(self, **kwargs):
        kwargs["id"] = kwargs.get("id", str(ulid.new()))
        super().__init__(**kwargs)

    id: Mapped[str] = mapped_column("id", primary_key=True)
    nama: Mapped[str] = mapped_column("nama")
    username: Mapped[str] = mapped_column("username")
    password: Mapped[str] = mapped_column("password")
    role: Mapped[str] = mapped_column("role")

    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
        
    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

# Admin.__mapper__.add_property('password', deferred(Admin.__table__.c.password))
@event.listens_for(Admin.password, "set", retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return bcrypt.generate_password_hash(value)
    return value