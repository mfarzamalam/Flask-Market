from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=30), nullable=False, unique=True)
    desc = db.Column(db.String(length=1024), nullable=False)

    def __repr__(self):
        return str(self.name)



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