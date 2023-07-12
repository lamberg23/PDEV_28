import requests
import json
from config import keys




class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote:str,base:str, amount:str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты "{base}"')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}" \nВыберите валюту /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обрабоать валюту "{base}" \nВыберите валюту /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey=RtftfXTKATkpc1EVjEZ3vLBUHYtB9AYNILhE3Xzu&currencies={base_ticker}&base_currency={quote_ticker}')

        price = json.loads(r.content)['data'][f'{keys[base]}']['value']
        total_price = round((price * int(amount)),2)

        return total_price
