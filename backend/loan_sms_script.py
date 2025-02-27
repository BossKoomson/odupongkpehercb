import sqlite3
import requests
import logging
from datetime import datetime
from tabulate import tabulate

# Initialize logging
logging.basicConfig(filename='loan_sms.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    conn = sqlite3.connect("loans.db")
    print("Connected to the database successfully.")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        total_amount REAL NOT NULL,
        amount_paid REAL NOT NULL,
        balance REAL NOT NULL,
        duration_left TEXT NOT NULL
    )''')
    print("'loans' table created or already exists.")
    conn.commit()
    conn.close()


# Add or update customer loan information
def update_customer_info():
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()

    name = input("Enter customer's name: ")
    phone = input("Enter customer's phone number: ")
    total_amount = float(input("Enter total loan amount: "))
    amount_paid = float(input("Enter amount paid: "))
    balance = total_amount - amount_paid
    duration_left = input("Enter duration left (e.g., 3 months): ")

    cursor.execute("INSERT INTO loans (name, phone, total_amount, amount_paid, balance, duration_left) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, phone, total_amount, amount_paid, balance, duration_left))
    conn.commit()
    conn.close()
    print("Customer information updated successfully.")

# Fetch customers from the database
def fetch_customers():
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loans")
    customers = cursor.fetchall()
    conn.close()
    return customers

# Send SMS to customers
def send_sms_to_customers():
    customers = fetch_customers()

    if not customers:
        print("No customers in the database.")
        return

    for customer in customers:
        message = (f"Hi {customer[1]},\n\n"
                   f"Your remaining balance is {customer[5]} GHS, out of a total loan amount of {customer[3]} GHS.\n"
                   f"You have {customer[6]} left to complete your payment.\n\n"
                   "Thank you for banking with us.\nOdupong-RB PLC.")
        
        send_sms(customer[2], message)
        print(f"Message sent to {customer[1]}.")

# Function to send SMS
def send_sms(phone, message):
    url = "https://alerts.ebitsgh.com/sms/api"
    params = {
        "action": "send-sms",
        "api_key": "WWxCRUNtYm1WeGpzendvaW5CS0M",  # Replace with your actual API key
        "to": phone,
        "from": "Odupong RBL",
        "sms": message
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get('code') == 'ok':
            logging.info(f"SMS sent to {phone}.")
        else:
            logging.error(f"Failed to send SMS to {phone}: {response_json}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending SMS to {phone}: {e}")

# Main function
def main():
    initialize_database()
    print("1. Update customer loan info")
    print("2. Send SMS to customers")
    
    choice = input("Select an option (1 or 2): ")
    
    if choice == "1":
        update_customer_info()
    elif choice == "2":
        send_sms_to_customers()
    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
