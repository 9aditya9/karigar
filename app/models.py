from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

#association table

# booked = db.Table('booked',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('services_id', db.Integer, db.ForeignKey('services.id'))
# )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    booked_service = db.relationship('Booked',
                                    backref='customer',
                                    lazy='dynamic')

    posts = db.relationship('Post', backref='author', lazy='dynamic')
   # booked_service = db.relationship('Booked', backref='customer', lazy='dynamic')

    # services = db.relationship("Services", secondary="booked", lazy='subquery', backref=db.backref('users', lazy=True))
    # services_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    # followed = db.relationship(
    # 'Services', secondary=booked,
    # primaryjoin=(booked.c.services_id == services_id),
    # secondaryjoin=(booked.c.user_id == id),
    # backref=db.backref('booked', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?s={}'.format(digest, size)
        # return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    name = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return '<Services {}{}{}>'.format(self.id, self.name, self.price)




class Booked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    services_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
#    services_name = db.Column(db.String, db.ForeignKey('services.name'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    services=db.relationship('Services', backref='booker')
    def __repr__(self):
        """
        docstring
        """
        return '<Booked {}{}{}>'.format(self.id, self.services_id, self.user_id)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
