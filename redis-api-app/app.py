### redis-api-app/app.py
from flask import Flask, request, jsonify, session
from cache import get_cached_data, set_cache,redis_client
from session import login_user, logout_user, is_logged_in
from tasks import send_email
from flask_session import Session
import time

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis_client 
# app.config['SESSION_REDIS'] = get_cached_data().redis_client

Session(app)

@app.route('/')
def home():
    return "Welcome to Flask + Redis API!"

@app.route('/login', methods=['POST'])
def login():
    user = request.json.get('user')
    login_user(user)
    return jsonify({"message": f"Logged in as {user}"})

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

@app.route('/check-session')
def check_session():
    if is_logged_in():
        return jsonify({"session": session['user']})
    return jsonify({"error": "Not logged in"}), 401

@app.route('/slow-data')
def slow_data():
    cached = get_cached_data("heavy_data")
    if cached:
        return jsonify({"data": cached.decode(), "source": "cache"})

    time.sleep(3)
    result = "Heavy Data Result"
    set_cache("heavy_data", result, timeout=60)
    return jsonify({"data": result, "source": "generated"})

@app.route('/send-email')
def send():
    email = request.args.get("email")
    send_email.delay(email)
    return jsonify({"message": f"Email will be sent to {email}"})

if __name__ == '__main__':
    app.run(debug=True)