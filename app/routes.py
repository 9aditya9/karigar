from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddServiceForm
from app.models import User, Post, Services, Booked
from datetime import datetime

# index/home route
@app.route('/')
@app.route('/index')
def index():
    form = LoginForm()
    reg_form = RegistrationForm()
    return render_template('index.html',
                           title='Home Page')

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #  reg_form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page: 
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',
                           title='Sign In',
                           form=form)


#changed url from login.html


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


#changed url from register.html


@app.route('/user')
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #  posts = [{
    #      'author': user,
    #      'body': 'Test post #1'
    #  }, {
    #      'author': user,
    #      'body': 'Test post #2'
    #  }]
    #    booked_service = user.booked_service.order_by(Booked.timestamp.desc())
    #result = db.session.query(Services).join(Booked).filter(Booked.user_id == user.id)
    #booked = Booked.query.filter(Booked.user_id == user.id)
    #services = Services.query.all()
    result = db.session.query(Services, Booked).join(
        Booked, Booked.services_id == Services.id).filter(
            Booked.user_id == user.id).all()
    return render_template('user.html',
                           user=user,
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


@app.route('/booked')
@login_required
def add_book():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    serviceId = request.args.get('serviceId')
    order = Booked(services_id=serviceId, customer=current_user)
    db.session.add(order)
    db.session.commit()
    flash('Thank You! Your service has booked, our Karigar will be on your doorstep soon!')
    return redirect(url_for('services'))


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
    return render_template("2col.html")


@app.route('/services/deepcleaning')
@app.route('/services/deepcleaning/')
def deepcleaning():
    title = 'Deep Cleaning'
    serviceId = Services.query.filter_by(name='Deep Cleaning').first()
    return render_template("deepcleaning.html",
                           serviceId=serviceId,
                           title='Deep Cleaning')


@app.route('/services/haircut')
@app.route('/services/haircut/')
def haircut():
    title = 'Haircut'
    serviceId = Services.query.filter_by(name='Haircut').first()
    return render_template("haircut.html",
                           serviceId=serviceId,
                           title='Haircut')


@app.route('/services/washingmachinerepair')
@app.route('/services/washingmachinerepair/')
def washingmachinerepair():
    title = 'Washing Machine Repair'
    serviceId = Services.query.filter_by(name='Washing Machine Repair').first()
    return render_template("washingmachinerepair.html",
                           serviceId=serviceId,
                           title='Washing Machine Repair')


@app.route('/services/refrigeratorrepair')
@app.route('/services/refrigeratorrepair/')
def refrigeratorrepair():
    title = 'Refrigerator Repair'
    serviceId = Services.query.filter_by(name='Refrigerator Repair').first()
    return render_template("refrigeratorrepair.html",
                           serviceId=serviceId,
                           title='Refrigerator Repair')


@app.route('/services/tvrepair')
@app.route('/services/tvrepair/')
def tvrepair():
    title = 'TV Repair'
    serviceId = Services.query.filter_by(name='TV Repair').first()
    return render_template("tvrepair.html",
                           serviceId=serviceId,
                           title='TV Repair')


@app.route('/services/facial')
@app.route('/services/facial/')
def facial():
    title = 'Facial'
    serviceId = Services.query.filter_by(name='Facial').first()
    return render_template("facial.html", serviceId=serviceId, title='Facial')


@app.route('/services/bodyspa')
@app.route('/services/bodyspa/')
def bodyspa():
    title = 'Body Spa'
    serviceId = Services.query.filter_by(name='Body Spa').first()
    return render_template("bodyspa.html",
                           serviceId=serviceId,
                           title='Body Spa')


@app.route('/services/geyserrepair')
@app.route('/services/geyserrepair/')
def geyserrepair():
    title = 'Geyser Repair'
    serviceId = Services.query.filter_by(name='Geyser Repair').first()
    return render_template("geyserrepair.html",
                           serviceId=serviceId,
                           title='Geyser Repair')


@app.route('/services/haircutforwomen')
@app.route('/services/haircutforwomen/')
def haircutforwomen():
    title = 'Haircut for women'
    serviceId = Services.query.filter_by(name='Haircut for women').first()
    return render_template("haircutforwomen.html",
                           serviceId=serviceId,
                           title='Haircut for women')


@app.route('/services/bathroomcleaning')
@app.route('/services/bathroomcleaning/')
def bathroomcleaning():
    title = 'Bathroom Cleaning'
    serviceId = Services.query.filter_by(name='Bathroom Cleaning').first()
    return render_template("bathroomcleaning.html",
                           serviceId=serviceId,
                           title='Bathroom Cleaning')


@app.route('/services/kitchencleaning')
@app.route('/services/kitchencleaning/')
def kitchencleaning():
    title = 'Kitchen Cleaning'
    serviceId = Services.query.filter_by(name='Kitchen Cleaning').first()
    return render_template("kitchencleaning.html",
                           serviceId=serviceId,
                           title='Kitchen Cleaning')


@app.route('/services/plumber')
@app.route('/services/plumber/')
def plumber():
   title = 'Plumber'
   serviceId = Services.query.filter_by(name='Plumber').first()
   return render_template("plumber.html",
                          serviceId=serviceId,
                          title='Plumber')

@app.route('/services/electrician')
@app.route('/services/electrician/')
def electrician():
   title = 'Electrician'
   serviceId = Services.query.filter_by(name='Electrician').first()
   return render_template("electrician.html",
                          serviceId=serviceId,
                          title='Electrician')

@app.route('/services/painter')
@app.route('/services/painter/')
def painter():
   title = 'Painter'
   serviceId = Services.query.filter_by(name='Painter').first()
   return render_template("painter.html",
                          serviceId=serviceId,
                          title='Painter')


@app.route('/services/carpenter')
@app.route('/services/carpenter/')
def carpenter():
    title = 'Carpenter'
    serviceId = Services.query.filter_by(name='Carpenter').first()
    return render_template("carpenter.html",
                           serviceId=serviceId,
                           title='Carpenter')


@app.route('/services/floorcleaning')
@app.route('/services/floorcleaning/')
def floorcleaning():
    title = 'Floor Cleaning'
    serviceId = Services.query.filter_by(name='Floor Cleaning').first()
    return render_template("floorcleaning.html",
                           serviceId=serviceId,
                           title='Floor Cleaning')
