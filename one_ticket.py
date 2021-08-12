from pycbrf import ExchangeRates  # библиотека для получения курса валюты по данным центробанка
from datetime import datetime
from bitrix24 import *  # библиотека для работы с вебхуками Битрикс

bx24 = Bitrix24('https://cd56356.tmweb.ru/rest/1/w9fkw4ybtkyb5y14/')

# получаем курс валют с сайта центробанка на текущую дату
rates = ExchangeRates(datetime.now())

# получаем курс рубля относительно евро
rub_eur = 1 / rates['EUR'].value
# получаем курс евро относительно доллара
eur_usd = rates['EUR'].value / rates['USD'].value
# получаем курс евро относительно казахстанского тенге (делим ещё на 100, т.к. на сайте указывается курс 100 единиц)
eur_kzt = rates['EUR'].value / (rates['KZT'].value / 100)

list_currency = ['USD', 'EUR']
for currency in list_currency:
    print(f'{currency} update: ',
        bx24.callMethod('crm.currency.update',
                        id=currency,
                        fields={
                            "AMOUNT_CNT": "1",
                            "AMOUNT": rates[currency].value
                        }))
print('KZT update: ',
    bx24.callMethod('crm.currency.update',
                    id='KZT',
                    fields={
                        "AMOUNT_CNT": "100",
                        "AMOUNT": rates['KZT'].value
                    }))

print('%.3f' %rub_eur, '%.3f' %eur_usd, '%.3f' %eur_kzt) # вывод курса так как было в задании (не идут в БИТРИКС)
