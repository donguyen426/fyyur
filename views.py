from flask import Flask, Response, flash, redirect, render_template, request, url_for
from models import *
from forms import *

from utils import Utils
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


# @app.route("/")
def index():
    return render_template("pages/home.html")


#  Venues
#  ----------------------------------------------------------------

# BACKLOG: to reimplement
# @app.route("/venues")
def venues():
    # TODO: replace with real venues data.
    # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = [
        {
            "city": "San Francisco",
            "state": "CA",
            "venues": [
                {
                    "id": 1,
                    "name": "The Musical Hop",
                    "num_upcoming_shows": 0,
                },
                {
                    "id": 3,
                    "name": "Park Square Live Music & Coffee",
                    "num_upcoming_shows": 1,
                },
            ],
        },
        {
            "city": "New York",
            "state": "NY",
            "venues": [
                {
                    "id": 2,
                    "name": "The Dueling Pianos Bar",
                    "num_upcoming_shows": 0,
                }
            ],
        },
    ]

    venues = Venue.query.group_by("id", "state", "city").order_by("state", "city").all()
    lastStateCity = ""
    areas = []
    for v in venues:
        # count num_upcoming_shows
        upcoming_shows_count = (
            db.session.query(Show)
            .filter(Show.venue_id == v.id)
            .filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            .count()
        )
        # venue data
        venue = {"id": v.id, "name": v.name, "num_upcoming_shows": upcoming_shows_count}

        # same area ?
        if lastStateCity == (v.state + "_" + v.city):
            areas[-1]["venues"].append(venue)
        # new area
        else:
            areas.append({"city": v.city, "state": v.state, "venues": [venue]})

        lastStateCity = v.state + "_" + v.city

    return render_template("pages/venues.html", areas=areas)


# @app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [
            {
                "id": 2,
                "name": "The Dueling Pianos Bar",
                "num_upcoming_shows": 0,
            },
            {
                "id": 3,
                "name": "xxx",
                "num_upcoming_shows": 1,
            },
        ],
    }
    q = request.form.get("search_term", "")
    venues = Venue.query.filter(Venue.name.ilike(f"%{q}%")).all()
    results = {}
    results["data"] = Utils.lmodel_to_ldict(venues)
    results["count"] = len(venues)
    return render_template(
        "pages/search_venues.html",
        results=results,
        search_term=q,
    )


