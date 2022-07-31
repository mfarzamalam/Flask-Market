from market import app
from flask import render_template, redirect, url_for
from market.models import Item, User
from .forms import RegisterForm
from market import db


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
            password_hash = form.password1.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('market_page'))
    elif form.errors != {}:
        print("errors:", form.errors)
        return render_template('register.html', form=form, errors=form.errors)
    else:
        return render_template('register.html', form=form)