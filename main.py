#!/usr/bin python3
#!/usr/bin/env python3

import logging
import os
import sys
from bottle import Bottle, run, route, template, TEMPLATE_PATH, error, static_file, redirect, request
import datetime
import spotipy
import spotipy.util
from spotipy import oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json

app = Bottle()

# globals
logging.basicConfig(level = logging.DEBUG, format = "%(asctime)s - %(levelname)s - %(message)s")
CLIENT_ID     = "e29426dfb22c41cdbc92122fbb9c398c"
CLIENT_SECRET = "837fd2824bec47e5a003419165674bdd"
SCOPE = "user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"
CACHE = ".spotifyoauthcache"
CLIENT_CREDENTIALS = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
SP_OAUTH2 = oauth2.SpotifyOAuth(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = "http://localhost:8000/verified", scope = SCOPE, cache_path = CACHE)
LIMIT = 50
OFFSET = 0
SESSION = requests.Session()

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


def has_token():
	if not get_token():
		get_token()
	spotify = spotipy.Spotify(auth = get_token(), client_credentials_manager = CLIENT_CREDENTIALS)
	return spotify

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
try:
	spotify = has_token()
except spotipy.client.SpotifyException:
	token = get_token()
	spotify = spotipy.Spotify(auth = token, client_credentials_manager = CLIENT_CREDENTIALS)

# Static Routes
@app.route("/static/css/<filepath:re:.*\.css>")
@app.route("/static/css/<filepath:re:.*\.css>/")
def css(filepath):
    return static_file(filepath, root="static/css")

@app.route("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
@app.route("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>/")
def font(filepath):
    return static_file(filepath, root="static/font")

@app.route("/static/img/<filepath:re:.*\.(jpg|jpeg|png|gif|ico|svg)>")
@app.route("/static/img/<filepath:re:.*\.(jpg|jpeg|png|gif|ico|svg)>/")
def img(filepath):
    return static_file(filepath, root="static/img")

@app.route("/static/js/<filepath:re:.*\.js>")
@app.route("/static/js/<filepath:re:.*\.js>/")
def js(filepath):
    return static_file(filepath, root="static/js")

# web interface

@app.route("/")
def root():
	"""
		TODO: check if user is logged in.
	"""
	htmlLoginButton = getSPOauthURI()
	return template("index.html", year = datetime.datetime.now().year, link = htmlLoginButton)

@app.route("/", method = "POST")
@app.route("/search/<keyword>/<type>", method = "POST")
@app.route("/search/<keyword>/<type>/", method = "POST")
def get_results():
	redirect("/search/" + request.forms.get("search") + "/" + request.forms.get("type"))
	search(request.forms.get("search"), request.forms.get("type"))

@app.route("/search/<keyword>/<type>")
@app.route("/search/<keyword>/<type>/")
def search(keyword, type):
	"""
		Searhces data according to the filters.
		TODO: check if logged in.
		TODO: have logged in mode.
	"""
	result = spotify.search(q = keyword, limit = LIMIT, offset = OFFSET, type = type)
	return template("search.html", keyword = keyword, result = result, year = datetime.datetime.now().year, type = type, prev_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "next"), link = getSPOauthURI(), offset_data = get_offset_data(prev_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = OFFSET, limit = LIMIT, mode = "next"), result = result, type = type))

@app.route("/search/<keyword>/<type>/<curr_offset:int>")
@app.route("/search/<keyword>/<type>/<curr_offset:int>/")
def page(keyword, type, curr_offset):
	"""
		TODO: check if logged in.
		TODO: have logged in mode.
	"""
	if curr_offset < 0:
		return template("error.html")
	result = spotify.search(q = keyword, limit = LIMIT, offset = curr_offset, type = type)
	return template("search.html", keyword = keyword, result = result, year = datetime.datetime.now().year, type = type, prev_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "next"), link = getSPOauthURI(), offset_data = get_offset_data(prev_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "prev"), next_offset = get_offset(offset = curr_offset, limit = LIMIT, mode = "next"), result = result, type = type))

@app.route("/verified")
def verify():
	if get_token():
		""" 
			TODO: get cookies from spotify auth link
		"""
		# print(SESSION.)
		redirect("/most_played")

@app.route("/most_played")
@app.route("/most_played/")
@app.route("/most_played", method = "POST")
@app.route("/most_played/", method = "POST")
def get_most_played():
	"""
		TODO: check if logged in.
		TODO: have logged in mode.
	"""
	spotify = spotipy.Spotify(auth = get_token())
	spotify.trace = False
	logging.debug("Running get_most_played()")

	short_term_artists = spotify.current_user_top_artists(time_range = "short_term", limit = 100)["items"]
	short_term_tracks = spotify.current_user_top_tracks(time_range = "short_term", limit = 50)["items"]
	medium_term_artists = spotify.current_user_top_artists(time_range = "medium_term", limit = 100)["items"]
	medium_term_tracks = spotify.current_user_top_tracks(time_range = "medium_term", limit = 50)["items"]
	long_term_artists = spotify.current_user_top_artists(time_range = "long_term", limit = 100)["items"]
	long_term_tracks = spotify.current_user_top_tracks(time_range = "long_term", limit = 50)["items"]
	return template("most_played.html", spotify = spotify, short_term_artists = short_term_artists, short_term_tracks = short_term_tracks, medium_term_artists = medium_term_artists, medium_term_tracks = medium_term_tracks, long_term_artists = long_term_artists, long_term_tracks = long_term_tracks, year = datetime.datetime.now().year)


"""
	TODO: make playlist based on filter values and data shown.
	TODO: make function that handles pagination.
"""



# error pages
@app.route("/error")
@app.error(404)
def error_page(error):
	return template("error.html")

if __name__ == "__main__":
	run(app = app, host = "localhost", port = 8000, debug = True, reloader = True)
