from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseContractRiskRule

class RiskRule(BaseContractRiskRule):
    identifier = "sas-1-6"
    name = "Порушення строку оприлюднення повідомлення про внесення змін до договору про закупівлю"
    description = (
        "Несвоєчасне оприлюднення замовником повідомлення про внесення змін до договору про закупівлю протягом трьох робочих днів з дня внесення таких змін"
    )
    weight = 0.5

    async def process_contract(self, contract):
        if self.contract_matches_requirements(contract):
            changes_date = contract.get("dateSigned")
            if changes_date:
                expected_notice_date = changes_date + timedelta(days=3)
                current_date = datetime.now().date()
                if current_date > expected_notice_date:
                    return RiskFound(type="contract", id=contract["id"])
        return RiskNotFound()
