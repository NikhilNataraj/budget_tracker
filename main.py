import os

from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime

from helper import get_data, get_total, pack_data
from API import read_data, update_row, create_row, create_sheet, delete_sheet, delete_row, convert_to_dict

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


class User(UserMixin):
    def __init__(self, user_id, email, password):
        self.id = user_id
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return User(user_id="1", email=USER, password=PASSWORD)
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
            user = User(user_id="1", email=email, password=PASSWORD)
            login_user(user)
            return redirect(url_for("tracker"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    income_data = convert_to_dict(read_data("Income"))
    expense_data = convert_to_dict(read_data("Expenses"))

    total_income = get_total(income_data)
    total_expenses = get_total(expense_data)
    total_exp_percent = round(total_expenses / total_income * 100)

    month_name = datetime.strptime(income_data[0]["Date"], "%Y-%m-%d").strftime("%B %Y")

    if request.method == 'POST':
        action = request.form.get('action')  # Which Button was clicked

        if action == 'income' or action == 'expense':
            data = pack_data(request.form, len(expense_data))
            create_row(sheet="Income", info=data) if action == 'income' else create_row(sheet="Expenses", info=data)


        elif action == 'edit_income':
            item_id = request.form.get('item_id')
            print(item_id)
            session['item_data'] = get_data(item_id, income_data)
            return redirect(url_for('edit', item_id=item_id, tran="Income"))

        elif action == 'delete_income':
            delete_row("Income", request.form.get('item_id'))

        elif action == 'edit_expense':
            item_id = request.form.get('item_id')
            session['item_data'] = get_data(item_id, expense_data)
            return redirect(url_for('edit', item_id=item_id, tran="Expenses"))

        elif action == 'delete_expense':
            delete_row("Income", request.form.get('item_id'))

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
            data = pack_data(request.form, item_id)
            update_row(sheet=tran, row=f"{int(item_id)+1}", info=data)

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
