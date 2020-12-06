from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddServiceForm
from app.models import User, Post, Services, Booked
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():

    posts = [{
        'author': {
            'username': 'John'
        },
        'body': 'Beautiful day in Portland!'
    }, {
        'author': {
            'username': 'Susan'
        },
        'body': 'The Avengers movie was so cool!'
    }]
    form = LoginForm()
    reg_form = RegistrationForm()
    return render_template('index.html',
                           title='Home Page',
                           form=form,
                           reg_form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    reg_form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse.netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('index.html',
                           title='Sign In',
                           form=form,
                           reg_form=reg_form)


#changed url from login.html


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        user = User(username=reg_form.username.data, email=reg_form.email.data)
        user.set_password(reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('index.html', title='Register', reg_form=reg_form)


#changed url from register.html


@app.route('/user')
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [{
        'author': user,
        'body': 'Test post #1'
    }, {
        'author': user,
        'body': 'Test post #2'
    }]
#    booked_service = user.booked_service.order_by(Booked.timestamp.desc())
    #result = db.session.query(Services).join(Booked).filter(Booked.user_id == user.id)
    #booked = Booked.query.filter(Booked.user_id == user.id)
    #services = Services.query.all()
    result=db.session.query(Services, Booked).join(Booked, Booked.services_id == Services.id).filter(Booked.user_id==user.id).all()
    return render_template('user.html',
                           user=user,
                           posts=posts,
                           title='My Account',
                           result=result)


#changed posts=posts


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           form=form)


@app.route('/service')
@app.route('/services/')
@app.route('/services')
def services():
    # if session.get("user_id") is None:
    #     return render_template("services.html", name="SignIn/SignUp")
    return render_template('services.html', title='Services')


@app.route('/services/deepcleaning')
@app.route('/services/deepcleaning/')
@app.route('/services/dc/')
@app.route('/services/dc')
def deepcleaning():
    title = 'Deep Cleaning'
    serviceId = Services.query.filter_by(name='deep cleaning').first()

    return render_template("deepcleaning.html",
                           serviceId=serviceId,
                           title='Deep Cleaning')


@app.route('/booked')
@login_required
def add_book():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    serviceId = request.args.get('serviceId')
    order = Booked(services_id=serviceId, customer=current_user)
    db.session.add(order)
    db.session.commit()

    flash('Thank You, our Karigar will be on your doorstep soon!')
    return render_template(url_for('user'))


@app.route('/add', methods=['GET', 'POST'])
def addService():
    add_form = AddServiceForm()
    if add_form.validate_on_submit():
        name = Services(name=add_form.name.data, price=add_form.price.data)
        db.session.add(name)
        db.session.commit()
        return render_template(url_for('all'))
    return render_template("add.html", form=add_form)


@app.route('/all')
def all():
    services = Services.query.all()
    return render_template("all.html", services=services)

@app.route('/nuser')
def nuser():
    return render_template("nuser.html")
