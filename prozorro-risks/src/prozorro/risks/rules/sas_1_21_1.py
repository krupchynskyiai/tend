from datetime import datetime
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-21-1"
    name = "Порушення строку оприлюднення тендерної документації під час проведення відкритих торгів та конкурентного діалогу (оголошення з публікацією англійською мовою)"
    description = (
        "Недотримання замовником вимоги оприлюднити тендерну документацію в строки "
        "(пізніше ніж за 30 днів до встановленого в оголошенні кінцевого строку подання тендерних пропозицій)"
    )
    weight = 0.4

    async def process_tender(self, tender):
        if "tenderPeriod" in tender:
            tender_end_date = tender["tenderPeriod"]["endDate"]
            if tender_end_date and is_more_than_thirty_days(tender_end_date):
                return RiskFound()
        return RiskNotFound()

def is_more_than_thirty_days(tender_end_date):
    tender_end_datetime = datetime.strptime(tender_end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_datetime = datetime.now()
    difference = tender_end_datetime - current_datetime
    return difference.days > 30
