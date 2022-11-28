# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import logging
from logging import FileHandler, Formatter

from flask import Flask

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_moment import Moment
import views
from models import *
from utils import Utils

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = configDB(app)

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

app.jinja_env.filters["datetime"] = Utils.format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/venues", view_func=views.venues)
app.add_url_rule("/venues/search", view_func=views.search_venues, methods=["POST"])
app.add_url_rule("/venues/<int:venue_id>", view_func=views.show_venue)
app.add_url_rule("/venues/create", view_func=views.create_venue_form, methods=["GET"])
app.add_url_rule(
    "/venues/create", methods=["POST"], view_func=views.create_venue_submission
)
app.add_url_rule("/venues/<venue_id>", methods=["DELETE"], view_func=views.delete_venue)
app.add_url_rule(
    "/venues/<int:venue_id>/edit", methods=["GET"], view_func=views.edit_venue
)
app.add_url_rule(
    "/venues/<int:venue_id>/edit",
    methods=["POST"],
    view_func=views.edit_venue_submission,
)
app.add_url_rule("/artists", view_func=views.artists)
app.add_url_rule("/artists/search", methods=["POST"], view_func=views.search_artists)
app.add_url_rule("/artists/<int:artist_id>", view_func=views.show_artist)
app.add_url_rule(
    "/artists/<int:artist_id>/edit", methods=["GET"], view_func=views.edit_artist
)
app.add_url_rule(
    "/artists/<int:artist_id>/edit",
    methods=["POST"],
    view_func=views.edit_artist_submission,
)
app.add_url_rule("/artists/create", methods=["GET"], view_func=views.create_artist_form)
app.add_url_rule(
    "/artists/create", methods=["POST"], view_func=views.create_artist_submission
)
app.add_url_rule("/shows", view_func=views.shows)
app.add_url_rule("/shows/create", view_func=views.create_shows)
app.add_url_rule(
    "/shows/create", methods=["POST"], view_func=views.create_show_submission
)


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


if not app.debug:
    file_handler = FileHandler("error.log")
    file_handler.setFormatter(
        Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]")
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("errors")

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == "__main__":
    app.run(debug=True)

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
