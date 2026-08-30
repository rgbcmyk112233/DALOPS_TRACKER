from flask import session
import app
import random

def dummy_auth(username, password):

    if username == "admin" and password == "admin":
        return True
    else:
        return False
