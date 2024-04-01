from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-8"
    name = "Розмір забезпечення тендерної пропозиції визначено з порушенням встановлених Законом України «Про публічні закупівлі» (далі - Закон) граничних значень під час закупівлі товарів або послуг"
    description = (
        "Замовник в оголошенні про проведення конкурентної процедури закупівлі товарів або послуг встановив вимогу щодо надання забезпечення тендерної пропозиції у розмірі, що перевищує 3 відсотки очікуваної вартості закупівлі"
    )
    weight = 0.3

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender):
            expected_value = tender.get("value", {}).get("amount", 0)
            tender_security = tender.get("guarantee", {}).get("amount", 0)
            max_security = 0.03 * expected_value
            if tender_security > max_security:
                return RiskFound()
        return RiskNotFound()
