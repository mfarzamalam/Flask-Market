from market import app
from flask import flash, render_template, redirect, url_for
from market.models import Item, User
from .forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user


@app.route('/starter')
def hello_world():
    return "Hello, World!!!"


@app.route('/profile/<username>')
def user_profile(username):
    return f"Welcome {username}!"


@app.route('/home')
@app.route('/')
def home_page():
    return render_template('home.html', page_name='home')


@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', page_name='market', items=items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password1.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('market_page'))
    elif form.errors != {}:
        print("errors:", form.errors)
        return render_template('register.html', form=form, errors=form.errors)
    else:
        return render_template('register.html', form=form, errors='')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    errors = ''
    if form.validate_on_submit():
        user_obj = User.query.filter_by(username=form.username.data).first()
        if user_obj and user_obj.authenticate_user(user_input_password=form.password.data):
            login_user(user_obj)
            flash("You are logged in successfully", category='success')
            return redirect(url_for('market_page'))
        else:
            errors = ["Username or password is not correct".title()]

    return render_template('login.html', form=form, errors=errors)


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    flash("You are logged out successfully", category='success')
    return redirect(url_for('market_page'))