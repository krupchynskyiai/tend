from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-17"
    name = "Несвоєчасне укладення замовником договору про закупівлю за результатами проведення переговорної процедури закупівлі"
    description = (
        "Замовник уклав договір про закупівлю пізніше ніж через 35 днів з дня оприлюднення в електронній системі закупівель "
        "повідомлення про намір укласти договір про закупівлю під час застосування переговорної процедури"
    )
    weight = 0.5

    async def process_tender(self, tender):
        publish_date_str = tender.get("tenderPeriod", {}).get("startDate")
        contract_date_str = tender.get("contracts", [{}])[0].get("dateSigned")
        
        if publish_date_str and contract_date_str:
            publish_date = datetime.strptime(publish_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            contract_date = datetime.strptime(contract_date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            days_difference = (contract_date - publish_date).days
            if days_difference > 35:
                return RiskFound()
        
        return RiskNotFound()
