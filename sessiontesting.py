from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Global variable to simulate session-like data
session_data = {'counter': 0}

def background_task():
    global session_data
    while True:
        # Update the session-like data
        session_data['counter'] += 1
        time.sleep(1)

# Start the background task in a separate thread
thread = threading.Thread(target=background_task)
thread.start()

@app.route('/')
def testing():
    return render_template('testing.html', session_data=session_data)

@app.route('/get_data')
def get_data():
    global session_data
    return jsonify(session_data)


if __name__ == '__main__':
    app.run(debug=True)
