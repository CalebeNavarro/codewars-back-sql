from sqlalchemy import Column, Integer, String, update, delete, select, Boolean
from sqlalchemy.orm import relationship, joinedload

from werkzeug.security import generate_password_hash, check_password_hash

from app.settings.database import Base, session

from app.models.honor_model import Honor

from dataclasses import dataclass
from hmac import compare_digest


@dataclass
class User(Base):
  id: int
  name: str
  username: str
  current_honor: int
  email: str
  email_approved: bool

  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  name = Column(String(127), nullable=False)
  username = Column(String(127), nullable=False)
  current_honor = Column(Integer, default=0)
  super_user = Column(Boolean, default=False)

  password_check = Column(String(127), nullable=False)

  email = Column(String(127), nullable=False, unique=True)
  email_approved = Column(Boolean, default=False)


  honors = relationship("Honor")

  @property
  def password(self):
    raise AttributeError("password invalid")

  @password.setter
  def password(self, password):
    self.password_check = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_check, password)

  @staticmethod
  def delete_honors(user_id):
    with session() as s:
      stmt = delete(Honor).where(Honor.user_id == user_id)
      s.execute(stmt)
      s.commit()

  @staticmethod
  def get_honors(user_id: int) -> Honor:
    with session() as s:
      stmt = select(Honor).join(User.honors).where(User.id == user_id)
      result = s.execute(stmt).scalars().all()
      return result

  @staticmethod
  def serializer_query(query_result):
    keys = query_result.keys()
    value = query_result.one()
    return dict(zip(keys, value))

  @staticmethod
  def get_user_by_email(email: str) -> "User":
    with session() as s:
      stmt = select(User).where(User.email == email)
      user = s.execute(stmt).scalars().first()
    return user

  @staticmethod
  def get_all_users() -> list:
    with session() as s:
      query = s.execute(select(User))
      result = query.scalars().all()
    return result

  @staticmethod
  def get_user_by_user_id(user_id: int) -> "User":
    with session() as s:
      query = s.execute(select(User).where(User.id == user_id))
      result = query.scalars().first()
    return result

  @staticmethod
  def check_password(password, user):
      return compare_digest(password, user.password)

  def create_user(self):
    with session() as s:
      s.add(self)
      s.commit()

  @staticmethod
  def get_user_by_username(username: str) -> "User":
    with session() as s:
      stmt = select(User).where(User.username == username)
      result = s.execute(stmt).scalars().first()
    return result

  @classmethod
  def update_user(cls, data: dict, user_id: int) -> dict:
    with session() as s:
      stmt = update(User).where(User.id == user_id).values(**data).returning(User.name, User.username, User.current_honor)
      query_result = s.execute(stmt)
      s.commit()
    return cls.serializer_query(query_result)

  @staticmethod
  def delete_user(user_id: int) -> None:
    with session() as s:
      stmt = delete(User).where(User.id == user_id)
      s.execute(stmt)
      s.commit()

  @staticmethod
  def get_honor_by_user_id(user_id: int) -> list:
    with session() as s:
      stmt = select(Honor).join(User.honors).where(User.id == user_id)
      result = s.execute(stmt).scalars().all()
    return result

  @staticmethod
  def update_current_honor_by_user_id(user_id: int, honor: int):
    with session() as s:
      stmt = update(User).where(User.id == user_id).values({"current_honor": honor})
      s.execute(stmt)
      s.commit()

  @classmethod
  def update_user_by_email(cls, email: str):
    with session() as s:
      stmt = update(User).where(User.email == email).values(email_approved = True)
      s.execute(stmt)
      s.commit()

  def __repr__(self):
      return f'<User {self.name!r}>'
