import requests
from main import ADD_EXPENSE_URL, ADD_INCOME_URL, DELETE_EXPENSE_URL, DELETE_INCOME_URL

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


def edit_income(item_id):
   pass


def edit_expense(item_id):
    pass


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