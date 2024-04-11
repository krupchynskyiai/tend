
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-13"
    name = "Невиконання замовником рішення органу оскарження"
    description = "Після прийнятого органом оскарження рішення замовник не здійснив заходів щодо усунення порушення процедури закупівлі"
    weight = 0.5

    async def process_tender(self, tender):
        if "complaints" in tender:
            for complaint in tender["complaints"]:
                if complaint.get("status", "") == "resolved":
                    return RiskNotFound()
        return RiskFound()

