from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import os

load_dotenv()
Base = declarative_base()

if os.getenv("FLASK_ENV") == "development":
  engine = create_engine(os.getenv("DATABASE_URI_DEVELOPMENT"), echo=False, future=True)
else:
  engine = create_engine(os.getenv("DATABASE_URI"), echo=False, future=True)

engine.connect()

session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,
)

secondSession = Session(bind=engine)


def init_db():
  from app.models.users_model import User
  from app.models.honor_model import Honor
  from app.models.student_model import Student
  from app.models.enabler_model import Enabler
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
