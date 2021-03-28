from sqlalchemy import func
from .models import User, Rating, Movie, connect_to_db, db
from datetime import datetime

def load_movies():
    """Load movies from u.item into database."""
    
    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Movie.query.delete()

    print("Movie")

    f = open("website/seed_data/u.item", encoding = "ISO-8859-1")
    lines = f.readlines()
    result = []
    for item in lines:
        result.append(item.split('|'))

    for i in range(len(result)):
        movie_id = result[i][0]
        title = [result[i][1]]

        for item in title:
            item = item.split(" ")
            item.pop()
            title = " ".join(item)

        released_str = result[i][2]


        imdb_url = result[i][4]

        if released_str:
            released_at = datetime.strptime(released_str, "%d-%b-%Y").date()
        else:
            released_at = None

        movie = Movie(movie_id=movie_id,
                title=title,
                released_at=released_at,
                imdb_url=imdb_url)
        db.session.add(movie)
    db.session.commit()

def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("website/seed_data/u.user", encoding = "ISO-8859-1"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print("ratings")

    Rating.query.delete()

    f=open("website/seed_data/u.data", encoding = "ISO-8859-1")
    lines = f.readlines()
    result = []

    for item in lines:
        result.append(item.split('\t'))

    for i in range(len(result)):
        user_id = result[i][0]
        movie_id = result[i][1]
        score = result[i][2]


        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])
    print(max_id)
    
    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id })
    db.session.commit()

def seed_database():
    load_movies()
    load_users()
    load_ratings()
    set_val_user_id()