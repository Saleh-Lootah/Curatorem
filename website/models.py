from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()
# Hosted DB
DB_NAME = 'postgresql://saleh:12qwaszX@curatorem.postgres.database.azure.com/curaDB'
# Test DB
#DB_NAME = 'postgresql://postgres:12qwaszX@localhost:5432/Curatorem1.0'

class Rating(db.Model):
    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    score = db.Column(db.Integer, nullable=True)

    #Define relationship to user
    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))
    #Define relationship to movie
    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    rec_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))
    prediction = db.Column(db.Float, nullable=True)

    #Define relationship to user
    user = db.relationship("User", backref=db.backref("recommendations"), order_by=user_id)
    #Define relationship to movie
    movie = db.relationship("Movie", backref=db.backref("recommendations"), order_by=user_id)


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(200), nullable=True)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    

################# Helper functions #####################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.app = app
    db.init_app(app)