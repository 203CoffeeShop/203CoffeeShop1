import sqlite3 as sql

def insertUser(username, password):
    try:
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        con.commit()
    except Exception as e:
        print("An error occurred:", e)
    finally:
        con.close()

def retrieveUsers():
    try:
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("SELECT username, password FROM users")
        users = cur.fetchall()
        return users
    except Exception as e:
        print("An error occurred:", e)
    finally:
        con.close()

# Test the functions
insertUser("test_user", "test_password")
print(retrieveUsers())
