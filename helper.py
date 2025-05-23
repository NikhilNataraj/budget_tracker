import requests
import os

ADD_INCOME_URL = os.getenv("ADD_INCOME_API")
EDIT_INCOME_URL = os.getenv("EDIT_INCOME_API")
DELETE_INCOME_URL = os.getenv("DELETE_INCOME_API")

ADD_EXPENSE_URL = os.getenv("ADD_EXPENSE_API")
EDIT_EXPENSE_URL = os.getenv("EDIT_EXPENSE_API")
DELETE_EXPENSE_URL = os.getenv("DELETE_EXPENSE_API")


def add_income(data):
    info = {
        "income": data
    }
    response = requests.post(ADD_INCOME_URL, json=info)
    print(response.status_code)
    print(response.text)


def add_expense(data):
    info = {
        "expense": data
    }
    response = requests.post(ADD_EXPENSE_URL, json=info)
    print(response.status_code)
    print(response.text)


def delete_income(item_id):
    url = f"{DELETE_INCOME_URL}/{item_id}"
    response = requests.delete(url)
    print(response.status_code)
    print(response.text)


def delete_expense(item_id):
    url = f"{DELETE_EXPENSE_URL}/{item_id}"
    response = requests.delete(url)
    print(response.status_code)
    print(response.text)


def get_data(item_id, data):
    item = None
    for i in data:
        if i['id'] == int(item_id):
            item = {
                'id': item_id,
                'description': i['description'],
                'amount': i['amount'],
                'method': i['method'],
            }
    return item
