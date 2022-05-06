from flask_jwt_extended import current_user
from app.exceptions.jwt_exception import UserNotOwner


class JwtService:
  @staticmethod
  def identity_if_user_is_the_owner(user_id: int) -> None:
    if not current_user.id == user_id:
      raise UserNotOwner()

