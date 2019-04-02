#!/usr/bin python3
#!/usr/bin/env python3

import logging
import os
import sys
from bottle import app, TEMPLATE_PATH, hook, route, template, static_file, request, error, redirect, run
from beaker.middleware import SessionMiddleware
import datetime
import spotipy
import spotipy.util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

# globals
logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
CLIENT_ID          = "e29426dfb22c41cdbc92122fbb9c398c"
CLIENT_SECRET      = "837fd2824bec47e5a003419165674bdd"
SCOPE              = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read"
CACHE              = ".spotifyoauthcache"
CLIENT_CREDENTIALS = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
SP_OAUTH2          = oauth2.SpotifyOAuth(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = "http://localhost:8000/verified", scope = SCOPE, cache_path = CACHE)
LIMIT              = 50
OFFSET             = 0
LOGIN_STATUS       = False
SESSION_OPTS       = {
	"session.type": "file",
	"session.cookie_expires": True,
	"session.data_dir": "./session/",
	"session.auto": True
}
SESSION            = SessionMiddleware(app(), SESSION_OPTS)

TEMPLATE_PATH.insert(0, "")

# global functions

def get_token():
	""" 
		Gets the access token

		returns:
		access_token - token from cache
	"""
	access_token = ""
	token_info = SP_OAUTH2.get_cached_token()
	if token_info:
		access_token = token_info["access_token"]
	else:
		url = request.url
		code = SP_OAUTH2.parse_response_code(url)
		if code:
			print("Found Spotify auth code in Request URL! "
				"Trying to get valid access token...")
			token_info = SP_OAUTH2.get_access_token(code)
			access_token = token_info["access_token"]

	return access_token

def getSPOauthURI():
	"""  
		Gets the Log in URL from Spotify.

		returns:
		auth_url - log in url
	"""

	auth_url = SP_OAUTH2.get_authorize_url()
	return auth_url


def get_offset(offset, limit, mode):
	""" Gets offset according to modes. """
	if mode == "next":
		return offset + limit
	return offset - limit

def get_offset_data(prev_offset, next_offset, result, type):
	""" Gets the current offset data then returns a JSON data, """
	offset_data = dict()
	offset_data["prev_offset"], offset_data["next_offset"], offset_data["total"] = prev_offset, next_offset, result[type + "s"]["total"]
	return json.dumps(offset_data)


# check if app has token.
spotify = spotipy.Spotify(auth = get_token(), client_credentials_manager = CLIENT_CREDENTIALS)


@hook("before_request")
def setup_request():
	request.session = request.environ["beaker.session"]

# Static Routes
@route("/static/css/<filepath:re:.*\.css>")
@route("/static/css/<filepath:re:.*\.css>/")
def css(filepath):
    return static_file(filepath, root="static/css")

@route("/static/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
@route("/static/fonts/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>/")
def font(filepath):
    return static_file(filepath, root="static/fonts")

@route("/static/img/<filepath:re:.*\.(jpg|jpeg|png|gif|ico|svg)>")
@route("/static/img/<filepath:re:.*\.(jpg|jpeg|png|gif|ico|svg)>/")
def img(filepath):
    return static_file(filepath, root="static/img")

@route("/static/js/<filepath:re:.*\.js>")
@route("/static/js/<filepath:re:.*\.js>/")
def js(filepath):
    return static_file(filepath, root="static/js")

# web interface

@route("/")
def root():
	"""
		Route of "/". Redirects to index.html
	"""
	current_user = None
	if "logged_in" in request.session:
		if request.session["logged_in"]:
			current_user = spotify.current_user()
		
	else:
		request.session["logged_in"] = False
	htmlLoginButton = getSPOauthURI()
	return template("index.html", year = datetime.datetime.now().year, link = htmlLoginButton, login_status = request.session["logged_in"], current_user = current_user)

@route("/", method = "POST")
@route("/search/<keyword>/<type>", method = "POST")
@route("/search/<keyword>/<type>/", method = "POST")
def get_results():
	redirect("/search/" + request.forms.get("search") + "/" + request.forms.get("type"))
	search(request.forms.get("search"), request.forms.get("type"))

@route("/search/<keyword>/<type>")
@route("/search/<keyword>/<type>/")
def search(keyword, type):
	"""
		Searhces data according to the filters.
		TODO: check if logged in.
		TODO: have logged in mode.
	"""

	current_user = None
	if "logged_in" in request.session:
		if request.session["logged_in"]:
			current_user = spotify.current_user()
		
	else:
		request.session["logged_in"] = False

	get_type = {}
	get_type["type"] = type
	result = spotify.search(q = keyword, limit = LIMIT, offset = OFFSET, type = type)
	return template("search.html", keyword = keyword, result = result, year = datetime.datetime.now().year, type = type, prev_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "next"), link = getSPOauthURI(), offset_data = get_offset_data(prev_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "next"), result = result, type = type), get_type = json.dumps(get_type), login_status = request.session["logged_in"], current_user = spotify.current_user())


