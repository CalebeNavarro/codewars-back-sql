class UsernameNotFound(Exception):
  def __init__(self, username: str):
    self.message = {"message": f"{username} not found in codewars api!"}
    self.status_code = 404
