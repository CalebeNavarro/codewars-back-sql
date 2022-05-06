class EnablerNotFound(Exception):
  def __init__(self):
    self.message = {"message": "Enabler Not Found!"}
    self.status_code = 404