@route("/search/<keyword>/<type>/<curr_offset:int>")
@route("/search/<keyword>/<type>/<curr_offset:int>/")
def page(keyword, type, curr_offset):
	"""
		returns "search.html". For pagination purposes
	"""

	current_user = None
	if "logged_in" in request.session:
		if request.session["logged_in"]:
			current_user = spotify.current_user()
		
	else:
		request.session["logged_in"] = False

	if curr_offset < 0:
		return template("error.html")
	get_type = {}
	get_type["type"] = type
	result = spotify.search(q = keyword, limit = LIMIT, offset = curr_offset, type = type)
	return template("search.html", keyword = keyword, result = result, year = datetime.datetime.now().year, type = type, prev_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "next"), link = getSPOauthURI(), offset_data = get_offset_data(prev_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "next"), result = result, type = type), get_type = json.dumps(get_type), login_status = request.session["logged_in"], current_user = spotify.current_user())


@route("/verified")
def verify():
	"""
		Verifies the session.
	"""
	if get_token():
		request.session["logged_in"] = True
		redirect("/most_played")

@route("/most_played")
@route("/most_played/")
def get_most_played():
	"""
		TODO: check if logged in.
		TODO: have logged in mode.
	"""
	if "logged_in" in request.session:
		if request.session["logged_in"]:
			spotify = spotipy.Spotify(auth = get_token())
			current_user = spotify.current_user()
			spotify.trace = False
			logging.debug("Running get_most_played()")

			short_term_artists = spotify.current_user_top_artists(time_range = "short_term", limit = 100)["items"]
			short_term_tracks = spotify.current_user_top_tracks(time_range = "short_term", limit = 50)["items"]
			medium_term_artists = spotify.current_user_top_artists(time_range = "medium_term", limit = 100)["items"]
			medium_term_tracks = spotify.current_user_top_tracks(time_range = "medium_term", limit = 50)["items"]
			long_term_artists = spotify.current_user_top_artists(time_range = "long_term", limit = 100)["items"]
			long_term_tracks = spotify.current_user_top_tracks(time_range = "long_term", limit = 50)["items"]
			return template("most_played.html", spotify = spotify, short_term_artists = short_term_artists, short_term_tracks = short_term_tracks, medium_term_artists = medium_term_artists, medium_term_tracks = medium_term_tracks, long_term_artists = long_term_artists, long_term_tracks = long_term_tracks, year = datetime.datetime.now().year, login_status = request.session["logged_in"], current_user = current_user, date = datetime.datetime.now())
		else:
			redirect(getSPOauthURI())
	else:
		request.session["logged_in"] = False
		redirect(getSPOauthURI())

@route("/most_played", method = "POST")
@route("/most_played/", method = "POST")
def make_playlist():
	logging.debug("Running make_playlist()")
	playlist_name = request.forms.get("playlist_name")
	playlist_desc = request.forms.get("playlist_desc")
	playlist_term = request.forms.get("playlist_term")


	track_list = []
	playlist_obj = spotify.user_playlist_create(spotify.current_user()["id"], playlist_name, public = True, description = playlist_desc)
	tracks = spotify.current_user_top_tracks(time_range = playlist_term, limit = 50)["items"]
	for track in tracks:
		track_list.append(track["id"])
	spotify.user_playlist_add_tracks(user = spotify.current_user()["id"], playlist_id = playlist_obj["id"], tracks = track_list)
	redirect("/most_played")

@route("/logout")
def logout():
	request.session["logged_in"] = False
	os.unlink(CACHE)
	redirect("/")

# error pages
@route("/error")
@error(404)
def error_page(error):
	return template("error.html")

if __name__ == "__main__":
	run(app = SESSION, host = "localhost", port = 8000, debug = True, reloader = True)
