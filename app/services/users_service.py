from app.settings.database import session
from sqlalchemy import select, update

from app.models.users_model import User
from app.models.honor_model import Honor

from app.utils.codewars_api import CodewarsUtil

from .honors_service import HonorsServices

from app.exceptions import UserNotFound, UsernameNotFound, FieldNotAllowed, IncorrectFieldType, EmailAlreadyApproved, InvalidEmail

from datetime import datetime
from app.utils.email import isvalid

# Todo: research if it better to handle the error before it happens, or after.


class UsersServices:
  fields_allowed_update = ["name", "username", "email"]
  type_fields = {"name": str, "username": str, "email": str}

  @staticmethod
  def validate_fields_post(data: dict):
    email = data.get("email", None)
    if not isvalid(email):
      raise InvalidEmail()

  @classmethod
  def validate_fields(cls, data: dict):
    for key in data:
      if key not in cls.fields_allowed_update:
        raise FieldNotAllowed(key)
      if cls.type_fields[key] != type(data[key]):
        raise IncorrectFieldType(cls.type_fields[key], data[key], key)

  @staticmethod
  def get_all_honors_by_user_id(user_id: int) -> list[Honor]:
    user_honors = User.get_honors(user_id)
    print(user_honors)
    return user_honors

  @classmethod
  def create_honor_in_user(cls, user_id: int) -> None:
    user = User.get_user_by_user_id(user_id)

    if not user:
      raise UserNotFound()

    user_api = CodewarsUtil(user.username)
    user_api.response_by_username()
    honor = user_api.response.get("honor", None)

    if not honor:
      raise UsernameNotFound(user.username)

    honors = User.get_honor_by_user_id(user_id)
    has_updated = cls.check_honor_already_updated_today(honors)

    if has_updated and honor == user.current_honor:
      return

    data_user = {"honor": honor, "user_id": user_id}
    HonorsServices.create_honor_by_user_id(data_user)
    User.update_user({"current_honor": user_api.response["honor"]}, user_id)

  @staticmethod
  def check_honor_already_updated_today(honors: list):
    today = datetime.now().day
    for honor in honors:
      if today == honor.data.day:
        return True
    return False

  @staticmethod
  def get_user_by_username(username: str) -> User:
    return User.get_user_by_username(username)

  @staticmethod
  def get_user_by_email(email: str) -> User:
    user = User.get_user_by_email(email)
    if not user:
      raise UserNotFound()
    return user

  @staticmethod
  def update_user_by_email(email: str):
    User.update_user_by_email(email)

  @staticmethod
  def get_student_or_enabler_by_user_id(user_id: int):
    user = User.get_user_by_user_id(user_id)
    pass

  @classmethod
  def daily_update_honor(cls):
    users_list = User.get_all_users()
    for user in users_list:
      cls.create_honor_in_all_user(user.id)

  @classmethod
  def create_honor_in_all_user(cls, user_id: int) -> None:
    user = User.get_user_by_user_id(user_id)

    if not user:
      return

    user_api = CodewarsUtil(user.username)
    user_api.response_by_username()
    honor = user_api.response.get("honor", None)

    if not honor:
      return

    honors = User.get_honor_by_user_id(user_id)
    has_updated = cls.check_honor_already_updated_today(honors)

    if has_updated and honor == user.current_honor:
      return

    data_user = {"honor": honor, "user_id": user_id}
    HonorsServices.create_honor_by_user_id(data_user)
    User.update_user({"current_honor": user_api.response["honor"]}, user_id)
