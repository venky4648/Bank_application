from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited {amount}")
            return {"success": True, "message": f"Deposited {amount}. New balance: {self.balance}"}
        else:
            return {"success": False, "message": "Deposit amount must be greater than 0"}

    def withdraw(self, amount):
        if amount > self.balance:
            return {"success": False, "message": "Insufficient balance"}
        elif amount <= 0:
            return {"success": False, "message": "Withdrawal amount must be greater than 0"}
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew {amount}")
            return {"success": True, "message": f"Withdrew {amount}. New balance: {self.balance}"}

    def check_balance(self):
        return {"balance": self.balance}

    def view_transaction_history(self):
        return {"transactions": self.transaction_history}

# Create a global account object
account = BankAccount("John Doe")

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.json
    amount = float(data.get('amount'))
    response = account.deposit(amount)
    return jsonify(response)

@app.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    amount = float(data.get('amount'))
    response = account.withdraw(amount)
    return jsonify(response)

@app.route('/balance', methods=['GET'])
def balance():
    response = account.check_balance()
    return jsonify(response)

@app.route('/transactions', methods=['GET'])
def transactions():
    response = account.view_transaction_history()
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
