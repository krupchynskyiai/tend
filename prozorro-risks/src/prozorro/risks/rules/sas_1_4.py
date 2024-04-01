from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-4"
    name = "Порушення порядку оприлюднення оголошення про проведення конкурентних процедур закупівель товарів та послуг"
    description = (
        "Замовник додатково не оприлюднив англійською мовою в електронній системі закупівель оголошення про проведення "
        "процедури закупівлі товарів та/або послуг, очікувана вартість якої перевищує суму еквівалентну 133 тис. євро"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            notice = tender.get("notice")
            if notice:
                if notice.get("language") != "en":
                    if tender.get("value", {}).get("amount", 0) > 133_000:
                        return RiskFound()
        return RiskNotFound()
