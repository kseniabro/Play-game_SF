import requests
import json
from config import keys


class ConvertationException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def converter(base: str, quote: str, amount: str):
        if base == quote:
            raise ConvertationException(f'Невозможно пееревести одинаковые валюты {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertationException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertationException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertationException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        total_base *= amount

        return total_base
