import sqlite3
from database import create_database
from datetime import datetime
def add_transactions():
    transactions_type = input("Enter type (Income/Expense):").strip().capitalize()
    if transactions_type not in ("Income", "Expense"):
        print("Invalid type! Enter Income or Expense.")
        return
    category = input("Enter category:").strip()
    if not category:
        print("Category cannot be empty.")
        return
    try:
        amount = float(input("Enter amount:"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("please enter a valid number.")
        return
    description = input("Enter description:").strip()
    transaction_data = input("Enter date (YYYY-MM-DD):").strip()
    try:
        datetime.strptime(transaction_data, "%Y-%m-%d")
    except ValueError:
        print("Invalid date! Use YYYY-MM-DD format.")
        return
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO transactions (transaction_type, category, amount, description, transaction_date) VALUES (?, ?, ?, ?, ?)""", (transactions_type, category, amount, description, transaction_data))
        connection.commit()
        print("Transaction added successfully!")
    except sqlite3.Error as error:
        print("Database error:", error)
    finally:
        connection.close()
def view_transactions():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM transactions ORDER BY transaction_id DESC""")
    transactions = cursor.fetchall()
    connection.close()
    if not transactions:
        print("No transactions found.")
        return
    print("\n===== ALL TRANSACTIONS =====")
    for transaction in transactions:
        print("-" * 40)
        print("ID:", transaction[0])
        print("Type:", transaction[1])
        print("Category:", transaction[2])
        print("Amount:", transaction[3])
        print("Description:", transaction[4])
        print("Date:", transaction[5])
def show_summary():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT COALESCE(SUM(CASE WHEN transaction_type = 'Income' THEN amount ELSE 0 END), 0), COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) FROM transactions""")
    total_income, total_expenses = cursor.fetchone()
    connection.close()
    balance = total_income - total_expenses
    print("\n===== FINANCIAL SUMMARY =====")
    print(f"Total Income: RS.{total_income:.2f}")
    print(f"Total Expenses: RS.{total_expenses:.2f}")
    print(f"Current Balance: RS.{balance:.2f}")
def search_transactions():
    try:
        transaction_id = int(input("Enter transaction ID:"))
    except ValueError:
        print("please enter a valid transaction ID.")
        return
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
    transaction = cursor.fetchone()
    connection.close()
    if transaction:
        print("\nTransaction found:")
        print("ID:", transaction[0])
        print("Type:", transaction[1])
        print("Category:", transaction[2])
        print("Amount:", transaction[3])
        print("Description:", transaction[4])
        print("Date:", transaction[5])
    else:
        print("No transaction found.")
def update_transactions():
    try:
        transaction_id = int(input("Enter transaction ID:"))
    except ValueError:
        print("Please enter a valid ID.")
        return
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
    transaction = cursor.fetchone()
    if not transaction:
        print("No transaction found.")
        connection.close()
        return
    transaction_type = input("Enter new type (Income/Expense):").strip().capitalize()
    if transaction_type not in ("Income", "Expense"):
        print("invalid transaction type.")
        connection.close()
        return
    category = input("Enter new category:").strip()
    if not category:
        print("Category cannot be empty.")
        connection.close()
        return
    try:
        amount = float(input("Enter new amount:"))
        if amount <= 0:
            print("Amount must be greater than zero.")
            connection.close()
            return
    except ValueError:
        print("Invalid amount.")
        connection.close()
        return
    description = input("Enter new description:").strip()
    try:
        transaction_date = input("Enter new date (YYYY-MM-DD):").strip()
        datetime.strptime(transaction_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date! Use YYYY-MM-DD format.")
        connection.close()
        return
    cursor.execute("""UPDATE transactions SET transaction_type = ?, category = ?, amount = ?, description = ?, transaction_date = ? WHERE transaction_id = ?""", (transaction_type, category, amount, description, transaction_date, transaction_id))
    connection.commit()
    connection.close()
    print("Transaction updated successfully.")
def delete_transactions():
    try:
        transaction_id = int(input("Enter transaction ID:"))
    except ValueError:
        print("Please enter a valid ID.")
        return
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM transactions WHERE transaction_id = ?", (transaction_id,))
    transaction = cursor.fetchone()
    if transaction:
        confirm = input("Are you sure you want to delete? (yes/no):").strip().lower()
        if confirm == "yes":
            cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
            connection.commit()
            print("Transaction deleted successfully.")
        else:
            print("Delete cancelled.")
    else:
        print("No transaction found.")
    connection.close()
def main():
    create_database()
    while True:
        print("\n===== Expense Tracker =====")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Show Financial Summary")
        print("4. Search Transactions")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. Exit")
        choice = input("Select an option (1-7):").strip()
        if choice == "1":
            add_transactions()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            search_transactions()
        elif choice == "5":
            update_transactions()
        elif choice == "6":
            delete_transactions()
        elif choice == "7":
            print("Thank you for using Expense tracker!")
            break
        else:
            print("Please select 1-7.")
if __name__ == "__main__":
    main()
