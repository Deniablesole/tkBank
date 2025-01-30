import tkinter as tk
from tkinter import messagebox
import sqlite3

#database setup
def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
    """)
    conn.commit()
    conn.close()


#GUI Functionality
class BankingApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Banking App")
            self.root.geometry("400x400")

            #Account creation
            self.name_label = tk.Label(root, text="Name:")
            self.name_label.pack(pady=5)
            self.name_entry = tk.Entry(root)
            self.name_entry.pack(pady=5)

            self.create_account_btn = tk.Button(root, text="Create Account", command=self.create_account)
            self.create_account_btn.pack(pady=10)

            #Account actions
            self.deposit_label = tk.Label(root, text="Deposit/Withdraw Amount:")
            self.deposit_label.pack(pady=5)
            self.amount_entry = tk.Entry(root)
            self.amount_entry.pack(pady=5)

            self.deposit_btn = tk.Button(root, text="Deposit", command=self.deposit)
            self.deposit_btn.pack(pady=5)

            self.withdraw_btn= tk.Button(root, text="Withdraw", command=self.withdraw)
            self.withdraw_btn.pack(pady=5)

            #Balance check
            self.balance_btn = tk.Button(root, text="Check Balance", command=self.check_balance)
            self.balance_btn.pack(pady=10)

            #Message display
            self.message_label = tk.Label(root, text="", fg="green")
            self.message_label.pack(pady=10)

            #Create account function
        def create_account(self):
                name = self.name_entry.get()
                if not name:
                    messagebox.showerror("Error", "Name cannot be empty.")
                    return
                
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0.0))
                conn.commit()
                conn.close()
                self.message_label.config(text=f"Account created for {name}!")

                #Deposit function
        def deposit(self):
                try:
                    amount = float(self.amount_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid ammount.")
                    return
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE name = ?", (self.name_entry.get(),))
                result = cursor.fetchone()

                if result:
                    new_balance = result[0] + amount
                    cursor.execute("UPDATE accounts SET balance = ? WHERE name = ?", (new_balance, self.name_entry.get()))
                    conn.commit()
                    self.message_label.config(text=f"Deposited ${amount:.2f}")
                else:
                    messagebox.showerror("Error", "Account not found.")
                conn.close()

            #Withdraw function
        def withdraw(self):
                try:
                    amount = float(self.amount_entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount.")
                    return
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("SELECT balance FROM accounts WHERE name = ?", (self.name_entry.get(),))
                result = cursor.fetchone()

                if result:
                    if result[0] >= amount:
                        new_balance = result[0] - amount
                        cursor.execute("UPDATE accounts SET balance = ? WHERE name = ?", (new_balance, self.name_entry.get()))
                        conn.commit()
                        self.message_label.config(text=f"Withdrew ${amount:.2f}")
                    else:
                        messagebox.showerror("Error", "Insufficient funds.")
                else:
                    messagebox.showerror("Error", "Account not found.")
                conn.close()

        def check_balance(self):
             conn = sqlite3.connect("database.db")
             cursor = conn.cursor()
             cursor.execute("SELECT balance FROM accounts WHERE name = ?", (self.name_entry.get(),))
             result = cursor.fetchone()

             if result:
                  self.message_label.config(text=f"Balance: ${result[0]:.2f}")
             else:
                  messagebox.showerror("Error", "Account not found.")

             conn.close()
#Main execution
if __name__ == "__main__":
     setup_database()
     root = tk.Tk()
     app = BankingApp(root)
     root.mainloop()

