from prozorro.risks.models import RiskFound, RiskNotFound
from prozorro.risks.rules.base import BaseTenderRiskRule
from datetime import datetime, timedelta

class RiskRule(BaseTenderRiskRule):
    identifier = "sas-1-10"
    name = "Ненадання або несвоєчасне надання роз’яснень замовником щодо тендерної документації"
    description = (
        "Замовник протягом трьох робочих днів з дня оприлюднення звернення за роз’ясненнями або вимоги щодо усунення "
        "порушення не надав/несвоєчасно надав роз’яснення на таке звернення та/або не оприлюднив/оприлюднив його з порушенням "
        "строків у електронній системі закупівель"
    )
    weight = 0.4

    async def process_tender(self, tender):
        publication_date = datetime.strptime(tender["date"], "%Y-%m-%dT%H:%M:%SZ")
        deadline_date = publication_date + timedelta(days=3)
        clarification_requested = "clarifications" in tender
        if not clarification_requested or datetime.now() > deadline_date:
            return RiskFound()
        return RiskNotFound()
