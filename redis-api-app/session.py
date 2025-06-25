### redis-api-app/session.py
from flask import session

def login_user(user_id):
    session['user'] = user_id

def is_logged_in():
    return 'user' in session

def logout_user():
    session.pop('user', None)
