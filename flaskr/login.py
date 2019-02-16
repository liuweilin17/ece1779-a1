# handle login, logout and register

from flask import render_template, request, flash, redirect, url_for, session
from flaskr import app
from flaskr import forms
from flaskr import db
from flaskr.models import User
import hashlib
import base64
import uuid

def hash_password(salt, password):
    t_sha = hashlib.sha512()
    t_sha.update(str(password + salt).encode('utf-8'))
    return base64.urlsafe_b64encode(t_sha.digest())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        logout()

    form = forms.LoginForm()
    if form.validate_on_submit():
        valid = True
        message = ''
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user:
            password_hash = hash_password(user.salt, password)
            user = User.query.filter_by(username=username, password_hash=password_hash).first()
            if not user:
                valid = False
                message = "Username or Password does not exist"
        else:
            valid = False
            message = "Username or Password does not exist"

        if valid:
            session['user']=user.serialize()
            return redirect(url_for('home'))
        else:
            flash(message)

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        logout()
        return redirect(url_for('home'))

    form = forms.RegisterForm()
    if form.validate_on_submit():
        valid = True
        message = ''
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        user = User.query.filter_by(username=username).first()
        if user:
            valid = False
            message = 'Username has already existed'
        else:
            salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
            salt = salt.decode('utf-8')
            password_hash = hash_password(salt, password1)
            user = User(username=username, password_hash=password_hash, salt=salt)
            db.session.add(user)
            db.session.commit()
            message="Sign up successfully!"
        if valid:
            flash(message, "success")
        else:
            flash(message, "danger")

    return render_template('register.html', form=form)
