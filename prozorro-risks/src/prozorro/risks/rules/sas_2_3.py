from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-2-3"
    name = "Переможцем закупівлі обрано учасника, у якого не завантажено жодного файлу або документа"
    description = (
        "Є ймовірність порушення вимог Закону щодо невідхилення замовником тендерної пропозиції переможця "
        "процедури закупівлі через її невідповідність умовам тендерної документації"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if "awards" in tender:
            for award in tender["awards"]:
                if award.get("status", "") == "active":
                    if not award["documents"]:
                        return RiskFound()
        return RiskNotFound()