# @app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data1 = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
        "past_shows": [
            {
                "artist_id": 4,
                "artist_name": "Guns N Petals",
                "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                "start_time": "2019-05-21T21:30:00.000Z",
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }

    venue = Utils.model_to_dict(Venue.query.get(venue_id)).copy()
    # query all upcoming shows and convert to proper data structure
    upcoming_shows = (
        db.session.query(
            Show.artist_id, Show.start_time, Artist.name, Artist.image_link
        )
        .join(Artist, Artist.id == Show.artist_id)
        .filter(Show.venue_id == venue_id)
        .filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        .all()
    )
    venue["upcoming_shows"] = Utils.lrow_to_ldict(upcoming_shows)
    venue["upcoming_shows_count"] = len(venue["upcoming_shows"])

    # query all past shows and convert to proper data structure
    past_shows = (
        db.session.query(
            Show.artist_id, Show.start_time, Artist.name, Artist.image_link
        )
        .join(Artist, Artist.id == Show.artist_id)
        .filter(Show.venue_id == venue_id)
        .filter(Show.start_time <= datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        .all()
    )
    venue["past_shows"] = [record._mapping for record in past_shows]
    venue["past_shows_count"] = len(venue["past_shows"])

    return render_template("pages/show_venue.html", venue=venue)


#  Create Venue
#  ----------------------------------------------------------------


# @app.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


# @app.route("/venues/create", methods=["POST"])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    try:
        form = VenueForm(request.form, meta={"csrf": False})
        if form.validate_on_submit():
            venue = Venue()
            form.populate_obj(venue)
            db.session.add(venue)
            db.session.commit()
            # on successful db insert, flash success
            flash("Venue " + form.name.data + " was successfully listed!")
        else:
            # display error message
            message = "***".join([str(err) for err in form.errors.items()])
            flash("FIELD ERRORS: " + message)
            return render_template("forms/new_artist.html", form=VenueForm())
    except SQLAlchemyError as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        print(e)
        db.session.rollback()
        flash("An error occurred. Venue " + form.name.data + " could not be inserted.")
    finally:
        db.session.close()
    return render_template("pages/home.html")


#  Edit Venue
#  ----------------------------------------------------------------

# @app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    # form = VenueForm()
    data = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    }

    # TODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


# BACKLOG: need to test the bad data
# @app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        form = VenueForm(request.form, meta={"csrf": False})
        if form.validate_on_submit():
            venue = Venue.query.get(venue_id)
            form.populate_obj(venue)
            db.session.commit()
            flash("Venue " + form.name.data + " was successfully updated!")
        else:
            message = "***".join([str(err) for err in form.errors.items()])
            flash("FIELD ERRORS: " + message)
            return render_template("forms/edit_venue.html", form=form, venue=venue)
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash("An error occurred. Venue " + form.name.data + " could not be inserted.")
    finally:
        db.session.close()
    return redirect(url_for("show_venue", venue_id=venue_id))


# @app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        db.session.delete(Venue.query.get(venue_id))
        db.session.commit()
        flash("Venue deleted succesfully")
    except SQLAlchemyError as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        print(e)
        db.session.rollback()
        flash("Venue deleted unsuccesfully")
    finally:
        db.session.close()
    return redirect(url_for("index"))


#  Artists
#  ----------------------------------------------------------------
# @app.route("/artists")
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Utils.lrow_to_ldict(db.session.query(Artist.id, Artist.name).all())
    return render_template("pages/artists.html", artists=artists)


# BACKLOG: not tested yet
# @app.route("/artists/search", methods=["POST"])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [
            {
                "id": 4,
                "name": "Guns N Petals",
                "num_upcoming_shows": 0,
            }
        ],
    }
    q = request.form.get("search_term", "")
    artists = Venue.query.filter(Venue.name.ilike(f"%{q}%")).all()
    results = {}
    results["data"] = Utils.lmodel_to_ldict(artists)
    results["count"] = len(artists)

    return render_template(
        "pages/search_artists.html",
        results=results,
        search_term=q,
    )


