from flask import Flask, render_template

app = Flask(__name__)

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
    items = [
        {'id':1, 'name': 'Product Name 1', 'barcode':'asd213asdd2vggxz', 'price':201},
        {'id':2, 'name': 'Product Name 2', 'barcode':'asd213asdd2vggxz', 'price':202},
        {'id':3, 'name': 'Product Name 3', 'barcode':'asd213asdd2vggxz', 'price':203},
        {'id':4, 'name': 'Product Name 4', 'barcode':'asd213asdd2vggxz', 'price':204},
    ]
    return render_template('market.html', page_name='market', items=items)