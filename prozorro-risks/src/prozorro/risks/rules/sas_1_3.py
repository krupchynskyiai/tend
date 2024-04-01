from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-3"
    name = "Використання переговорної процедури закупівлі за відсутності законодавчих підстав (невідповідність підстав предмета закупівлі)"
    description = (
        "Замовник під час проведення переговорної процедури зазначає обґрунтування, яке не відповідає обраній підставі"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            justification = tender.get("justification")
            procurement_rationale = tender.get("procurementMethodRationale")
            if justification and procurement_rationale and justification != procurement_rationale:
                return RiskFound()
        return RiskNotFound()
