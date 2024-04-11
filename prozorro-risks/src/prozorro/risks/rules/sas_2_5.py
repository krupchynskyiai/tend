from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-2-5"
    name = "Уникнення застосування конкурентних процедур закупівель товарів чи послуг"
    description = (
        "Замовник протягом календарного року проводить закупівлю товарів чи послуг за одним і тим самим кодом "
        "Єдиного закупівельного словника, за яким він вже здійснював закупівлі, що в сумі дорівнюють або перевищують "
        "200,0 тис. грн"
    )
    weight = 0.1

    async def process_tender(self, tender):
        procurement_code = tender.get("procurementCode", "")
        if "procuringEntity" in tender and "identifier" in tender["procuringEntity"]:
            entity_identifier = tender["procuringEntity"]["identifier"]["id"]
            if procurement_code in procurement_history(entity_identifier):
                total_amount = sum_of_purchases(procurement_code)
                if total_amount >= 200000:
                    return RiskFound()
        return RiskNotFound()

def procurement_history(entity_identifier): #TODO
    pass

def sum_of_purchases(procurement_code): #TODO
    pass
