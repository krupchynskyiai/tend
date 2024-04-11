from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-2-4"
    name = "Відхилення тендерних пропозицій всіх учасників, крім переможця"
    description = (
        "Є ймовірність ризику упередженого розгляду замовником тендерних пропозицій з метою визначення "
        "конкретного учасника переможцем процедури закупівлі та укладення договору про закупівлю з порушенням "
        "принципів здійснення закупівель"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if "awards" in tender:
            for award in tender["awards"]:
                if award.get("status", "") == "active" and award.get("complaints", []):
                    return RiskFound()
        return RiskNotFound()