# @app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    data1 = {
        "id": 1,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "past_shows": [
            {
                "venue_id": 1,
                "venue_name": "The Musical Hop",
                "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
                "start_time": "2019-05-21T21:30:00.000Z",
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data2 = {
        "id": 2,
        "name": "Matt Quevedo",
        "genres": ["Jazz"],
        "city": "New York",
        "state": "NY",
        "phone": "300-400-5000",
        "facebook_link": "https://www.facebook.com/mattquevedo923251523",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "past_shows": [
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2019-06-15T23:00:00.000Z",
            }
        ],
        "upcoming_shows": [],
        "past_shows_count": 1,
        "upcoming_shows_count": 0,
    }
    data3 = {
        "id": 3,
        "name": "The Wild Sax Band",
        "genres": ["Jazz", "Classical"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "432-325-5432",
        "seeking_venue": False,
        "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "past_shows": [],
        "upcoming_shows": [
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-01T20:00:00.000Z",
            },
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-08T20:00:00.000Z",
            },
            {
                "venue_id": 3,
                "venue_name": "Park Square Live Music & Coffee",
                "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
                "start_time": "2035-04-15T20:00:00.000Z",
            },
        ],
        "past_shows_count": 0,
        "upcoming_shows_count": 3,
    }
    # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
    artist = Utils.model_to_dict(Artist.query.get(artist_id)).copy()
    artist["genres"] = Utils.convert_genres(artist["genres"])
    upcoming_shows = (
        db.session.query(Show.venue_id, Show.start_time, Venue.name, Venue.image_link)
        .join(Venue, Venue.id == Show.venue_id)
        .filter(Show.artist_id == artist_id)
        .filter(Show.start_time > datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        .all()
    )
    artist["upcoming_shows"] = Utils.lrow_to_ldict(upcoming_shows)
    artist["upcoming_shows_count"] = len(artist["upcoming_shows"])
    past_shows = (
        db.session.query(Show.venue_id, Show.start_time, Venue.name, Venue.image_link)
        .join(Venue, Venue.id == Show.venue_id)
        .filter(Show.artist_id == artist_id)
        .filter(Show.start_time <= datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        .all()
    )
    artist["past_shows"] = Utils.lrow_to_ldict(past_shows)
    artist["past_shows_count"] = len(artist["past_shows"])
    print(artist["genres"])
    return render_template("pages/show_artist.html", artist=artist)


#  Create Artist
#  ----------------------------------------------------------------


# @app.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


# @app.route("/artists/create", methods=["POST"])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        form = ArtistForm(request.form, meta={"csrf": False})
        if form.validate_on_submit():
            artist = Artist()
            form.populate_obj(artist)
            artist.genres = ",".join([str(g) for g in form.genres.data])
            db.session.add(artist)
            db.session.commit()
            # on successful db insert, flash success
            flash("Artist " + form.name.data + " was successfully listed!")
        else:
            message = "***".join([str(err) for err in form.errors.items()])
            flash("FIELD ERRORS: " + message)
            return render_template("forms/new_artist.html", form=ArtistForm())
    # TODO: on unsuccessful db insert, flash an error instead.
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash("An error occurred. Artist " + form.name.data + " could not be inserted.")
    finally:
        db.session.close()
    return render_template("pages/home.html")


# BACKLOG: genres is not displayed
# @app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    # form = ArtistForm()
    data = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    artist = Artist.query.get(artist_id)

    # artist["genres"] = str(artist["genres"]).split(",")
    form = ArtistForm(obj=artist)
    return render_template("forms/edit_artist.html", form=form, artist=artist)


# BACKLOG: need to test the bad data
# @app.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        form = ArtistForm(request.form, meta={"csrf": False})
        if form.validate_on_submit():
            artist = Artist.query.get(artist_id)
            form.populate_obj(artist)
            db.session.commit()
            flash("Artist " + form.name.data + " was successfully updated!")
        else:
            message = "***".join([str(err) for err in form.errors.items()])
            flash("FIELD ERRORS: " + message)
            return render_template("forms/edit_artist.html", form=form, artist=artist)
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()
        flash("An error occurred. Venue " + form.name.data + " could not be inserted.")
    finally:
        db.session.close()
    return redirect(url_for("show_artist", artist_id=artist_id))


#  Shows
#  ----------------------------------------------------------------

# BACKLOG : fix data fields
# @app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = [
        {
            "venue_id": 1,
            "venue_name": "The Musical Hop",
            "artist_id": 4,
            "artist_name": "Guns N Petals",
            "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            "start_time": "2019-05-21T21:30:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 5,
            "artist_name": "Matt Quevedo",
            "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            "start_time": "2019-06-15T23:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-01T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-08T20:00:00.000Z",
        },
        {
            "venue_id": 3,
            "venue_name": "Park Square Live Music & Coffee",
            "artist_id": 6,
            "artist_name": "The Wild Sax Band",
            "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
            "start_time": "2035-04-15T20:00:00.000Z",
        },
    ]

    shows = Utils.lrow_to_ldict(
        db.session.query(
            Show.venue_id.label("venue_id"),
            Venue.name.label("venue_name"),
            Show.artist_id.label("artist_id"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image_link"),
            Show.start_time.label("start_time"),
        )
        .join(Venue, Venue.id == Show.venue_id)
        .join(Artist, Artist.id == Show.artist_id)
        .all()
    )
    return render_template("pages/shows.html", shows=shows)


# @app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


# @app.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    try:
        form = ShowForm(request.form, meta={"csrf": False})
        if form.validate_on_submit():
            show = Show()
            form.populate_obj(show)
            db.session.add(show)
            db.session.commit()
            # on successful db insert, flash success
            flash("Show was successfully listed!")
    except SQLAlchemyError as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash("An error occured. Show could not be inserted")
    finally:
        db.session.close()
    return render_template("pages/home.html")
