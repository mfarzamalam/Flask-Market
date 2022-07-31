from market import app
from flask import render_template
from market.models import Item
from .forms import RegisterForm


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


@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)