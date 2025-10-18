from sqlalchemy import Column, Integer, String, DECIMAL, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.config import BaseModel

class DataKesehatan(BaseModel):
    __tablename__ = 'data_kesehatan'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    mahasiswa_id = Column(String(26), ForeignKey('mahasiswa.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    tinggi_badan = Column(DECIMAL(5, 2), nullable=True)
    berat_badan = Column(DECIMAL(5, 2), nullable=True)
    tensi_sistolik = Column(Integer, nullable=True)
    tensi_diastolik = Column(Integer, nullable=True)
    tanggal = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    @property
    def tensi_lengkap(self):
        """Return format tensi lengkap: sistolik/diastolik"""
        if self.tensi_sistolik and self.tensi_diastolik:
            return f"{self.tensi_sistolik}/{self.tensi_diastolik}"
        return None
    
    def __repr__(self):
        return f'<DataKesehatan {self.id} - Mahasiswa {self.mahasiswa_id}>'