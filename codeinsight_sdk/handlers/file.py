from typing import List
from ..handler import Handler
from ..models import File

class FileHandler(Handler):
    def get(self, id: int) -> File:
        """
        Retrieves a file by its ID.
        """
        path = f"files/{id}"
        resp = self.client.request("GET", url_part=path)
        return File.from_dict(resp.json()["data"])
