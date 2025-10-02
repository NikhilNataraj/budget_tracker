import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import date, timedelta, datetime

from helper import get_total, unpack_data
import db as database

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)


class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password = password_hash


@login_manager.user_loader
def load_user(user_id):
    user_data = database.get_user_by_id(user_id)
    if user_data:
        return User(id=user_data['id'], email=user_data['email'], password_hash=user_data['password_hash'])
    return None


@app.route("/")
@login_required
def home():
    user_books = database.get_books(current_user.id)
    if user_books:
        return redirect(url_for("tracker", book_name=user_books[0]['name']))
    return redirect(url_for("tracker", book_name="Default"))


# Login and Register routes remain the same
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = database.get_user_by_email(email)
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(id=user_data['id'], email=user_data['email'], password_hash=user_data['password_hash'])
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if database.get_user_by_email(email):
            flash("An account with this email already exists.")
            return redirect(url_for('register'))
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        user_id = database.add_user(email, password_hash)
        database.add_book("My First Book", user_id)
        new_user = User(id=user_id, email=email, password_hash=password_hash)
        login_user(new_user)
        flash("Account created successfully!")
        return redirect(url_for('home'))
    return render_template("register.html")


@app.route("/tracker/<book_name>", methods=["GET", "POST"])
@login_required
def tracker(book_name):
    all_books = database.get_books(current_user.id)
    current_book = database.get_book_by_name(book_name, current_user.id)

    if not all_books and book_name == "Default":
        return render_template("index.html", books=None, current_book=None, logged_in=True)

    if not current_book:
        flash(f"Book '{book_name}' not found!")
        return redirect(url_for('home'))

    # --- FILTER LOGIC ---
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Default to current month if no dates are provided
    if not start_date or not end_date:
        today = date.today()
        start_date = today.replace(day=1).strftime('%Y-%m-%d')
        # Find the last day of the month
        next_month = today.replace(day=28) + timedelta(days=4)
        end_of_month = next_month - timedelta(days=next_month.day)
        end_date = end_of_month.strftime('%Y-%m-%d')

    if request.method == 'POST':
        # Transaction handling logic remains the same
        action = request.form.get('action')
        item_id = request.form.get('item_id')
        if action in ['income', 'expense']:
            data = unpack_data(request.form)
            database.add_transaction(action, data, current_book['id'])
        elif action in ['edit_income', 'edit_expense']:
            return redirect(url_for('edit', book_name=book_name, tran_type=action.split('_')[1], item_id=item_id))
        elif action in ['delete_income', 'delete_expense']:
            database.delete_transaction(action.split('_')[1], item_id)
        # Redirect to preserve the filter in the URL
        return redirect(url_for('tracker', book_name=book_name, start_date=start_date, end_date=end_date))

    # Fetch transactions using the filter dates
    income_data = database.get_transactions("income", current_book['id'], start_date, end_date)
    expense_data = database.get_transactions("expense", current_book['id'], start_date, end_date)

    total_income = get_total(income_data)
    total_expenses = get_total(expense_data)
    total_exp_percent = round(total_expenses / total_income * 100) if total_income > 0 else 0

    # Update the display title based on the filter
    try:
        start_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_obj = datetime.strptime(end_date, '%Y-%m-%d')
        if start_obj.month == end_obj.month and start_obj.year == end_obj.year:
            display_period = start_obj.strftime("%B %Y")
        else:
            display_period = f"{start_obj.strftime('%b %d, %Y')} - {end_obj.strftime('%b %d, %Y')}"
    except ValueError:
        display_period = "Selected Period"

    return render_template("index.html",
                           income=income_data, expense=expense_data,
                           total_income=total_income, total_expenses=total_expenses,
                           total_exp_percent=total_exp_percent,
                           books=all_books, current_book=current_book, logged_in=True,
                           start_date=start_date, end_date=end_date,  # Pass dates to template
                           display_period=display_period)  # Pass formatted period to template


# All other routes (add_book, delete_book_route, edit, logout) remain the same
@app.route("/add_book", methods=["POST"])
@login_required
def add_book():
    book_name = request.form.get("book_name")
    if book_name:
        database.add_book(book_name, current_user.id)
        flash(f"Book '{book_name}' created successfully!")
        return redirect(url_for('tracker', book_name=book_name))
    else:
        flash("Book name cannot be empty.")
        return redirect(request.referrer or url_for('home'))


@app.route("/delete_book/<book_name>", methods=["POST"])
@login_required
def delete_book_route(book_name):
    book_to_delete = database.get_book_by_name(book_name, current_user.id)
    if book_to_delete:
        all_books = database.get_books(current_user.id)
        if len(all_books) <= 1:
            flash("You cannot delete your last book.")
            return redirect(url_for('tracker', book_name=book_name))
        database.delete_book(book_to_delete['id'], current_user.id)
        flash(f"Book '{book_name}' and all its transactions have been deleted.")
    else:
        flash(f"Book '{book_name}' not found.")
    return redirect(url_for('home'))


@app.route("/edit/<book_name>/<tran_type>/<item_id>", methods=["GET", "POST"])
@login_required
def edit(book_name, tran_type, item_id):
    item = database.get_single_transaction(tran_type, item_id)
    if item:
        book = database.get_books(current_user.id)
        book_ids = [b['id'] for b in book]
        if item['book_id'] not in book_ids:
            flash("Unauthorized access to transaction.")
            return redirect(url_for('home'))
    if not item:
        flash("Record not found!")
        return redirect(url_for('tracker', book_name=book_name))
    if request.method == "POST":
        if request.form.get('action') == "save":
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