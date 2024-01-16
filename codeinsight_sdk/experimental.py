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
        # First we get the inventory summary for the project with vulnerability summary
        # Then we iterate over the inventory items and calling the inventory vulnerability endpoint for each item with a vulnerability
        inventory = self.client.projects.get_inventory_summary(
            project_id, vulnerabilitySummary=True
        )

        # Iterate over the inventory items, find which have vulnerabilities.
        item: ProjectInventoryItem
        vuln_items: list(ProjectInventoryItem) = []
        for item in inventory:
            if item.vulnerabilitySummary is None or len(item.vulnerabilitySummary) == 0:
                continue

            # If the item has a vulnerability, get the vulnerability details for this item and append it
            item_vul_summary = item.vulnerabilitySummary[0]
            k = ""
            if "CvssV2" in item_vul_summary.keys():
                k = "CvssV2"
            elif "CvssV3" in item_vul_summary.keys():
                k = "CvssV3"
            else:
                # If the item has no vulnerabilities, skip it
                continue

            if sum(item_vul_summary[k].values()) > 0:
                vul_detail = self.client.inventories.get_inventory_vulnerabilities(
                    item.id
                )
                item.vulnerabilities = vul_detail
                vuln_items.append(item)
            else:
                # If the item has no vulnerabilities, skip it
                continue

        return vuln_items
