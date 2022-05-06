from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.settings.database import Base
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Honor(Base):
    data: datetime
    honor: int

    __tablename__ = 'honor'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    honor = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    relationship("Users", back_populates="honors")
