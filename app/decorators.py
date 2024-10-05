from flask import session
from flask import url_for
from flask import redirect
import functools

import functools

def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        print("#"*50)
        print(f"DEBUG: Called {func.__name__}()")
        print(f"Arguments: args={args}, kwargs={kwargs}")
        print(f"Return Value: {result}")
        print("#"*50)

        return result  # Return the result of the function
    return wrapper

def login_required(f):
    def wrapper(*args, **kwargs):
        # Check if user_id is in session
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))  # Redirect to login if not logged in
        return f(*args, **kwargs)  # Proceed to the view function
    wrapper.__name__ = f.__name__  # Preserve the function name
    return wrapper

def role_required(required_role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Check if user is logged in and has the required role
            if 'user_id' not in session or session.get('role_id') != required_role:
                return redirect(url_for('auth.login'))  # Redirect if not authorized
            return f(*args, **kwargs)  # Proceed to the view function
        wrapper.__name__ = f.__name__  # Preserve the function name
        return wrapper
    return decorator
