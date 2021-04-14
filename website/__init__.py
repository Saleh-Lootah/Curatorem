from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from jinja2 import StrictUndefined


ENV = 'dev'
SEED = False
OMDB = 'http://www.omdbapi.com/?i=tt3896198&apikey=d92d85b8'

###############################################################

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HelloWorld'
    #app.jinja_env.undefined = StrictUndefined

    ###########################################################

    from .models import connect_to_db, db, User, Rating, Movie
    from .seed import seed_database

    if ENV == 'dev':
        app.debug = True
        app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
        connect_to_db(app)
    else:
        app.debug = False
        connect_to_db(app)

    if SEED == True:
        db.drop_all(app=app)
        db.create_all(app=app)
        seed_database()
    else:
        db.create_all(app=app)
    

    ###########################################################

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    ###########################################################

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app