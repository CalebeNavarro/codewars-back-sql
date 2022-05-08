from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required

from app.services import UsersServices, JwtService

from app.services.users_service import UsersServices


class UserView(Resource):
  def post(self):
    UsersServices.daily_update_honor()
    return "gi"


class UserRetrieveHonorsView(Resource):
  def get(self, user_id: int):
    user_honors = UsersServices.get_all_honors_by_user_id(user_id)
    return make_response(jsonify(user_honors), 200)
