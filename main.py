import os
import nltk
import requests

from flask import Flask, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
from datetime import datetime

from helper import add_income, add_expense, delete_expense, delete_income, get_data

load_dotenv()

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
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

    total_exp_percent = round(total_expenses / total_income * 100)

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
            item_id = request.form.get('item_id')
            session['item_data'] = get_data(item_id, income_data)
            return redirect(url_for('edit', item_id=item_id, tran="income"))

        elif action == 'delete_income':
            delete_income(request.form.get('item_id'))

        elif action == 'edit_expense':
            item_id = request.form.get('item_id')
            session['item_data'] = get_data(item_id, expense_data)
            return redirect(url_for('edit', item_id=item_id, tran="expense"))

        elif action == 'delete_expense':
            delete_expense(request.form.get('item_id'))

            # Return response or redirect
        return redirect(url_for('tracker'))

    return render_template("index.html", income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses,
                           total_exp_percent=total_exp_percent,
                           month=month_name)


# TODO = COMPLETE THIS.
@app.route("/edit/<tran>/<item_id>", methods=["GET", "POST"])
def edit(tran, item_id):
    if request.method == "POST":
        redirect(url_for("tracker"))

    item = session.pop('item_data', {})
    return render_template("edit.html", **item)


if __name__ == '__main__':
    app.run(debug=True)