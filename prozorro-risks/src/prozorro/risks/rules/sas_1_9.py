from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-9"
    name = "Незастосування конкурентних процедур закупівель, визначених Законом, під час закупівлі товарів або послуг"
    description = (
        "Замовник здійснив закупівлю товарів або послуг без проведення конкурентних процедур закупівель, визначених Законом, на суму, що дорівнює або перевищує 200 тис. грн"
    )
    weight = 0.2

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender):
            expected_value = tender.get("value", {}).get("amount", 0)
            if expected_value >= 200000:
                return RiskFound()
        return RiskNotFound()
