from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-16"
    name = "Несвоєчасне укладення замовником договору про закупівлю за результатами проведення конкурентної процедури закупівлі"
    description = (
        "Замовник уклав договір про закупівлю пізніше ніж через 20 днів з дня прийняття рішення про намір укласти договір про закупівлю "
        "відповідно до вимог тендерної документації та тендерної пропозиції переможця процедури закупівлі"
    )
    weight = 0.5

    async def process_tender(self, tender):
        decision_date_str = tender.get("decisionDate")
        contract_date_str = tender.get("contracts", [{}])[0].get("dateSigned")
        
        if decision_date_str and contract_date_str:
            decision_date = datetime.strptime(decision_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            contract_date = datetime.strptime(contract_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            days_difference = (contract_date - decision_date).days
            if days_difference > 20:
                return RiskFound()
        
        return RiskNotFound()
