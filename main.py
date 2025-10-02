import os

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime

# UPDATED IMPORTS to use local database and helper functions
from helper import get_total, unpack_data
import db as database

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
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
    # REPLACED API calls with much faster local DB calls
    income_data = database.get_transactions("income")
    expense_data = database.get_transactions("expense")

    total_income = get_total(income_data)
    total_expenses = get_total(expense_data)

    # Prevent division by zero error
    total_exp_percent = 0
    if total_income > 0:
        total_exp_percent = round(total_expenses / total_income * 100)

    # Display the current month by default
    month_name = datetime.now().strftime("%B %Y")
    # If there is income data, use its date to determine the month
    if income_data:
        try:
            month_name = datetime.strptime(income_data[0]["date"], "%Y-%m-%d").strftime("%B %Y")
        except (ValueError, IndexError):
            # Handle cases with bad date format or no data
            pass


    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'income' or action == 'expense':
            data = unpack_data(request.form)
            database.add_transaction(action, data)

        elif action == 'edit_income':
            item_id = request.form.get('item_id')
            return redirect(url_for('edit', tran_type="income", item_id=item_id))

        elif action == 'delete_income':
            database.delete_transaction("income", request.form.get('item_id'))

        elif action == 'edit_expense':
            item_id = request.form.get('item_id')
            return redirect(url_for('edit', tran_type="expense", item_id=item_id))

        elif action == 'delete_expense':
            database.delete_transaction("expense", request.form.get('item_id'))

        return redirect(url_for('tracker'))

    return render_template("index.html", income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses,
                           total_exp_percent=total_exp_percent,
                           month=month_name, logged_in=True)


@app.route("/edit/<tran_type>/<item_id>", methods=["GET", "POST"])
@login_required
def edit(tran_type, item_id):
    # Fetch the specific item directly from the database
    item = database.get_single_transaction(tran_type, item_id)
    if not item:
        flash("Record not found!")
        return redirect(url_for('tracker'))

    if request.method == "POST":
        action = request.form.get('action')

        if action == "save":
            data = unpack_data(request.form)
            database.update_transaction(tran_type, item_id, data)

        return redirect(url_for("tracker"))

    # Pass the database row object and transaction type to the template
    return render_template("edit.html", item=item, tran_type=tran_type)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
