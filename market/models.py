from email.policy import default
from enum import unique
from market import db


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    email = db.Column(db.String(length=250), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.Integer(), nullable=False, default=100)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self) -> str:
        return str(self.username)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=30), nullable=False, unique=True)
    desc = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return str(self.name)