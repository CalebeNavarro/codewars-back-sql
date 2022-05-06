import ipdb
from sqlalchemy import Column, Integer, ForeignKey, select, delete
from sqlalchemy.orm import relationship, backref, joinedload
from app.settings.database import Base, session

from dataclasses import dataclass

from app.models.users_model import User
from app.models.student_model import Student


@dataclass()
class Enabler(Base):
  id: int
  user: object

  __tablename__ = "enabler"

  id = Column(Integer, primary_key=True)

  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
  user = relationship("User")

  students = relationship("Student", back_populates="enabler")

  @staticmethod
  def create_enabler(data: dict) -> "Enabler":
    with session() as s:
      user = User(**data)
      student = Enabler(user=user)
      s.add(user)
      s.add(student)
      s.commit()
    return student

  @staticmethod
  def get_all_enablers() -> list:
    with session() as s:
      stmt = select(Enabler)\
        .options(joinedload(Enabler.user))\
        .join(Enabler.user)
      result = s.execute(stmt).scalars().all()
    return result

  @staticmethod
  def get_enabler_by_enabler_id(enabler_id: int) -> "Enabler":
    with session() as s:
      stmt = select(Enabler)\
        .options(joinedload(Enabler.students).joinedload(Student.user))\
        .options(joinedload(Enabler.user))\
        .where(Enabler.id == enabler_id)
      enabler = s.execute(stmt).scalars().first()
    return enabler

  @staticmethod
  def get_user_by_enabler_id(enabler_id: int) -> User:
    with session() as s:
      stmt = select(User).join(Enabler.user).where(Enabler.id == enabler_id)
      user = s.execute(stmt).scalars().first()
    return user

  def serializer_students(self):
    return {
      "id": self.id,
      "user": self.user,
      "students": self.students
    }
