from pycbrf import ExchangeRates  # библиотека для получения курса валюты по данным центробанка
from datetime import datetime

# получаем курс валют с сайта центробанка на текущую дату
rates = ExchangeRates(datetime.now())

# получаем курс рубля относительно евро
rub_eur = 1 / float(rates['EUR'].value)
# получаем курс евро относительно доллара
eur_usd = float(rates['EUR'].value) / float(rates['USD'].value)
# получаем курс евро относительно казахстанского тенге (делим ещё на 100, т.к. на сайте указывается курс 100 единиц)
eur_kzt = float(rates['EUR'].value) / (float(rates['KZT'].value) / 100)

print('%.3f' %rub_eur, '%.3f' %eur_usd, '%.3f' %eur_kzt)