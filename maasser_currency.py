import datetime

from forex_python.converter import CurrencyRates
from datetime import timedelta, datetime


class MaasserCurrency:
    exchanges_rates = None
    exchanges_rates_time = None

    @classmethod
    def get_exchanges_rates(cls):
        if cls.exchanges_rates is None or (datetime.now() - cls.exchanges_rates_time).days >= 1:
            c = CurrencyRates()
            ils_usd = c.get_rate('ILS', 'USD')
            ils_eur = c.get_rate('ILS', 'EUR')
            cls.exchanges_rates = {
                'ILS:USD': ils_usd,
                'ILS:EUR': ils_eur,
            }
            cls.exchanges_rates_time = datetime.now()
        return cls.exchanges_rates