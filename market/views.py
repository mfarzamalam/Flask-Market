from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


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


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password1.data
        )
        db.session.add(user_obj)
        db.session.commit()
        login_user(user_obj)
        flash("Account Created Successfully, You are logged in successfully", category='success')
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
    logout_user()
    flash("You are logged out successfully", category='info')
    return redirect(url_for('home_page'))


@app.route('/purchase_item')
def puchase_item(item_id, user_id):
    user_obj = User.query.filter_by(id=user_id)
    item = Item.query.filter_by(id=item_id)
    item.owner = user_obj.id
    db.session.add(user_obj)
    db.session.commit()

    return redirect(url_for('market_page'))