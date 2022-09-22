import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == amount:
            raise APIException(f'Используйте название валюты из списка валют. /help')
        elif base == amount:
            raise APIException(f'Используйте название валюты из списка валют. /help')
        elif quote == base:
            raise APIException(f'Валюты не должны быть идентичны.'\
                               f'Невозможно конвертировать идентичную валюту. /help')
        else:
            ...
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не могу конвертировать указанную валюту "{quote}". Проверьте список валют. /values')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не могу конвертировать указанную валюту "{base}" . Проверьте список валют: /values')
        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException(f'Некорректное значение валюты. /help')
        except ValueError:
            raise APIException(f'Кол-во валюты следует вводить в виде числового значения/дроби.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base