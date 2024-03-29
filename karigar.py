from app import app, db
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}


#The Flask application instance is called app and is a member of the app package.
#The from app import app statement imports the app variable that is a member of the app package.
#If you find this confusing, you can rename either the package or the variable to something else.
