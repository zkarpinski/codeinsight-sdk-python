from ..models import ProjectInventoryItem, Vulnerability
from ..handler import Handler

class InventoryHandler(Handler):
    """ Handles operations related to inventories."""

    def __init__(self, client):
        super().__init__(client)
        self.cls = ProjectInventoryItem
    
    def get(self, inventoryId: int) -> list[ProjectInventoryItem]:
        """
        Get an inventory item by id.

        Args:
            inventoryId (int): The inventory item id.

        Returns:
            ProjectInventoryItem: The inventory item.
        """
        path = f"inventories/{inventoryId}"
        resp = self.client.request("GET", url_part=path)
        inventory = []
        for inv_item in resp.json()['data']:
            inventory.append(ProjectInventoryItem.from_dict(inv_item))
        return inventory
    
    def get_inventory_vulnerabilities(self, inventoryId: int,
                                      limit: int = 25,
                                      offset: int = 1) -> list[Vulnerability]:
        """
        Get all vulnerabilities for an inventory item.

        Args:
            inventoryId (int): The inventory item id.

        Returns:
            dict: The vulnerabilities.
        """
        path = f"inventories/{inventoryId}/vulnerabilities"
        params = {"limit": limit, "offset": offset}
        resp = self.client.request("GET", url_part=path, params=params)

        # TODO - Iterate pages

        inventory_vuls: list(Vulnerability) = []
        for v in resp.json()['data']:
            inventory_vuls.append(Vulnerability.from_dict(v))

        return inventory_vuls