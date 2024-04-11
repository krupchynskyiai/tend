from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseContractRiskRule

class RiskRule(BaseContractRiskRule):
    identifier = "sas-1-14"
    name = "Неоприлюднення звіту про виконання договору"
    description = "Замовник не оприлюднив звіту про виконання договору у строки, встановлені Законом"
    weight = 0.3

    async def process_contract(self, contract):
        if contract.get("status", "") == "active":
            if not contract.get("documents") or not any(
                doc.get("documentType", "") == "contractAnnex" for doc in contract["documents"]
            ):
                return RiskFound()
        return RiskNotFound()
