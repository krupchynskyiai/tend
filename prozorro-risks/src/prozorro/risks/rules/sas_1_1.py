from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-1"
    name = "Використання переговорної процедури закупівлі за відсутності законодавчих підстав (двічі відмінені процедури відкритих торгів)"
    description = (
        "Замовник застосовує переговорну процедуру закупівлі, але в електронній системі закупівель не виявлено двох "
        "процедур відкритих торгів щодо придбання такого самого предмета закупівлі, у тому числі частково (за лотом), "
        "які були відмінені через відсутність достатньої кількості тендерних пропозицій"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            open_procurements = [
                lot["relatedLot"] for lot in tender.get("lots", []) if lot.get("status", "") == "cancelled"
            ]
            if len(open_procurements) >= 2:
                return RiskFound()
        return RiskNotFound()
