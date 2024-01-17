from .handler import Handler
from .models import ProjectInventoryItem


class ExperimentalHandler(Handler):
    def __init__(self, client):
        super().__init__(client)

    def get(self):
        # Do nothing, there is no get for this handler
        pass

    def get_project_vulnerabilities(
        self, project_id: int
    ) -> list[ProjectInventoryItem]:
        """
        Get all vulnerabilities for a project.

        Args:
            project_id (int): The project id.

        Returns:
            dict: The vulnerabilities.
        """
        # First we get the inventory for the project
        # Then we iterate over the inventory items and calling the inventory vulnerability endpoint for each item with a vulnerability
        inventory = self.client.projects.get_inventory(
            project_id, skip_vulnerabilities=False, include_files=True
        )

        # Iterate over the inventory items, find which have vulnerabilities.
        item: ProjectInventoryItem
        vuln_items: list(ProjectInventoryItem) = []
        for item in inventory.inventoryItems:
            if item.vulnerabilities is None:
                continue
            # If the item no no vulnerabilities, ignore it
            if len(item.vulnerabilities) == 0:
                continue
            # TODO: Summarize the vulnerabilities?
            vuln_items.append(item)
        return vuln_items
