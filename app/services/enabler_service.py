from app.models.users_model import User
from app.models.enabler_model import Enabler

from app.services import UsersServices

from app.exceptions import EnablerNotFound, InvalidEmail

from app.exceptions import UserNotFound


class EnablerServices:
  @staticmethod
  def validate_fields_post(data: dict):
    email = data.get("email", None)
    if email[-14:] != "@kenzie.com.br":
      raise InvalidEmail()

  @staticmethod
  def create_enabler(data: dict) -> Enabler:
    enabler = Enabler.create_enabler(data)
    return enabler

  @staticmethod
  def get_all_enablers() -> list:
    return Enabler.get_all_enablers()

  @staticmethod
  def update_user_by_user_id(data: dict, user_id: int) -> dict:
    # Todo: Colocar na usersServices e também realizar uma lógica para evitar students alterar enabler.
    return User.update_user(data, user_id)

  @staticmethod
  def delete_enabler(enabler_id: int) -> None:
    User.delete_user(enabler_id)

  @staticmethod
  def get_enabler_by_enabler_id(enabler_id: int) -> User:
    enabler = Enabler.get_enabler_by_enabler_id(enabler_id)
    if not enabler:
      raise EnablerNotFound
    return enabler

  @staticmethod
  def update_honor_by_enabler_id(enabler_id: int):
    user = Enabler.get_user_by_enabler_id(enabler_id)
    if not user:
      raise UserNotFound()
    UsersServices.create_honor_in_user(user.id)

  @staticmethod
  def get_user_by_email(email: str) -> User:
    return User.get_user_by_email(email)

