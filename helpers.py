from functools import wraps
from flask import g, request, redirect, url_for, session


def login_required(f):
    # Use Flask login_required function decorator from documentation    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None: 
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function