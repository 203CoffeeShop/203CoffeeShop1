from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

con = sqlite3.connect('orders1.db', check_same_thread=False)
cursor = con.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        coffee_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL)
''')

con.commit()

menu = [
    {'id': 1, 'name': 'Espresso', 'price': 2.5},
    {'id': 2, 'name': 'Cappuccino', 'price': 3.0},
    {'id': 3, 'name': 'Latte', 'price': 3.5},
    {'id': 4, 'name': 'Mocha', 'price': 4.0},
    {'id': 5, 'name': 'Americano', 'price': 3.0},
]

@app.route('/')
def home():
    return render_template('index.html', menu=menu)

@app.route('/order', methods=['POST'])
def order():
    order_id = int(request.form['coffee_id'])
    quantity = int(request.form['quantity'])
    coffee = next((item for item in menu if item['id'] == order_id), None)

    if coffee:
        total_price = coffee['price'] * quantity
        cursor.execute("INSERT INTO orders (coffee_name, quantity, total_price) VALUES (?,?,?)", (coffee['name'], quantity, total_price))
        con.commit()

        return render_template('orderpage.html', coffee=coffee, quantity=quantity, total_price=total_price)
    return 'Invalid order'

@app.route('/confirm', methods=['POST'])
def confirm():
    return 'Order confirmed'

if __name__ == '__main__':
    app.run(debug=True)