from typing import List
from ..handler import Handler
from ..models import Folder


class FolderHandler(Handler):
    def get(self, id: int) -> Folder:
        """
        Retrieves a folder by its ID.
        """
        path = f"folders/{id}"
        resp = self.client.request("GET", url_part=path)
        return Folder.from_dict(resp.json()["data"])
