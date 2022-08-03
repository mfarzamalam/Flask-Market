from market import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    email = db.Column(db.String(length=250), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=100), nullable=False)
    price = db.Column(db.Integer(), nullable=False, default=100)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def pretty_price(self):
        num = self.price
        new_num=str(num)
        
        if len(str(num)) > 3:
            divide=0
            count=0
            new_num=''
            for i in str(num):
                new_num+=i
                if count > 0:
                    divide += 1
                if divide%3 == 0:
                    new_num+=','
                
                count+=1
        
            if new_num[-1] == ',':
                new_num = new_num[0:-1]
        
        new_num+='$'
        return new_num

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, get_password):
        self.password_hash = bcrypt.generate_password_hash(get_password).decode('utf-8')

    def authenticate_user(self, user_input_password):
        return bcrypt.check_password_hash(self.password_hash, user_input_password)

    def __repr__(self) -> str:
        return str(self.username)

    def can_purchase(self, item_obj):
        return self.price >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=30), nullable=False, unique=True)
    desc = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return str(self.name)

    def buy(self, user):
        self.owner = user.id
        user.price -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.price += self.price
        db.session.commit()