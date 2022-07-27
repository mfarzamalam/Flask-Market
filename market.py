from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!!!"


@app.route('/profile/<username>')
def user_profile(username):
    return f"Welcome {username}!"