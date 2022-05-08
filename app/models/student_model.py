import ipdb
from sqlalchemy import Column, Integer, ForeignKey, select, delete, update
from sqlalchemy.orm import relationship, joinedload

from app.settings.database import Base, session

from app.models.users_model import User

from dataclasses import dataclass


@dataclass
class Student(Base):
  id: int
  enabler_id: int
  user: User

  __tablename__ = 'student'

  id = Column(Integer, primary_key=True)

  user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
  user = relationship("User")

  enabler_id = Column(Integer, ForeignKey("enabler.id"))
  enabler = relationship("Enabler", back_populates="students")

  def get_user_by_student(self):
    with session() as s:
      stmt = select(User).join(Student.user).where(Student.id == self.id)
      user = s.execute(stmt).scalars().first()
    return user

  @staticmethod
  def get_student_by_user_id(user_id: int):
    with session() as s:
      stmt = select(Student).options(joinedload(Student.user)).join(User).where(User.id == user_id)
      result = s.execute(stmt).scalars().first()
    return result

  @staticmethod
  def create_student(user: User) -> "Student":
    with session() as s:
      student = Student(user=user)
      s.add(user)
      s.add(student)
      s.commit()
    return student

  @staticmethod
  def get_user_by_student_id(student_id: int) -> User:
    with session() as s:
      stmt = select(User).join(Student.user).where(Student.id == student_id)
      result = s.execute(stmt).scalars().first()
    return result

  @staticmethod
  def get_student_by_student_id(student_id: int) -> dict:
    with session() as s:
      stmt = select(Student)\
        .options(joinedload(Student.user))\
        .where(Student.id == student_id)
      user = s.execute(stmt).scalars().first()
    return user

  @staticmethod
  def get_all_students():
    with session() as s:
      stmt = select(Student).options(joinedload(Student.user))
      users = s.execute(stmt).scalars().all()
    return users

  @staticmethod
  def delete_student(user_id: int) -> None:
    with session() as s:
      stmt = delete(Student).where(User.id == user_id)
      s.execute(stmt)
      s.commit()

  def add_student_in_enabler(self, enabler_id: int) -> None:
    with session() as s:
      stmt = update(Student).where(Student.id == self.id).values(enabler_id = enabler_id)
      s.execute(stmt)
      s.commit()

  @staticmethod
  def update_enabler_in_student(student_id: int, enabler_id: int) -> None:
    with session() as s:
      stmt = update(Student).where(Student.id == student_id).values(enabler_id=enabler_id)
      s.execute(stmt)
      s.commit()
