from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseContractRiskRule

class RiskRule(BaseContractRiskRule):
    identifier = "sas-1-19"
    name = "Укладення договору про закупівлю без проведення конкурентних процедур закупівель/спрощених закупівель"
    description = (
        "Замовник оприлюднив 1 і більше звітів про договір про закупівлю, укладений без використання електронної системи закупівель, "
        "за однаковим кодом предмета закупівлі відповідно до національного класифікатора України ДК 021:2015 «Єдиний закупівельний словник» "
        "(далі - Єдиний закупівельний словник) на загальну суму, що перевищує 50 тис. грн"
    )
    weight = 0.3

    async def process_contract(self, contract):
        if contract.value.amount > 50000:
            item_code = contract.item_classification[0].id
            similar_contracts = [
                c for c in contract.get_similar_contracts() if c.item_classification[0].id == item_code
            ]
            if len(similar_contracts) >= 1:
                return RiskFound()
        return RiskNotFound()
