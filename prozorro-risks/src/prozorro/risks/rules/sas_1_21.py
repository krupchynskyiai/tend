from datetime import datetime
from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-21"
    name = "Порушення строку оприлюднення тендерної документації під час проведення відкритих торгів та конкурентного діалогу"
    description = (
        "Недотримання замовником вимоги оприлюднити тендерну документацію в установлені Законом строки "
        "(пізніше ніж за 15 днів до встановленого в оголошенні кінцевого строку подання тендерних пропозицій)"
    )
    weight = 0.4

    async def process_tender(self, tender):
        if "tenderPeriod" in tender:
            tender_end_date = tender["tenderPeriod"]["endDate"]
            if tender_end_date and is_more_than_fifteen_days(tender_end_date):
                return RiskFound()
        return RiskNotFound()

def is_more_than_fifteen_days(tender_end_date):
    tender_end_datetime = datetime.strptime(tender_end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_datetime = datetime.now()
    difference = current_datetime - tender_end_datetime
    return difference.days > 15
