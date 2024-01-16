from ..models import Report
from ..handler import Handler


class ReportHandler(Handler):
    """
    A class that handles operations related to reports.

    Args:
        client (Client): The client object used for making API requests.

    Attributes:
        cls (Report): The class representing a report.

    Methods:
        get(id): Retrieves a report by its ID.
        all(): Retrieves all reports.

    """

    def __init__(self, client):
        super().__init__(client)
        self.cls = Report

    def get(self, id: int):
        """
        Retrieves a report by its ID.

        Args:
            id (int): The ID of the report to retrieve.

        Returns:
            Report: The report object.

        """
        path = f"reports/{id}"
        resp = self.client.request("GET", url_part=path)
        report_data = resp.json()["data"]
        report = self.cls.from_dict(report_data)
        return report

    def all(self):
        """
        Retrieves all reports.

        Returns:
            list: A list of report objects.

        """
        path = "reports"
        resp = self.client.request("GET", url_part=path)
        reports = []
        for report_data in resp.json()["data"]:
            reports.append(self.cls.from_dict(report_data))
        return reports
