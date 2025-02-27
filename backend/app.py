from flask import Flask, request, jsonify
import loan_sms_script  # Assuming the script is in the same directory

app = Flask(__name__)

# Adjusted update_customer_info in loan_sms_script to take arguments
def update_customer_info(data):
    import sqlite3

    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()

    name = data["name"]
    phone = data["phone"]
    total_amount = float(data["total_amount"])
    amount_paid = float(data["amount_paid"])
    balance = total_amount - amount_paid
    duration_left = data["duration_left"]

    cursor.execute("INSERT INTO loans (name, phone, total_amount, amount_paid, balance, duration_left) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, phone, total_amount, amount_paid, balance, duration_left))
    conn.commit()
    conn.close()
    print("Customer information updated successfully.")

@app.route("/update_customer", methods=["POST"])
def update_customer():
    try:
        data = request.json
        update_customer_info(data)
        return jsonify({"message": "Customer info updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send_sms", methods=["POST"])
def send_sms():
    try:
        loan_sms_script.send_sms_to_customers()
        return jsonify({"message": "SMS sent to all customers."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
