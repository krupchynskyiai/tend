from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-7"
    name = "Перевищення строку розгляду тендерної пропозиції, яку за результатами оцінки визначено найбільш економічно вигідною"
    description = (
        "Замовник перевищив строк розгляду (понад п’ять робочих днів) тендерної пропозиції, яку за результатами оцінки визначено найбільш економічно вигідною, та не оприлюднив повідомлення про продовження строку розгляду тендерної пропозиції"
    )
    weight = 0.3

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender):
            end_date = tender.get("tenderPeriod", {}).get("endDate")
            if end_date:
                expected_end_date = end_date + timedelta(days=5)
                current_date = datetime.now().date()
                if current_date > expected_end_date:
                    return RiskFound()
        return RiskNotFound()
