"""
Currency converter.

(c) 2018 - laymonage
"""

import requests


def convert(currency_from, currency_to, amount=1):
    """Convert from a currency to another with a given amount."""
    currency_from, currency_to = currency_from.upper(), currency_to.upper()
    query = "{}_{}".format(currency_from, currency_to)
    url = "https://free.currencyconverterapi.com/api/v5/convert?compact=y&q="
    req = requests.get(url + query).json()
    if req:
        result = float(req[query]["val"]) * float(amount)
        result = "{:f}".format(result)
        return ("{} {}  equals  {} {}"
                .format(amount, currency_from,
                        result.rstrip("0").rstrip("."), currency_to))

    return ("Exchange rate not found for {} to {}"
            .format(currency_from, currency_to))
