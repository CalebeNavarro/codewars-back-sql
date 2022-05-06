from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from app.services import UsersServices, JwtService

from app.exceptions import UserNotFound, UsernameNotFound, UserNotOwner


class UserRetrieveHonorsView(Resource):
  def get(self, user_id: int):
    user_honors = UsersServices.get_all_honors_by_user_id(user_id)
    return make_response(jsonify(user_honors), 200)
