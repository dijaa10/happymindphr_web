from enum import Enum
from datetime import date,datetime
from pydantic import Field,EmailStr,BaseModel,field_validator
from app.enums.gender import Gender
from typing import Optional

class MahasiswaUpdateRequest(BaseModel):
    nama: str
    nim: str = Field(max_length=9)
    jenis_kelamin: Gender
    email: EmailStr
    
    # --- PERBAIKAN DITAMBAHKAN DI SINI ---
    # Baris ini memberitahu Pydantic untuk menerima field 'avatar'.
    # 'Optional[str] = None' berarti field ini tidak wajib ada (opsional).
    avatar: Optional[str] = None

