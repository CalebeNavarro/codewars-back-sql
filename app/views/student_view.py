from flask_restful import Resource
from flask import request, make_response, jsonify

from sqlalchemy.exc import InvalidRequestError, DataError, IntegrityError
from app.exceptions import UserNotFound, UsernameNotFound, InvalidEmail
from psycopg2 import errors

from app.services import StudentServices, UsersServices, GoogleServices

from app.exceptions import FieldNotAllowed, StudentNotFound

from flask_jwt_extended import current_user, jwt_required

class Student(Resource):

  def get(self):
    all_students = StudentServices.get_all_students()
    return make_response(jsonify(all_students), 200)

  def post(self):
    data = request.json
    if request.json.get("email_approved", None):
      return {"message": "email_approved is not allowed by user"}, 400

    data_response = GoogleServices.validate_human(data["token"])
    if not data_response["success"]:
      return {"message": "Invalid captcha"}

    del data["token"]
    try:
      UsersServices.validate_fields_post(data)
      student_created = StudentServices.create_student(data)
      return make_response(jsonify(student_created), 201)
    except IntegrityError as e:
      return make_response({"message": "Email already exists!"}, 409)
    except (InvalidRequestError, TypeError) as e:
      return make_response({'message': str(e)}, 400)
    except InvalidEmail as e:
      return e.message, e.status_code

  @jwt_required()
  def patch(self):
    data = request.json
    if request.json.get("email_approved", None):
      return {"message": "email_approved is not allowed by user"}, 400

    try:
      UsersServices.validate_fields(data)
      student_updated = StudentServices.update_user_by_user_id(data, current_user.id)
      return make_response(student_updated, 200)
    except DataError as e:
      if type(e.orig) == errors.StringDataRightTruncation:
        return {"message": "Exceed characters"}, 400
    except FieldNotAllowed as e:
        return  e.message, e.status_code
    return {"message": "Server Error. Please, report error to e-mail calebe.snavarro@gmail.com"}, 500


  @jwt_required()
  def delete(self):
    StudentServices.delete_student(current_user.id)
    return '', 204

  @jwt_required()
  def put(self):
    enabler_id = request.json.get("enabler_id")
    if request.json.get("email_approved", None):
      return {"message": "email_approved is not allowed by user"}, 400

    try:
      StudentServices.update_enabler_in_student(current_user.id, enabler_id)
      return make_response(jsonify({"message": "successful"}), 200)
    except IntegrityError as e:
      if type(e.orig) == errors.ForeignKeyViolation:
        return {"message": "Invalid Enabler id"}, 400
    return {"message": "Server Error!"}

class StudentRequiredLogin(Resource):
  @jwt_required()
  def get(self):
    student = StudentServices.get_student_by_user_id(current_user.id)
    return make_response(jsonify(student), 200)


class StudentRetrieve(Resource):
  def get(self, student_id):
    try:
      student = StudentServices.get_student_by_student_id(student_id)
    except StudentNotFound as e:
      return e.message, e.status_code
    return make_response(jsonify(student), 200)


class StudentHonorsRetrieve(Resource):
  def patch(self, student_id: int):
    try:
      StudentServices.update_honor_by_student_id(student_id)
    except (UsernameNotFound, StudentNotFound, UserNotFound) as e:
      return e.message, e.status_code

    return '', 204
