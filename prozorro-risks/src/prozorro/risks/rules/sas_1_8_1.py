from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-8-1"
    name = "Розмір забезпечення тендерної пропозиції визначено з порушенням встановлених Законом граничних значень під час закупівлі робіт"
    description = (
        "Замовник в оголошенні про проведення конкурентної процедури закупівлі робіт встановив вимогу щодо надання забезпечення тендерної пропозиції у розмірі, що перевищує 0,5 відсотка очікуваної вартості закупівлі"
    )
    weight = 0.3

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender):
            expected_value = tender.get("value", {}).get("amount", 0)
            tender_security = tender.get("guarantee", {}).get("amount", 0)
            max_security = 0.005 * expected_value
            if tender_security > max_security:
                return RiskFound()
        return RiskNotFound()
