from flask import jsonify, make_response
from flask_restful import Resource

from app.services import HonorsServices, UsersServices

class HonorView(Resource):
  def get(self):
    result = HonorsServices.get_honors()
    return make_response(jsonify(result), 200)


class HonorRetrieveView(Resource):
  def get(self, honor_id):
    result = HonorsServices.get_honor_by_id(honor_id)
    if not result:
      return {"message": "Honor not found!"}, 404
    return make_response(jsonify(result), 200)
