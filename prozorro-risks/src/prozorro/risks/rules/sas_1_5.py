from datetime import datetime, timedelta
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-5"
    name = "Перевищення строку оприлюднення оголошення з відомостями про укладену рамкову угоду"
    description = (
        "Неоприлюднення або несвоєчасне оприлюднення замовником оголошення з відомостями про укладену рамкову угоду "
        "(у разі здійснення закупівлі за рамковими угодами) (не пізніше ніж через сім робочих днів з дня укладення рамкової угоди)"
    )
    weight = 0.5

    async def process_tender(self, tender):
        if self.tender_matches_requirements(tender, category=False):
            framework_agreement_date = tender.get("dateFrameworkAgreement")
            if framework_agreement_date:
                expected_notice_date = framework_agreement_date + timedelta(days=7)
                current_date = datetime.now().date()
                if current_date > expected_notice_date:
                    return RiskFound()
        return RiskNotFound()
