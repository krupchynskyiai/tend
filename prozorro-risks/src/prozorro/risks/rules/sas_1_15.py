from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseContractRiskRule

class RiskRule(BaseContractRiskRule):
    identifier = "sas-1-15"
    name = "Неоприлюднення договору про закупівлю в електронній системі закупівель"
    description = "Відсутність оприлюдненого договору про закупівлю за результатами конкурентної процедури закупівлі/спрощеної закупівлі"
    weight = 0.5

    async def process_contract(self, contract):
        if contract.get("status", "") == "active":
            return RiskNotFound()
        return RiskFound()
