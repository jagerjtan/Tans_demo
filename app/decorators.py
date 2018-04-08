# coding: utf8

from flask import redirect,flash,session,url_for
from functools import wraps

# Admin访问限制装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" in session and "admin_id" in session:
            flash("online", "stat1")
            return f(*args, **kwargs)
        else:
            flash("offline", "stat2")
            return redirect(url_for("admin.login", next=request.url))

    return decorated_function