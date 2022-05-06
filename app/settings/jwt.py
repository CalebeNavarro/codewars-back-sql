import os
import datetime
from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager

from app.models.users_model import User

load_dotenv()


def init_jwt(app: Flask) -> None:
  app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
  app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=3)
  jwt = JWTManager(app)

  @jwt.user_identity_loader
  def user_identity_lookup(user):
    return user.id

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.get_user_by_user_id(identity)
