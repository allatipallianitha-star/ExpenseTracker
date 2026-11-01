import sqlite3
def create_database():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Income', 'Expense')), category TEXT NOT NULL, amount REAL NOT NULL CHECK(amount > 0), description TEXT, transaction_date TEXT NOT NULL)""")
    connection.commit()
    connection.close()
    print("Database created successfully!")
if __name__ == "__main__":
    create_database()