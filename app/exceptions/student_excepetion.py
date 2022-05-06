class StudentNotFound(Exception):
  def __init__(self):
    self.message = {"message": "Student Not Found!"}
    self.status_code = 404
