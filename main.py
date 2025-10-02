import os

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from datetime import datetime

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
def home():
    books = database.get_books()
    if books:
        return redirect(url_for("tracker", book_name=books[0]['name']))
    # If there are absolutely no books, create the default one and redirect
    database.add_book("Default Book")
    return redirect(url_for("tracker", book_name="Default Book"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == USER and check_password_hash(PASSWORD, password):
            user = User(id="1", email=email, password=PASSWORD)
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/tracker/<book_name>", methods=["GET", "POST"])
@login_required
def tracker(book_name):
    all_books = database.get_books()
    current_book = database.get_book_by_name(book_name)

    if not current_book:
        flash(f"Book '{book_name}' not found!")
        return redirect(url_for('home'))

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'income' or action == 'expense':
            data = unpack_data(request.form)
            database.add_transaction(action, data, current_book['id'])

        elif action == 'edit_income':
            return redirect(
                url_for('edit', book_name=book_name, tran_type="income", item_id=request.form.get('item_id')))

        elif action == 'delete_income':
            database.delete_transaction("income", request.form.get('item_id'))

        elif action == 'edit_expense':
            return redirect(
                url_for('edit', book_name=book_name, tran_type="expense", item_id=request.form.get('item_id')))

        elif action == 'delete_expense':
            database.delete_transaction("expense", request.form.get('item_id'))

        return redirect(url_for('tracker', book_name=book_name))

    income_data = database.get_transactions("income", current_book['id'])
    expense_data = database.get_transactions("expense", current_book['id'])
    total_income = get_total(income_data)
    total_expenses = get_total(expense_data)

    total_exp_percent = round(total_expenses / total_income * 100) if total_income > 0 else 0
    month_name = datetime.now().strftime("%B %Y")

    return render_template("index.html",
                           income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses,
                           total_exp_percent=total_exp_percent, month=month_name,
                           books=all_books, current_book=current_book, logged_in=True)


@app.route("/add_book", methods=["POST"])
@login_required
def add_book():
    book_name = request.form.get("book_name")
    if book_name:
        database.add_book(book_name)
        flash(f"Book '{book_name}' created successfully!")
        return redirect(url_for('tracker', book_name=book_name))
    else:
        flash("Book name cannot be empty.")
        return redirect(request.referrer or url_for('home'))


@app.route("/delete_book/<book_name>", methods=["POST"])
@login_required
def delete_book_route(book_name):
    book_to_delete = database.get_book_by_name(book_name)
    if book_to_delete:
        # Prevent deletion of the last book
        all_books = database.get_books()
        if len(all_books) <= 1:
            flash("You cannot delete the last book.")
            return redirect(url_for('tracker', book_name=book_name))

        database.delete_book(book_to_delete['id'])
        flash(f"Book '{book_name}' and all its transactions have been deleted.")
    else:
        flash(f"Book '{book_name}' not found.")

    return redirect(url_for('home'))


@app.route("/edit/<book_name>/<tran_type>/<item_id>", methods=["GET", "POST"])
@login_required
def edit(book_name, tran_type, item_id):
    item = database.get_single_transaction(tran_type, item_id)
    if not item:
        flash("Record not found!")
        return redirect(url_for('tracker', book_name=book_name))

    if request.method == "POST":
        action = request.form.get('action')
        if action == "save":
            data = unpack_data(request.form)
            database.update_transaction(tran_type, item_id, data)
        return redirect(url_for("tracker", book_name=book_name))

    return render_template("edit.html", item=item, tran_type=tran_type, book_name=book_name)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)