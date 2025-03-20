import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

class ATM:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ATM System")
        self.window.geometry("400x600")
        self.window.configure(bg="#f0f0f0")
        
        # Initialize account data
        self.current_user = None
        self.load_accounts()
        
        # Create main frames
        self.create_welcome_frame()
        self.create_login_frame()
        self.create_main_menu_frame()
        self.create_transaction_frame()
        
        # Show welcome frame initially
        self.show_frame(self.welcome_frame)
        
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
    
    def create_welcome_frame(self):
        self.welcome_frame = tk.Frame(self.window, bg="#f0f0f0")
        
        welcome_label = tk.Label(
            self.welcome_frame,
            text="Welcome to ATM",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        welcome_label.pack(pady=50)
        
        start_button = tk.Button(
            self.welcome_frame,
            text="Start",
            command=lambda: self.show_frame(self.login_frame),
            font=("Arial", 14),
            width=20,
            height=2
        )
        start_button.pack(pady=20)
    
    def create_login_frame(self):
        self.login_frame = tk.Frame(self.window, bg="#f0f0f0")
        
        tk.Label(
            self.login_frame,
            text="Account Number",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        self.account_entry = tk.Entry(self.login_frame, font=("Arial", 12))
        self.account_entry.pack(pady=5)
        
        tk.Label(
            self.login_frame,
            text="PIN",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        self.pin_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 12))
        self.pin_entry.pack(pady=5)
        
        login_button = tk.Button(
            self.login_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12),
            width=15,
            height=1
        )
        login_button.pack(pady=20)
        
        back_button = tk.Button(
            self.login_frame,
            text="Back",
            command=lambda: self.show_frame(self.welcome_frame),
            font=("Arial", 12),
            width=15,
            height=1
        )
        back_button.pack(pady=10)
    
    def create_main_menu_frame(self):
        self.main_menu_frame = tk.Frame(self.window, bg="#f0f0f0")
        
        menu_label = tk.Label(
            self.main_menu_frame,
            text="Main Menu",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0"
        )
        menu_label.pack(pady=20)
        
        buttons = [
            ("Check Balance", self.show_balance),
            ("Withdraw", lambda: self.show_frame(self.transaction_frame)),
            ("Deposit", lambda: self.show_frame(self.transaction_frame)),
            ("Transaction History", self.show_transaction_history),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            tk.Button(
                self.main_menu_frame,
                text=text,
                command=command,
                font=("Arial", 12),
                width=20,
                height=2
            ).pack(pady=10)
    
    def create_transaction_frame(self):
        self.transaction_frame = tk.Frame(self.window, bg="#f0f0f0")
        
        tk.Label(
            self.transaction_frame,
            text="Amount",
            font=("Arial", 12),
            bg="#f0f0f0"
        ).pack(pady=10)
        
        self.amount_entry = tk.Entry(self.transaction_frame, font=("Arial", 12))
        self.amount_entry.pack(pady=5)
        
        withdraw_button = tk.Button(
            self.transaction_frame,
            text="Withdraw",
            command=self.withdraw,
            font=("Arial", 12),
            width=15,
            height=1
        )
        withdraw_button.pack(pady=10)
        
        deposit_button = tk.Button(
            self.transaction_frame,
            text="Deposit",
            command=self.deposit,
            font=("Arial", 12),
            width=15,
            height=1
        )
        deposit_button.pack(pady=10)
        
        back_button = tk.Button(
            self.transaction_frame,
            text="Back to Main Menu",
            command=lambda: self.show_frame(self.main_menu_frame),
            font=("Arial", 12),
            width=15,
            height=1
        )
        back_button.pack(pady=10)
    
    def show_frame(self, frame):
        for f in [self.welcome_frame, self.login_frame, self.main_menu_frame, self.transaction_frame]:
            f.pack_forget()
        frame.pack()
    
    def login(self):
        account = self.account_entry.get()
        pin = self.pin_entry.get()
        
        if account in self.accounts and self.accounts[account]["pin"] == pin:
            self.current_user = account
            self.show_frame(self.main_menu_frame)
        else:
            messagebox.showerror("Error", "Invalid account number or PIN")
    
    def logout(self):
        self.current_user = None
        self.show_frame(self.welcome_frame)
    
    def show_balance(self):
        balance = self.accounts[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Current Balance: ${balance:.2f}")
    
    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            if amount > self.accounts[self.current_user]["balance"]:
                messagebox.showerror("Error", "Insufficient funds")
                return
                
            self.accounts[self.current_user]["balance"] -= amount
            self.add_transaction("Withdraw", amount)
            self.save_accounts()
            
            messagebox.showinfo("Success", f"Withdrawn ${amount:.2f}")
            self.amount_entry.delete(0, tk.END)
            self.show_frame(self.main_menu_frame)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
                
            self.accounts[self.current_user]["balance"] += amount
            self.add_transaction("Deposit", amount)
            self.save_accounts()
            
            messagebox.showinfo("Success", f"Deposited ${amount:.2f}")
            self.amount_entry.delete(0, tk.END)
            self.show_frame(self.main_menu_frame)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
    
    def add_transaction(self, type_, amount):
        transaction = {
            "type": type_,
            "amount": amount,
            "balance": self.accounts[self.current_user]["balance"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.accounts[self.current_user]["transactions"].append(transaction)
    
    def show_transaction_history(self):
        transactions = self.accounts[self.current_user]["transactions"]
        if not transactions:
            messagebox.showinfo("Transaction History", "No transactions found")
            return
            
        history = "Transaction History:\n\n"
        for t in transactions:
            history += f"Type: {t['type']}\n"
            history += f"Amount: ${t['amount']:.2f}\n"
            history += f"Balance: ${t['balance']:.2f}\n"
            history += f"Date: {t['date']}\n"
            history += "-" * 30 + "\n"
            
        messagebox.showinfo("Transaction History", history)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    atm = ATM()
    atm.run()
