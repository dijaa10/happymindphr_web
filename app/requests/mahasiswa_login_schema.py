from pydantic import Field,EmailStr,BaseModel,field_validator
from app.models.Mahasiswa import Mahasiswa
from app.config import session

class MahasiswaLoginRequest(BaseModel):
    email: EmailStr
    password: str

    # @field_validator('email',mode='before')
    # @classmethod
    # def check_email_if_exist(cls, value):
    #     mahasiswa_data = session.query(Mahasiswa).filter_by(email=value).scalar()
    #     if (mahasiswa_data is 1):
    #         return value
    #     else:
    #          return value
            