import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY'
    ) or '\x95a\xf5\xfc\x14\xe5\xfb\xc2\xbd\xb8\x83\x84\xf1\xd7@\xcd\xc1\x0e\xf1\xf2M\xbd|y'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']


#There are several formats for the application to specify configuration options.
#The most basic solution is to define your variables as keys in app.config,
#which uses a dictionary style to work with variables.
