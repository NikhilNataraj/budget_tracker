import os
import requests

from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime

from helper import add_income, add_expense, delete_expense, delete_income, get_data

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

# GET_INCOME_URL = os.getenv("GET_INCOME_API")
ADD_INCOME_URL = os.getenv("ADD_INCOME_API")
EDIT_INCOME_URL = os.getenv("EDIT_INCOME_API")
DELETE_INCOME_URL = os.getenv("DELETE_INCOME_API")

# GET_EXPENSE_URL = os.getenv("GET_EXPENSE_API")
ADD_EXPENSE_URL = os.getenv("ADD_EXPENSE_API")
EDIT_EXPENSE_URL = os.getenv("EDIT_EXPENSE_API")
DELETE_EXPENSE_URL = os.getenv("DELETE_EXPENSE_API")


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":  # fixed ID for now
        return User(id="1", email=USER, password=PASSWORD)
    return None

@app.route("/")
def reroute():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == USER and check_password_hash(PASSWORD, password):
            user = User(id="1", email=email, password=PASSWORD)
            login_user(user)
            return redirect(url_for("tracker"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    # income_data = requests.get(GET_INCOME_URL).json()['income']
    # expense_data = requests.get(GET_EXPENSE_URL).json()['expenses']

    income_data = [{'date': '2025-05-01', 'description': 'Salary', 'amount': 49840, 'method': 'Account', 'id': 2}]
    expense_data = [{'date': '2025-05-04', 'description': 'Rent', 'amount': 16500, 'method': 'Cash', 'id': 2},
                    {'date': '2025-05-10', 'description': 'Investments', 'amount': 20000, 'method': 'Account', 'id': 3},
                    {'date': '2025-05-24', 'description': 'Flight tickets', 'amount': 3588, 'method': 'Card', 'id': 4}]

    total_income = 0
    for inc in income_data:
        total_income += inc['amount']

    total_expenses = 0
    for exp in expense_data:
        total_expenses += exp['amount']

    total_exp_percent = round(total_expenses / total_income * 100)

    month_name = datetime.strptime(income_data[0]["date"], "%Y-%m-%d").strftime("%B %Y")

    if request.method == 'POST':

        action = request.form.get('action')  # Which Button was clicked

        if action == 'income':
            description = request.form.get('description')
            amount = float(request.form.get('amount'))
            method = request.form.get('method')
            tran_date = request.form.get('date')
            data = {
                "date": tran_date,
                "description": description,
                "amount": amount,
                "method": method
            }
            add_income(data)

        elif action == 'expense':
            description = request.form.get('description')
            amount = float(request.form.get('amount'))
            method = request.form.get('method')
            tran_date = request.form.get('date')
            data = {
                "date": tran_date,
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
            print(item_id)
            session['item_data'] = get_data(item_id, expense_data)
            return redirect(url_for('edit', item_id=item_id, tran="expense"))

        elif action == 'delete_expense':
            delete_expense(request.form.get('item_id'))

            # Return response or redirect
        return redirect(url_for('tracker'))

    return render_template("index.html", income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses,
                           total_exp_percent=total_exp_percent,
                           month=month_name, logged_in=True)


@app.route("/edit/<tran>/<item_id>", methods=["GET", "POST"])
def edit(tran, item_id):
    if request.method == "POST":
        action = request.form.get('action')  # Which Button was clicked
        if action == "save":
            description = request.form.get('description')
            amount = float(request.form.get('amount'))
            method = request.form.get('method')
            tran_date = request.form.get('date')
            data = {
                tran: {
                    "date": tran_date,
                    "description": description,
                    "amount": amount,
                    "method": method
                }
            }
            print(data)
            if tran == "income":
                edit_url = f"{EDIT_INCOME_URL}/{item_id}"
            else:
                edit_url = f"{EDIT_EXPENSE_URL}/{item_id}"

            response = requests.put(edit_url, json=data)
            print(response.status_code)
            print(response.text)

        return redirect(url_for("tracker"))

    item = session.pop('item_data', {})
    item['tran'] = tran
    return render_template("edit.html", **item)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
