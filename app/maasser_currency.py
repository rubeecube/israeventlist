import datetime

from forex_python.converter import CurrencyRates
from datetime import datetime

import re


class MaasserCurrency:
    strip_re = re.compile(f"eur|ils|usd|€|₪|{re.escape('$')}", re.IGNORECASE)
    CURRENCIES = [CURRENCY_ILS, CURRENCY_EUR, CURRENCY_USD] = range(3)

    exchanges_rates = None
    exchanges_rates_time = None

    @classmethod
    def get_exchanges_rates(cls):
        if cls.exchanges_rates is None or (datetime.now() - cls.exchanges_rates_time).days >= 1:
            c = CurrencyRates()
            eur_usd = c.get_rate('EUR', 'USD')
            ils_usd = c.get_rate('ILS', 'USD')
            ils_eur = c.get_rate('ILS', 'EUR')
            cls.exchanges_rates = {
                'EUR:USD': eur_usd,
                'ILS:USD': ils_usd,
                'ILS:EUR': ils_eur,
            }
            cls.exchanges_rates_time = datetime.now()
        return cls.exchanges_rates

    @classmethod
    def exchange(cls, amount, from_currency, to_currency):
        if from_currency not in cls.CURRENCIES:
            return amount
        if to_currency not in cls.CURRENCIES:
            return amount
        if from_currency == to_currency:
            return amount

        rates = MaasserCurrency.get_exchanges_rates()

        if from_currency == cls.CURRENCY_EUR:
            if to_currency == cls.CURRENCY_ILS:
                amount /= rates['ILS:EUR']
            elif to_currency == cls.CURRENCY_USD:
                amount *= rates['EUR:USD']
        elif from_currency == cls.CURRENCY_USD:
            if to_currency == cls.CURRENCY_ILS:
                amount /= rates['ILS:USD']
            elif to_currency == cls.CURRENCY_EUR:
                amount /= rates['EUR:USD']
        elif from_currency == cls.CURRENCY_ILS:
            if to_currency == cls.CURRENCY_EUR:
                amount *= rates['ILS:EUR']
            elif to_currency == cls.CURRENCY_USD:
                amount *= rates['ILS:USD']

        return amount

    @classmethod
    def currency_to_str(cls, currency, symbol=True):
        if currency == cls.CURRENCY_EUR:
            if symbol:
                return "€"
            else:
                return 'EUR'
        if currency == cls.CURRENCY_ILS:
            if symbol:
                return "₪"
            else:
                return 'ILS'
        if currency == cls.CURRENCY_USD:
            if symbol:
                return "$"
            else:
                return 'USD'

    @classmethod
    def str_to_currency(cls, s):
        if s.lower() == 'eur':
            return cls.CURRENCY_EUR
        if s.lower() == 'ils':
            return cls.CURRENCY_ILS
        if s.lower() == 'usd':
            return cls.CURRENCY_USD
        return None

    @classmethod
    def get_currency_from_str(cls, s):
        if 'eur' in s.lower() or '€' in s:
            return MaasserCurrency.CURRENCY_EUR
        elif 'usd' in s.lower() or '$' in s:
            return MaasserCurrency.CURRENCY_USD
        elif 'ils' in s.lower() or '₪' in s:
            return MaasserCurrency.CURRENCY_ILS

    @classmethod
    def strip_currency_from_str(cls, s):
        return float(MaasserCurrency.strip_re.sub('', s))
