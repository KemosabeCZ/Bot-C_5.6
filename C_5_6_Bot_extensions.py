import json
import requests
from C_5_6_Bot_config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(amount, base, summa):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            summa_key = exchanges[summa.lower()]
        except KeyError:
            raise APIException(f"Валюта {summa} не найдена")

        if base_key == summa_key:
            raise APIException(f'Попытка конвертации в исходную валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        a = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_key}&symbols={summa_key}')
        response = json.loads(a.content)
        result_amount = response['rates'][summa_key] * amount  # значение из значения /курс/ * amount
        result_amount = round(result_amount, 2)
        message = f'{amount} {base} сейчас это : {result_amount} {summa}'
        return message
