from flask import Flask, request # использую для запуска локального сервера
from bitrix24 import * # библиотека для работы с вебхуками Битрикс
import requests

bx24 = Bitrix24('https://cd56356.tmweb.ru/rest/1/mdg5cbd63vj7xscr/')

app = Flask(__name__)

def get_contact(name, surname, phone, adress): # Функция для проверки контакта, создания и обновления
    get_contact = bx24.callMethod(
        'crm.contact.list',
        filter={
            'NAME': name,
            'LAST_NAME': surname,
            'PHONE': phone,
            'ADRESS': adress
        }
    )
    if get_contact == []:
        call = bx24.callMethod(
            'crm.contact.add', # Возвращает ID созданного контакта
            fields={
                'NAME': name,
                'LAST_NAME': surname,
                'PHONE': [
                    {
                        'VALUE': phone,
                        'VALUE_TYPE': 'WORK'
                    }],
                'ADRESS': adress
            }
        )
        result = str(call)
    else:
        call = bx24.callMethod(
            'crm.contact.update', # Возвращает True если контакт обновлен
            id = get_contact[0]['ID'],
            fields = {
                'NAME': name,
                'LAST_NAME': surname,
                'PHONE': phone,
                'ADRESS': adress
            }
        )
        if call == True:
            result = str(get_contact[0]['ID'])
    return result

def get_product_list_id(product_list): # Функция для поиска продуктов и получения списка их ID
    list_id = []
    for product in product_list:
        call = bx24.callMethod('crm.product.list', filter = {'NAME': product})
        list_id.append(int(call[0]['ID']))
    return list_id

def get_deal(code): # Функция поиска сделки по коду доставки
    call = bx24.callMethod(
        'crm.deal.list',
        filter = {
            'UF_CRM_1628887707': code.replace('#','')
        }
    )
    return call

def add_deal(title, description, contact, delivery_adress, delivery_date, delivery_code):
    bx24.callMethod(
        'crm.deal.add',
        fields = {
            'TITLE': title,
            'STAGE_ID': 'NEW',
            'COMMENTS': description,
            'CONTACT_ID': contact,
            'UF_CRM_1628887616': delivery_adress,
            'UF_CRM_1628887689': delivery_date,
            'UF_CRM_1628887707': delivery_code.replace('#','')
        })

def add_product(id, product_list): # Функция добавления продуктов в сделку
    url = f"https://cd56356.tmweb.ru/rest/1/mdg5cbd63vj7xscr/crm.deal.productrows.set.json?id={id}&"
    for i in range(0, len(product_list)):
        url = url + f"rows[{i}][PRODUCT_ID]={product_list[i]}&"
    requests.get(url)

@app.route('/', methods=['POST'])
def result():
    data = request.json
    try:
        contact_id = get_contact(data['client']['name'], data['client']['surname'], data['client']['phone'], data['client']['adress'])
        list_products = get_product_list_id(data['products'])
        deal = get_deal(data['delivery_code'])[0]['ID']
        if get_deal(data['delivery_code']) == []:
            add_deal(data["title"], data["description"], contact_id, data["delivery_adress"], data["delivery_date"], data["delivery_code"])
            add_product(deal, list_products)
            return 'add Deal\n'
        else:
            bx24.callMethod(
                'crm.deal.update',
                id = get_deal(data['delivery_code'])[0]['ID'],
                fields = {
                    'TITLE': data['title'],
                    'STAGE_ID': 'NEW',
                    'COMMENTS': data["description"],
                    'CONTACT_ID': contact_id,
                    'UF_CRM_1628887616': data["delivery_adress"],
                    'UF_CRM_1628887689': data["delivery_date"],
                    'UF_CRM_1628887707': data["delivery_code"].replace('#','')
                }
            )
            add_product(deal, list_products)
            return 'update Deal\n'
    except BitrixError as message:
        return message

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
