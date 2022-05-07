import requests

import os
from dotenv import load_dotenv
load_dotenv()

class GoogleServices:
  @staticmethod
  def validate_human(token):
    secret = os.getenv("SECRET_CAPTCHA")
    response = requests.post(f"https://www.google.com/recaptcha/api/siteverify?secret={secret}&response={token}")
    data = response.json()
    return data
