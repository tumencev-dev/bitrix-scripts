from bitrix24 import * # библиотека для работы с вебхуками Битрикс

data = {
    "title": "title",
    "description": "Some description",
    "client": {
        "name": "Jon",
        "surname": "Karter",
        "phone": "+77777777777",
        "adress": "st. Mira, 287, Moscow"
        },
    "products": [
        "Candy", 
        "Carrot", 
        "Potato"
        ],
    "delivery_adress": "st. Mira, 211, Ekaterinburg",
    "delivery_date": "2021-01-01:16:00",
    "delivery_code": "#232nkF3fAdn"
    }

bx24 = Bitrix24('https://cd56356.tmweb.ru/rest/1/mdg5cbd63vj7xscr/')

def add_deal(title, description, contact_id, delivery_adress, delivery_date, delivery_code):
     bx24.callMethod(
         'crm.deal.add',
         fields = {
            'TITLE': title,
            'STAGE_ID': 'NEW',
            'COMMENTS': description,
            'CONTACT_ID': contact_id,
            'UF_CRM_1628887616': delivery_adress,
            'UF_CRM_1628887689': delivery_date,
            'UF_CRM_1628887707': delivery_code
         })

# print(bx24.callMethod('crm.deal.list'))
#print(bx24.callMethod('crm.deal.fields'))
#print(bx24.callMethod('crm.contact.list'))
#print(add_deal(data["title"], data["description"], '3', data["delivery_adress"], data["delivery_date"], data["delivery_code"]))
print(bx24.callMethod('crm.deal.productrows.set', id = 23, rows = [{'PRODUCT_ID': 33}]))
#print(bx24.callMethod('crm.deal.productrows.get', id = 23))