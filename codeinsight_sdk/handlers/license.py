from typing import List
from ..handler import Handler
from ..models import License


class LicenseHandler(Handler):
    def all(self) -> List[License]:
        """
        Retrieves all licenses.
        """
        path = "licenses"
        resp = self.client.request("GET", url_part=path)
        return [License.from_dict(license) for license in resp.json()["data"]]

    def get(self, id: int) -> License:
        """
        Retrieves a license by its ID.
        """
        path = f"licenses/{id}"
        resp = self.client.request("GET", url_part=path)
        return License.from_dict(resp.json()["data"])
