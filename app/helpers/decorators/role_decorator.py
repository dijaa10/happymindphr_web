from flask_login import current_user
from flask import flash,request,redirect
from functools import wraps
def must_super_admin(f):
    """
    Decorator to restrict access to a view function to only users 
    whose role is "super_admin".
    
    If the current user is not a "super_admin":
    1. A flash message is shown to the user.
    2. The user is redirected back to the previous page (request.referrer).

    Requires 'current_user' (with a 'role' attribute), 'flash', 'redirect', 
    and 'request' to be available in the context of the application 
    (typically from Flask or a related extension).
    
    :param f: The view function to be wrapped (decorated).
    :type f: function
    :returns: The wrapped function or a redirection response.
    :rtype: function or werkzeug.wrappers.response.Response
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.role != "super_admin":
            flash("Anda tidak bisa mengakses halaman ini","error")
            return redirect(request.referrer)
        return f(*args, **kwargs)
    return wrap
    