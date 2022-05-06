import requests


class CodewarsUtil:
  base_uri = "https://www.codewars.com/api/v1/users"

  def __init__(self, username: str) -> None:
    self.username = username
    self.response = {}

  def response_by_username(self):
    self.response = requests.get(f'{self.base_uri}/{self.username}').json()
