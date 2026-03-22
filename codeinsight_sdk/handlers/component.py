from typing import List
from ..handler import Handler
from ..models import Component

class ComponentHandler(Handler):
    def all(self) -> List[Component]:
        """
        Retrieves all components.
        """
        path = "components"
        resp = self.client.request("GET", url_part=path)
        return [Component.from_dict(component) for component in resp.json()["data"]]

    def get(self, id: int) -> Component:
        """
        Retrieves a component by its ID.
        """
        path = f"components/{id}"
        resp = self.client.request("GET", url_part=path)
        return Component.from_dict(resp.json()["data"])
