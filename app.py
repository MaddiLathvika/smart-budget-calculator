from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # income or expense
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Create DB
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    transactions = Transaction.query.all()

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return render_template(
        'index.html',
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        t_type = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])

        new_transaction = Transaction(
            type=t_type,
            category=category,
            amount=amount
        )

        db.session.add(new_transaction)
        db.session.commit()

        return redirect('/')

    return render_template('add_transaction.html')


@app.route('/delete/<int:id>')
def delete(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect('/')


@app.route('/report')
def report():
    transactions = Transaction.query.all()

    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expense = sum(t.amount for t in transactions if t.type == 'expense')
    balance = total_income - total_expense

    return render_template(
        'report.html',
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run()