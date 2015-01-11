from flask import session, g, flash, redirect, url_for, request
from functools import wraps


def login_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['email'] = user.email

def logout_user(user):
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('email',None)

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return view(*args, **kwargs)
        else:
            flash('You need to login first.',"danger")
            return redirect(url_for('auth.login',next=request.url))
    return wrapper

def admin_required(view):
    @wraps(view)
    def wrapper(*args,**kwargs):
        if 'user_id' in session:
            if User.get_by_id(session.get('user_id')).is_admin:
                return view(*args,**kwargs)
        flash('You need to login as an administrator to access that page.',"danger")
        return redirect(url_for('auth.login',next=request.url))
    return wrapper




def get_token_expire_minutes(seconds):
   return int(seconds)/60

def get_token_expire_hours(seconds):
    return int(get_token_expire_minutes(seconds))/60

def get_expire_days(seconds):
    return int(get_token_expire_hours(seconds))/24

def expires_in(seconds):
    if get_token_expire_days(seconds) <= 1:
        if get_token_expire_hours(seconds) <= 1:
            return str(get_token_expire_minutes(seconds)) + ' Minutes'
        return str(get_token_expire_hours(seconds)) + ' Hours'
    return str(get_token_expire_days(seconds)) + ' Days'



