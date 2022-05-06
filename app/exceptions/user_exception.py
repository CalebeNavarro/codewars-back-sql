class UserNotFound(Exception):
  def __init__(self):
    self.message = {"message": "User not found!"}
    self.status_code = 404
    super().__init__(self.message, self.status_code)


class FieldNotAllowed(Exception):
  def __init__(self, key):
    self.message = {"message": f"Field {key} not allowed"}
    self.status_code = 400
    super().__init__(self.message)


class IncorrectFieldType(Exception):
  def __init__(self, correct_type, incorrect_field, key):
    self.message = {
      "message": f"Incorrect type field",
      "example": f"The field name {key} was the type {type(incorrect_field)}, but the correct type is {correct_type}"
    }
    self.status_code = 400


class EmailAlreadyApproved(Exception):
  def __init__(self):
    self.message = {"message": "Email already approved"}
    self.status_code = 400


class InvalidEmail(Exception):
  def __init__(self):
    self.message = {"message": "Invalid email format"}
    self.status_code = 400
