from typing import List
from ..handler import Handler
from ..models import Rule

class RuleHandler(Handler):
    def all(self) -> List[Rule]:
        """
        Retrieves all rules.
        """
        path = "rules"
        resp = self.client.request("GET", url_part=path)
        return [Rule.from_dict(rule) for rule in resp.json()["data"]]

    def get(self, id: int) -> Rule:
        """
        Retrieves a rule by its ID.
        """
        path = f"rules/{id}"
        resp = self.client.request("GET", url_part=path)
        return Rule.from_dict(resp.json()["data"])
