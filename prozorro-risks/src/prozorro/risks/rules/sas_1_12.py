from datetime import datetime
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-12"
    name = "Перевищення строку розгляду тендерних пропозицій у разі проведення конкурентної процедури закупівлі (оголошення з публікацією англійською мовою)"
    description = "Замовник перевищив строк (понад 20 робочих днів) розгляду тендерних пропозицій у разі проведення конкурентної процедури закупівлі, очікувана вартість якої перевищує суму еквівалентну 133 тис. євро"
    weight = 0.3

    def is_more_than_twenty_days(self, proposal_review_date):
        proposal_review_datetime = datetime.strptime(proposal_review_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_datetime = datetime.now()
        difference = current_datetime - proposal_review_datetime
        return difference.days > 20

    async def process_tender(self, tender):
        if tender.get("value", {}).get("amount") and tender["value"]["amount"] > 133000:
            proposal_review_date = tender.get("awardPeriod", {}).get("endDate")
            if proposal_review_date and self.is_more_than_twenty_days(proposal_review_date):
                return RiskFound()
        return RiskNotFound()
