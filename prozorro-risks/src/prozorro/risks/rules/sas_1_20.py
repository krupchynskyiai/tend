from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-20"
    name = "Неоприлюднення тендерної документації"
    description = (
        "Замовник не оприлюднив тендерної документації в електронній системі закупівель"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if "documents" not in tender:
            return RiskFound()
        return RiskNotFound()
