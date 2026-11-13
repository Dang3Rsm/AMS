import functools
from flask import session, url_for, redirect, flash

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

def role_required(required_role):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session or session.get('role_id') != required_role:
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator