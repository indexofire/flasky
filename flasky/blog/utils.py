# -*- coding: utf-8 -*-
from functools import wraps
from google.appengine.api import users
from flask import redirect
from flask import request


def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view
