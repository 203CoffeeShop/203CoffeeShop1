from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, jsonify, flash,sessions
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import sqlite3, time

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = 3600
Session(app)

#Connects to the sqlite Database and creates a table for the 
#infomation needed if one doesn't exist with that name
con = sqlite3.connect('new_orders1.db', check_same_thread=False)
cursor = con.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orderList (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        coffee_name TEXT NOT NULL,
        cost REAL NOT NULL,
        amount INTEGER NOT NULL,
        total_cost REAL NOT NULL)
''')

con.commit()


#List which contains all the drink which can be purchased
menu = [
    {'ID': 1, 'name': 'Flat White', 'price': 5, 'popular': False, 'type': 'coffee', 'image': 'static/images/flat-white.jpg'},
    {'ID': 2, 'name': 'Cappuccino', 'price': 5, 'popular': True, 'type': 'coffee', 'image': 'static/images/cappucino.png'},
    {'ID': 3, 'name': 'Cafe Latte', 'price': 5.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/cafe-latte.jpg'},
    {'ID': 4, 'name': 'Vanilla Latte', 'price': 6.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/Vanilla_Latte.jpg'},
    {'ID': 5, 'name': 'Caramel Latte', 'price':6.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/Caramel-Latte.jpg'},
    {'ID': 6, 'name': 'Long Black', 'price': 4, 'popular': False, 'type': 'coffee', 'image': 'static/images/long-black.jpg'},
    {'ID': 7, 'name': 'Short Black', 'price': 4, 'popular': False, 'type': 'coffee', 'image': 'static/images/short-black.jpg'},
    {'ID': 8, 'name': 'Americano', 'price': 4, 'popular': False, 'type': 'coffee', 'image': 'static/images/americano.jpg'},
    {'ID': 9, 'name': 'Macchiato', 'price': 4.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/macchiato.png'},
    {'ID': 10, 'name': 'Piccolo Latte', 'price': 4.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/Piccolo-Latte.png'},
    {'ID': 11, 'name': 'Caramel Affogato', 'price': 7.5, 'popular': False, 'type': 'coffee', 'image': 'static/images/Caramel-Affogato.jpg'},
    {'ID': 12, 'name': 'Mocha', 'price': 6, 'popular': True, 'type': 'chocolate', 'image': 'static/images/mocha.png'},
    {'ID': 13, 'name': 'Hot Chocolate', 'price': 5.5, 'popular': False, 'type': 'chocolate', 'image': 'static/images/hot-chocolate.jpg'},
    {'ID': 14, 'name': 'White Hot Chocolate', 'price': 6.5, 'popular': False, 'type': 'chocolate', 'image': 'static/images/white-hot-chocolate.png'},
    {'ID': 15, 'name': 'White Chocolate Mocha', 'price': 6.8, 'popular': True, 'type': 'chocolate', 'image': 'static/images/White-Chocolate-Mocha.jpg'},
    {'ID': 16, 'name': 'English Breakfast', 'price': 4.5, 'popular': False, 'type': 'tea', 'image': 'static/images/english-tea.jpg'},
    {'ID': 17, 'name': 'Green Tea', 'price': 4.5, 'popular': True, 'type': 'tea', 'image': 'static/images/green-tea.png'},
    {'ID': 18, 'name': 'Ginger Tea', 'price': 4.5, 'popular': False, 'type': 'tea', 'image': 'static/images/ginger-tea.png'},
    {'ID': 19, 'name': 'Lemon Tea', 'price': 4.5, 'popular': False, 'type': 'tea', 'image': 'static/images/lemon-tea.png'},
    {'ID': 20, 'name': 'Ice Coffee', 'price': 7, 'popular': False, 'type': 'cold', 'image': 'static/images/iced-coffee.jpg'},
    {'ID': 21, 'name': 'Ice Chocolate', 'price': 7, 'popular': False, 'type': 'cold', 'image': 'static/images/iced-chocolate.jpg'},
    {'ID': 22, 'name': 'Ice Americano', 'price': 6, 'popular': False, 'type': 'cold', 'image': 'static/images/iced-americano.png'},
    {'ID': 23, 'name': 'Ice Latte', 'price': 7, 'popular': True, 'type': 'cold', 'image': 'static/images/iced-latte.jpg'}
]

#connects to the sqlite databse and creates a table for 
# user information if one already doesn't exist
con = sqlite3.connect('new_orders1.db', check_same_thread=False)
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
con.commit()

#Adds the users information into the database
def add_user(username, password):
    con = sqlite3.connect('new_orders1.db', check_same_thread=False)
    cursor = con.cursor()
    cursor.execute("INSERT or replace INTO users (username, password) VALUES (?,?)", (username, password))
    con.commit()

#Get's information and sends it to the add_user function
#also redirects the user to the proper page to make an account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        add_user(username, password)
        return redirect(url_for('login'))
    return render_template('create_account.html')

#Get's the name of the user from the database
def get_user(username):
    con = sqlite3.connect('new_orders1.db', check_same_thread=False)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    con.close()
    return user
#####################################################

@app.route('/base')
def base():
    return render_template('base.html')
@app.route('/index1')
def index1():
    return render_template('index1.html')
@app.route('/DrinkMenu')
def DrinkMenu():

    if 'cart' in session:
        orders = session['cart']
        total_cost = sum(order['total_cost'] for order in orders)
        return render_template('DrinkMenu.html', orders=orders, total_cost=total_cost, menu=menu)
    else:
        return render_template('DrinkMenu.html', menu=menu)
    

@app.route('/cart', methods=['POST'])
def cart():
    # Clear the existing cart session
    session['cart'] = []

    # Retrieve data from the form
    coffee_name = request.form.get('coffee_name')
    price = float(request.form.get('price'))
    amount = int(request.form.get('amount'))

    total_cost = price * amount

    # Save order details to session (cart)
    item = {
        'coffee_name': coffee_name,
        'price': price,
        'amount': amount,
        'total_cost': total_cost
    }

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(item)
    session.modified = True  # Ensure session is saved

    return jsonify()

@app.route('/cart_display')
def cart_display():
    if 'cart' in session:
        orders = session['cart']
        total_cost = sum(order['total_cost'] for order in orders)
        return render_template('cart.html', orders=orders, total_cost=total_cost)
    else:
        flash("Your cart is empty.", "info")
        return render_template('cart.html', orders=[], total_cost=0)
    
# @app.route('/place_order', methods=['POST'])
# def place_order():
#     con = sqlite3.connect('new_orders1.db', check_same_thread=False)
#     cursor = con.cursor()

#     cursor.execute("SELECT * FROM orderList")
#     orders_before_placing = cursor.fetchall()

#     # Optionally, you can perform additional processing or validation here

#     # Clear the cart after placing the order
#     cursor.execute("DELETE FROM orderList")
#     con.commit()

#     cursor.execute("SELECT * FROM orderList")
#     orders_after_placing = cursor.fetchall()

#     print("Orders before placing:", orders_before_placing)
#     print("Orders after placing:", orders_after_placing)

#     return render_template('order_confirmation.html', orders=orders_before_placing)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'cart' in session:
        orders_before_placing = session['cart']

        # Optionally, you can perform additional processing or validation here

        # Clear the cart after placing the order
        session.pop('cart', None)

        print("Orders before placing:", orders_before_placing)
        print("Cart after placing:", session.get('cart'))

        return render_template('order_confirmation.html', orders=orders_before_placing)
    else:
        flash("Your cart is empty.", "info")
        return render_template('order_confirmation.html', orders=[])


########################################
#send the user to the homepage
@app.route('/home')
def home():
    return render_template('index.html', menu=menu)

@app.route('/drinks', methods=['GET','POST'])
def drinks():
    if request.method == 'POST':
        session['cart'] = request.form['cart']
    return render_template('drinks.html', menu=menu)

@app.route('/orders', methods=['POST'])
def orders():
    return render_template('orderpage.html')

#The start page when you visit the website
#Takes information from the user and checks if it exists in the database, if so 
#the user is allowed to login 
#else it shows an error
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and user[1] == password:
            session["username"] = username
            session["last_active"] = time.time()
            return redirect('/home')
        else:
            flash("Invalid username or password", "error")
    return render_template('loginpage.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if request.method == 'POST':
        data = request.json
        print('Received data:', data)

        if 'cart' not in session:
            session['cart'] = []

        # Add the item to the cart
        item = {
            'coffee_name': data.get('coffee_name'),
            'price': float(data.get('price')),
            'amount': int(data.get('amount')),
            'total_cost': float(data.get('price')) * int(data.get('amount'))
        }

        session['cart'].append(item)
        session.modified = True  # Ensure session is saved

        return jsonify()
    
@app.route('/check_session')
def check_session():
    if "username" in session:
        return jsonify({"satus": "active"})
    else:
        return jsonify({"satus": "expired"})

#Redirects the user to the settings page
@app.route('/settings')
def settings():
    return render_template('settingspage.html')

if __name__ == '__main__':
    add_user("admin", "password")
    app.secret_key = "app.secret_key"
    app.run(debug=True)