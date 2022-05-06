from flask_restful import Resource
from flask import request, make_response, jsonify

from sqlalchemy.exc import IntegrityError, InvalidRequestError, DataError
from psycopg2 import errors
from app.exceptions import FieldNotAllowed, IncorrectFieldType, EnablerNotFound, UsernameNotFound, UserNotFound, InvalidEmail

from app.services import EnablerServices, UsersServices

from flask_jwt_extended import current_user, jwt_required


class Enabler(Resource):
  def get(self):
    all_enablers = EnablerServices.get_all_enablers()
    return make_response(jsonify(all_enablers), 200)

  def post(self):
    data = request.json
    try:
      UsersServices.validate_fields_post(data)
      EnablerServices.validate_fields_post(data)
      enabler_created = EnablerServices.create_enabler(data)
      return make_response(jsonify(enabler_created), 201)
    except IntegrityError as e:
      return make_response({"error": str(e).split("\n")[1]}, 409)
    except (InvalidRequestError, TypeError) as e:
      return make_response({'message': str(e)}, 400)
    except InvalidEmail as e:
      return e.message, e.status_code

  @jwt_required()
  def patch(self):
    data = request.json

    try:
      UsersServices.validate_fields(data)
      enabler_updated = EnablerServices.update_user_by_user_id(data, current_user.id)
      return make_response(enabler_updated, 200)
    except DataError as e:
      if type(e.orig) == errors.StringDataRightTruncation:
        return {"message": "Exceed characters"}, 400
    except FieldNotAllowed as e:
        return  e.message, e.status_code
    except IntegrityError as e:
      if type(e.orig) == errors.UniqueViolation:
        return {"message": "Email already exist!"}
    except IncorrectFieldType as e:
      return e.message, e.status_code
    return {"message": "Server Error. Please, report error to e-mail calebe.snavarro@gmail.com"}, 500

  @jwt_required()
  def delete(self):
    EnablerServices.delete_enabler(current_user.id)
    return '', 204


class EnablerRetrieve(Resource):
  def get(self, enabler_id):
    try:
      enabler = EnablerServices.get_enabler_by_enabler_id(enabler_id)
    except EnablerNotFound as e:
      return e.message, e.status_code

    return make_response(jsonify(enabler.serializer_students()), 200)


class EnablerHonorsRetrieve(Resource):
  def post(self, enabler_id: int):
    try:
      EnablerServices.update_honor_by_enabler_id(enabler_id)
    except (UsernameNotFound, EnablerNotFound, UserNotFound) as e:
      return e.message, e.status_code

    return '', 204
