from app.models.users_model import User
from app.models.student_model import Student

from app.exceptions import StudentNotFound

from app.services import UsersServices

from app.models.honor_model import Honor


class StudentServices:
  @staticmethod
  def create_student(data: dict) -> Student:
    user = User(**data)
    student_created = Student.create_student(user)
    return student_created

  @staticmethod
  def get_student_by_user_id(user_id: int):
    student = Student.get_student_by_user_id(user_id)
    return student

  @staticmethod
  def get_all_students() -> list:
    return Student.get_all_students()

  @staticmethod
  def update_user_by_user_id(data: dict, user_id: int) -> dict:
    return User.update_user(data, user_id)

  @staticmethod
  def delete_student(user_id: int) -> None:
    User.delete_honors(user_id)
    User.delete_user(user_id)

  @staticmethod
  def update_enabler_in_student(user_id: int, enabler_id: int) -> None:
    student = Student.get_student_by_user_id(user_id)
    print(student.id, enabler_id)
    Student.update_enabler_in_student(student.id, enabler_id)

  @staticmethod
  def get_student_by_student_id(student_id: int) -> dict:
    student = Student.get_student_by_student_id(student_id)
    if not student:
      raise StudentNotFound
    return student

  @staticmethod
  def update_honor_by_student_id(student_id: int):
    user = Student.get_user_by_student_id(student_id)
    if not user:
      raise StudentNotFound
    UsersServices.create_honor_in_user(user.id)
