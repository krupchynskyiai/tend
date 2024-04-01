from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-2-1"
    name = "Використання переговорної процедури закупівлі за відсутності законодавчих підстав (додаткова закупівля робіт, послуг)"
    description = (
        "Замовник застосовує переговорну процедуру закупівлі для закупівлі додаткових аналогічних робіт чи послуг в того "
        "самого учасника за умови, що закупівля додаткових робіт чи послуг була здійснена протягом трьох років після "
        "укладення основного договору про закупівлю в того самого учасника, та не перевищує 50 відсотків ціни основного "
        "договору про закупівлю, але в електронній системі закупівель не виявлено закупівлі в того самого учасника"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            additional_procurements = [
                proc["id"] for proc in tender.get("relatedProcesses", []) if proc.get("relationship", "") == "additional"
            ]
            three_years_ago_date = self._three_years_ago_date()
            filtered_procurements = [
                proc for proc in additional_procurements if proc.get("date", "") >= three_years_ago_date
            ]
            if len(filtered_procurements) <= 0.5 * tender["value"]["amount"]:
                return RiskFound()
        return RiskNotFound()

    def _three_years_ago_date(self):
        current_date = datetime.now()
        three_years_ago = current_date - timedelta(days=3 * 365)
        return three_years_ago
