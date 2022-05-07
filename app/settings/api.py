from flask import Flask
from flask_restful import Api
from flask import Blueprint


def init_app(app: Flask) -> None:
  api_bp = Blueprint('api', __name__, url_prefix="/api/v1")
  api = Api(api_bp)


  from app.views.users_view import UserRetrieveHonorsView
  api.add_resource(UserRetrieveHonorsView, "/users/<int:user_id>/honors")

  from app.views.honors_view import HonorView, HonorRetrieveView
  api.add_resource(HonorView, "/honors")
  api.add_resource(HonorRetrieveView, "/honors/<int:honor_id>")

  from app.views.account_view import Account
  api.add_resource(Account, "/login")

  from app.views.student_view import Student, StudentRetrieve, StudentHonorsRetrieve, StudentRequiredLogin
  api.add_resource(Student, "/student")
  api.add_resource(StudentRetrieve, "/student/<int:student_id>")
  api.add_resource(StudentHonorsRetrieve, "/student/<int:student_id>/honors")
  api.add_resource(StudentRequiredLogin, "/student/who_i_am")

  from app.views.enabler_view import Enabler, EnablerRetrieve, EnablerHonorsRetrieve
  api.add_resource(Enabler, "/enabler")
  api.add_resource(EnablerRetrieve, "/enabler/<int:enabler_id>")
  api.add_resource(EnablerHonorsRetrieve, "/enabler/<int:enabler_id>/honors")

  from app.views.email_confirm import EmailConfirm
  api.add_resource(EmailConfirm, "/email_confirm/<string:email>")

  from app.views.google_view import GoogleView
  api.add_resource(GoogleView, "/google")

  app.register_blueprint(api_bp)
