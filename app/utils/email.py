import os
import smtplib
import pyotp
import re
from dotenv import load_dotenv

load_dotenv()


def send_email_from_smtp(email: str):
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login("calebe.snavarro@gmail.com", os.getenv("PASSWORD"))
  access_number = otp_generate('email').now()

  server.sendmail("calebe.snavarro@gmail.com", email, f"Uses this number to get access {access_number}")
  server.quit()

  return access_number


def otp_generate(email):
  totp = pyotp.TOTP('base32secret3232', interval=200)
  return totp


def isvalid(email):
  regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
  if re.fullmatch(regex, email):
      return True
  return False