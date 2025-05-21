import os
import nltk
import requests

from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
# from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

app = Flask(__name__)
Bootstrap(app)

# GET_INCOME_URL = os.getenv("GET_INCOME_API")
ADD_INCOME_URL = os.getenv("ADD_INCOME_API")
EDIT_INCOME_URL = os.getenv("EDIT_INCOME_API")
DELETE_INCOME_URL = os.getenv("DELETE_INCOME_API")

# GET_EXPENSE_URL = os.getenv("GET_EXPENSE_API")
ADD_EXPENSE_URL = os.getenv("ADD_EXPENSE_API")
EDIT_EXPENSE_URL = os.getenv("EDIT_EXPENSE_API")
DELETE_EXPENSE_URL = os.getenv("DELETE_EXPENSE_API")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/", methods=["GET", 'POST'])
def tracker():
    # income_data = requests.get(GET_INCOME_URL).json()['income']
    # expense_data = requests.get(GET_EXPENSE_URL).json()['expenses']

    income_data = [{'date': '01/05/2025', 'description': 'Salary', 'amount': 49840, 'method': 'Account', 'id': 2}]
    expense_data = [{'date': '05/05/2025', 'description': 'Rent', 'amount': 16500, 'method': 'Cash', 'id': 2},
                    {'date': '10/05/2025', 'description': 'Investments', 'amount': 20000, 'method': 'Account', 'id': 3}]

    total_income = 0
    for inc in income_data:
        total_income += inc['amount']

    total_expenses = 0
    for exp in expense_data:
        total_expenses += exp['amount']

    total_exp_percent = round(total_expenses/total_income * 100)

    month_name = datetime.strptime(income_data[0]["date"], "%d/%m/%Y").strftime("%B %Y")

    if request.method == 'POST':

        action = request.form.get('action')  # 'income' or 'expense'

        if action == 'income':
            description = request.form.get('description')
            amount = float(request.form.get('amount'))
            method = request.form.get('method')
            data = {
                "date": datetime.now().strftime("%d/%m/%Y"),
                "description": description,
                "amount": amount,
                "method": method
            }
            # process as income
            add_income(data)

        elif action == 'expense':
            description = request.form.get('description')
            amount = float(request.form.get('amount'))
            method = request.form.get('method')
            data = {
                "date": datetime.now().strftime("%d/%m/%Y"),
                "description": description,
                "amount": amount,
                "method": method
            }
            # process as expense
            add_expense(data)

        elif action == 'edit_income':
            # TODO = FIX THIS!!
            item_id=request.form.get('item_id')
            # edit_income(income_data[i for i in income_data if i['id']==item_id])
            edit_income(item_id)

        elif action == 'delete_income':
            delete_income(request.form.get('item_id'))

        elif action == 'edit_expense':
            edit_expense(request.form.get('item_id'))

        elif action == 'delete_expense':
            delete_expense(request.form.get('item_id'))


            # Return response or redirect
        return redirect(url_for('tracker'))

    return render_template("index.html", income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses, total_exp_percent=total_exp_percent,
                           month=month_name)


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
    response = requests.post(ADD_INCOME_URL, json=info)
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

# TODO = COMPLETE THIS.
@app.route("/edit/<item_id>")
def edit(item_id):
    print(item_id)
    return render_template("edit.html")


if __name__ == '__main__':
    app.run(debug=True)
