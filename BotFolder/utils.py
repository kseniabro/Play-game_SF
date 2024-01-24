import requests
import json
from config import values


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def converter(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Невозможно пееревести одинаковые валюты {base}.')

        try:
            base_ticker = values[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = values[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[values[quote]]
        total_base *= amount

        return total_base
