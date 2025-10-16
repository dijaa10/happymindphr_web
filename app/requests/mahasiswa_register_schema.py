from enum import Enum
from datetime import date,datetime
from pydantic import Field,EmailStr,BaseModel,field_validator
from app.enums.gender import Gender


class MahasiswaRegisterRequest(BaseModel):
    nama: str
    nik: str = Field(max_length=36)
    nim: str = Field(max_length=9)
    alamat: str
    tanggal_lahir: date
    password: str
    jenis_kelamin: Gender
    email: EmailStr
    no_hp: str

    @field_validator('tanggal_lahir', mode='before')
    @classmethod
    def parse_custom_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%d-%m-%Y').date()
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD or DD-MM-YYYY format")
        return value



