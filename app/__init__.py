from flask import Flask
from app.settings.api import init_app
from app.settings.database import init_db
from app.settings.jwt import init_jwt
from flask_cors import CORS


def create_app():
  app = Flask(__name__)
  CORS(app, origins=["https://codewars-kenzie-sql.vercel.app", "http://localhost:3000"])
  app.config["JSON_SORT_KEYS"] = False

  init_jwt(app)

  # init_db()
  init_app(app)

  return app
