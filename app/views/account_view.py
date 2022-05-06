from flask_restful import Resource
from flask import request, jsonify

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from app.services import UsersServices

from app.models.student_model import Student

from app.exceptions import UserNotFound

class Account(Resource):
  def post(self):
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
      return {"message": "missing fields"}
    if type(password) != str:
      return {"message": "Wrong type password"}

    try:
      user = UsersServices.get_user_by_email(email)
    except UserNotFound as e:
      return e.message, e.status_code
    if not user.verify_password(password):
      return {"message": "Wrong   password"}, 400

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

  @jwt_required()
  def get(self):

    return jsonify(
      user_id=current_user.id,
      current_honor=current_user.current_honor,
      username=current_user.username,
      name=current_user.name,
      email=current_user.email,
    )
