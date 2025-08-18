# backend/app.py
from flask import Flask, redirect, request, session, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.exceptions import SpotifyException
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin from React frontend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")

SCOPES = [
    'playlist-read-private',
    'user-top-read',
    'user-library-read',
    'playlist-modify-public',
    'playlist-modify-private',
    'playlist-read-collaborative'
]
def get_spotipy_client(access_token=None):
    try:
        if access_token:
            return spotipy.Spotify(auth=access_token)
        
        cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
        auth_manager = spotipy.oauth2.SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=' '.join(SCOPES),
            cache_handler=cache_handler
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        logger.error(f"Error creating Spotify client: {e}")
        raise


def get_user_playlists(sp):
    try:
        results = sp.current_user_playlists(limit=50)
        logger.info(f"Retrieved {len(results['items'])} playlists.")
        return [item['name'] for item in results['items']]
    except SpotifyException as e:
        logger.error(f"Spotify error fetching playlists for user {sp.current_user()['id']}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error (playlists): {e}")
        return []

def get_liked_exclusive_songs(sp):
    user_id = sp.current_user()["id"]
    liked_only_songs = []
    limit = 50
    offset = 0
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results['items']
        if not items:
            break
        liked_only_songs.extend(items)
        offset += limit
    liked_track_ids = set(item['track']['id'] for item in liked_only_songs if item['track'])

    own_playlist_track_ids = set()
    limit = 50
    offset = 0
    while True:
        playlists = sp.current_user_playlists(limit=limit, offset=offset)
        if not playlists['items']:
            break
        for playlist in playlists['items']:
            if playlist['owner']['id'] == user_id:
                playlist_id = playlist['id']
                track_offset = 0
                while True:
                    tracks = sp.playlist_tracks(playlist_id, offset=track_offset)
                    if not tracks['items']:
                        break
                    for item in tracks['items']:
                        track = item.get('track')
                        if track:
                            own_playlist_track_ids.add(track['id'])
                    track_offset += len(tracks['items'])
        offset += limit
    only_liked = liked_track_ids - own_playlist_track_ids

    return [item['track']['name'] for item in liked_only_songs if item['track']['id'] in only_liked]
@app.route('/')
def home():
    return "Mergify Flask Backend is running!"

@app.route('/login')
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={' '.join(SCOPES)}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code') # Capture the query parameters from Spotify's redirect

    if not code:
        return redirect(FRONTEND_URI)  # TODO: redirect to a custom error page

    # Add the `code` to the frontend redirect URL
    redirect_url = f"{FRONTEND_URI}/callback?code={code}"
    return redirect(redirect_url)

@app.route('/exchange_token', methods=["POST"])
def exchange_token():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code found in request"}), 400

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    r = requests.post(token_url, data=payload, headers=headers)
    token_data = r.json()

    if r.status_code != 200 or "access_token" not in token_data:
        return jsonify({"error": "Token exchange failed", "details": token_data}), 400

    return jsonify({
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"]
    })

@app.route('/get_liked_songs')
def get_liked_songs():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not access_token:
        return jsonify({"error": "Missing access token"}), 401

    sp = get_spotipy_client(access_token)
    liked_songs = get_liked_exclusive_songs(sp)
    return jsonify({"liked_songs": liked_songs})


@app.route('/fetch_playlists')
def fetch_playlists():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not access_token:
        return jsonify({"error": "Missing access token"}), 401

    sp = get_spotipy_client(access_token)
    playlists = get_user_playlists(sp)
    return jsonify({"playlists": playlists})

@app.route('/user/top-artists', methods=["GET"])
def get_all_top_artists():
    access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not access_token:
        return jsonify({"error": "Missing access token"}), 401

    time_ranges = ['short_term', 'medium_term', 'long_term']
    requested_range = request.args.get("range")  # Optional ?range=short_term
    limit = int(request.args.get("limit", 5))
    simple = request.args.get("simple", "false").lower() == "true"

    if requested_range and requested_range not in time_ranges:
        return jsonify({"error": "Invalid range value"}), 400

    try:
        sp = get_spotipy_client(access_token)
        result = {}

        ranges_to_query = [requested_range] if requested_range else time_ranges

        for r in ranges_to_query:
            artists = sp.current_user_top_artists(time_range=r, limit=limit)['items']
            if simple:
                result[r] = [artist['name'] for artist in artists]
            else:
                result[r] = [
                    {
                        "name": artist['name'],
                        "image": artist['images'][0]['url'] if artist.get("images") else None,
                        "genres": artist['genres']
                    }
                    for artist in artists
                ]
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error fetching top artists: {e}")
        return jsonify({"error": "Failed to fetch top artists", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)