from app.settings.database import session
from sqlalchemy import select, update
from app.models.honor_model import Honor
from datetime import datetime
from app.utils.codewars_api import CodewarsUtil


class HonorsServices:

  @staticmethod
  def get_honors():
    with session() as s:
      stmt = select(Honor)
      result = s.execute(stmt).scalars().all()
    return result

  @staticmethod
  def get_honor_by_id(honor_id: int):
    with session() as s:
      stmt = select(Honor).where(Honor.id == honor_id)
      result = s.execute(stmt).scalars().first()
    return result

  @staticmethod
  def create_honor_by_user_id(data_user: dict) -> None:
    with session() as s:
      u = Honor(data=datetime.now(), **data_user)
      s.add(u)
      s.commit()

  @staticmethod
  def update_honor_by_user_id(user_id, data) -> None:
    with session() as s:
      stmt = update(Honor).where(Honor.id == user_id).values(**data).\
        execution_options(synchronize_session="fetch")
      s.execute(stmt)
      s.commit()
