class UserNotOwner(Exception):
  def __init__(self, *args: object) -> None:
    self.message = "Not allowed!"
    self.status_code = 403
    super().__init__(*args)
