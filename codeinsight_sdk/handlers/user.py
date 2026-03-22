from typing import List
from ..handler import Handler
from ..models import User


class UserHandler(Handler):
    def all(self) -> List[User]:
        """
        Retrieves all users.
        """
        path = "users"
        resp = self.client.request("GET", url_part=path)
        return [User.from_dict(user) for user in resp.json()["data"]]

    def get(self, id: int) -> User:
        """
        Retrieves a user by its ID.
        """
        path = f"users/{id}"
        resp = self.client.request("GET", url_part=path)
        return User.from_dict(resp.json()["data"])
