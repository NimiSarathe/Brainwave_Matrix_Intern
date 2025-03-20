from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class ATM:
    def __init__(self):
        self.accounts = {}
        self.load_accounts()
    
    def load_accounts(self):
        if os.path.exists("accounts.json"):
            with open("accounts.json", "r") as f:
                self.accounts = json.load(f)
        else:
            self.accounts = {
                "1234": {"pin": "1234", "balance": 1000.0, "transactions": []}
            }
            self.save_accounts()
    
    def save_accounts(self):
        with open("accounts.json", "w") as f:
            json.dump(self.accounts, f)
    
    def add_transaction(self, account, type_, amount):
        transaction = {
            "type": type_,
            "amount": amount,
            "balance": self.accounts[account]["balance"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.accounts[account]["transactions"].append(transaction)
        self.save_accounts()

atm = ATM()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        account = request.form.get('account')
        pin = request.form.get('pin')
        
        if account in atm.accounts and atm.accounts[account]["pin"] == pin:
            session['account'] = account
            return redirect(url_for('main_menu'))
        else:
            flash('Invalid account number or PIN', 'error')
    
    return render_template('login.html')

@app.route('/main_menu')
def main_menu():
    if 'account' not in session:
        return redirect(url_for('login'))
    return render_template('main_menu.html')

@app.route('/balance')
def check_balance():
    if 'account' not in session:
        return redirect(url_for('login'))
    
    account = session['account']
    balance = atm.accounts[account]["balance"]
    return render_template('balance.html', balance=balance)

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'account' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        account = session['account']
        amount = float(request.form.get('amount', 0))
        transaction_type = request.form.get('type')
        
        if amount <= 0:
            flash('Amount must be positive', 'error')
            return redirect(url_for('transaction'))
        
        if transaction_type == 'withdraw':
            if amount > atm.accounts[account]["balance"]:
                flash('Insufficient funds', 'error')
                return redirect(url_for('transaction'))
            atm.accounts[account]["balance"] -= amount
            atm.add_transaction(account, "Withdraw", amount)
            flash(f'Successfully withdrawn ${amount:.2f}', 'success')
        else:  # deposit
            atm.accounts[account]["balance"] += amount
            atm.add_transaction(account, "Deposit", amount)
            flash(f'Successfully deposited ${amount:.2f}', 'success')
        
        atm.save_accounts()
        return redirect(url_for('main_menu'))
    
    return render_template('transaction.html')

@app.route('/history')
def transaction_history():
    if 'account' not in session:
        return redirect(url_for('login'))
    
    account = session['account']
    transactions = atm.accounts[account]["transactions"]
    return render_template('history.html', transactions=transactions)

@app.route('/logout')
def logout():
    session.pop('account', None)
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)