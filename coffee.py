from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
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
    CREATE TABLE IF NOT EXISTS neworders (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        coffee_name TEXT NOT NULL,
        amount INTEGER NOT NULL,
        total_cost REAL NOT NULL)
''')

con.commit()

#List which contains all the drink which can be purchased
menu = [
    {'ID': 1, 'name': 'Flat White', 'price': 5, 'popular': True},
    {'ID': 2, 'name': 'Cappuccino', 'price': 5, 'popular': True},
    {'ID': 3, 'name': 'Cafe Latte', 'price': 5.5, 'popular': True},
    {'ID': 4, 'name': 'Vanilla Latte', 'price': 6.5, 'popular': True},
    {'ID': 5, 'name': 'Caramel Latte', 'price':6.5, 'popular': True},
    {'ID': 6, 'name': 'Long Black', 'price': 4, 'popular': False},
    {'ID': 7, 'name': 'Short Black', 'price': 4, 'popular': False},
    {'ID': 8, 'name': 'Americano', 'price': 4, 'popular': False},
    {'ID': 9, 'name': 'Macchiato', 'price': 4.5, 'popular': False},
    {'ID': 10, 'name': 'Piccolo Latte', 'price': 4.5, 'popular': False},
    {'ID': 11, 'name': 'Caramel Affogato', 'price': 7.5, 'popular': False},
    {'ID': 12, 'name': 'Mocha', 'price': 6, 'popular': False},
    {'ID': 13, 'name': 'Hot Chocolate', 'price': 5.5, 'popular': False},
    {'ID': 14, 'name': 'White Hot Chocolate', 'price': 6.5, 'popular': False},
    {'ID': 15, 'name': 'White Chocolate Mocha', 'price': 6.8, 'popular': False},
    {'ID': 16, 'name': 'English Breakfast', 'price': 4.5, 'popular': False},
    {'ID': 17, 'name': 'Green Tea', 'price': 4.5, 'popular': False},
    {'ID': 18, 'name': 'Ginger Tea', 'price': 4.5, 'popular': False},
    {'ID': 19, 'name': 'Lemon Tea', 'price': 4.5, 'popular': False},
    {'ID': 20, 'name': 'Ice Coffee', 'price': 7, 'popular': False},
    {'ID': 21, 'name': 'Ice Chocolate', 'price': 7, 'popular': False},
    {'ID': 22, 'name': 'Ice Americano', 'price': 6, 'popular': False},
    {'ID': 23, 'name': 'Ice Latte', 'price': 7, 'popular': False}
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

#send the user to the homepage
@app.route('/home')
def home():
    return render_template('index.html', menu=menu)

@app.route('/drinks')
def drinks():
    return render_template('drinks.html', menu=menu)

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

@app.route('/check_session')
def check_session():
    if "username" in session:
        return jsonify({"satus": "active"})
    else:
        return jsonify({"satus": "expired"})

@app.route('/order', methods=['POST'])
def order():
    order_id = int(request.form['coffee_id'])
    amount = int(request.form['amount'])
    coffee = next((item for item in menu if item['ID'] == order_id), None)

    if coffee:
        total_cost = coffee['price'] * amount
        cursor.execute("INSERT INTO neworders (coffee_name, amount, total_cost) VALUES (?,?,?)", (coffee['name'], amount, total_cost))
        con.commit()

        return render_template('orderpage.html', coffee=coffee, amount=amount, total_cost=total_cost)
    return 'Invalid order'

@app.route('/confirm', methods=['POST'])
def confirm():
    return redirect('/home')


if __name__ == '__main__':
    add_user("admin", "password")
    app.secret_key = "app.secret_key"
    app.run(debug=True)