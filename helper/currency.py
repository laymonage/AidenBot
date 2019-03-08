"""
Currency converter.

(c) 2018 - laymonage
"""

import os
import requests


def convert(currency_from, currency_to, amount=1):
    """Convert from a currency to another with a given amount."""
    api_key = os.getenv('CURRENCY_CONVERTER_API_KEY', None)
    if not api_key:
        return "Currency Converter API is not configured."
    currency_from, currency_to = currency_from.upper(), currency_to.upper()
    query = "{}_{}".format(currency_from, currency_to)
    url = "https://free.currencyconverterapi.com/api/v6/convert?compact=ultra"
    req = requests.get(url + "&apiKey={}&q={}".format(api_key, query)).json()
    if req:
        result = float(req[query]) * float(amount)
        result = "{:f}".format(result)
        return ("{} {}  equals  {} {}"
                .format(amount, currency_from,
                        result.rstrip("0").rstrip("."), currency_to))

    return ("Exchange rate not found for {} to {}"
            .format(currency_from, currency_to))
