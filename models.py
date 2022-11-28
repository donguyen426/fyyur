from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
from flask_migrate import Migrate

db = SQLAlchemy()


def configDB(app):
    app.config.from_object("config")
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class Venue(db.Model):
    __tablename__ = "Venue"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    address = Column(String(120))
    phone = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = Column(ARRAY(String))
    website = Column(String(500))
    seeking_talent = Column(Boolean, default=False)
    seeking_description = Column(String(500))

    shows = db.relationship("Show", backref="Venue", lazy="dynamic")


class Artist(db.Model):
    __tablename__ = "Artist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String(120))
    state = Column(String(120))
    phone = Column(String(120))
    genres = Column(String(120))
    image_link = Column(String(500))
    facebook_link = Column(String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = Column(String(500))
    seeking_venue = Column(Boolean, default=False)
    seeking_description = Column(String(500))

    shows = db.relationship("Show", backref="Artist", lazy=True)


# with app.app_context():
#     create_all()

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey("Venue.id"), nullable=False)
    artist_id = Column(Integer, ForeignKey("Artist.id"), nullable=False)
    start_time = Column(String(), nullable=False)
