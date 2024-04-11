from datetime import datetime
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-11"
    name = "Ненадання або несвоєчасне надання замовником відповіді на звернення учасника з вимогою щодо надання додаткової інформації стосовно причин невідповідності його пропозиції умовам тендерної документації"
    description = "Замовник не надав відповіді протягом п’яти днів з дня надходження такого звернення від учасника через електронну систему закупівель з вимогою щодо надання додаткової інформації стосовно причин невідповідності його пропозиції умовам тендерної документації, від учасника, тендерна пропозиція якого відхилена"
    weight = 0.3

    def is_more_than_five_days(self, enquiry_date):
        enquiry_datetime = datetime.strptime(enquiry_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        current_datetime = datetime.now()
        difference = current_datetime - enquiry_datetime
        return difference.days > 5

    async def process_tender(self, tender):
        enquiries = tender.get("enquiries", [])
        for enquiry in enquiries:
            enquiry_date = enquiry.get("date")
            if enquiry_date and self.is_more_than_five_days(enquiry_date):
                return RiskFound()
        return RiskNotFound()
