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
    return render_template('home.html')