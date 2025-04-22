# backend/app.py
from flask import Flask, redirect, request, jsonify, make_response
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin from React frontend

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")

def get_spotipy_client():
    scope = 'playlist-read-private'
    # scope = "user-library-read" # not giving the right ones
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=scope))
    return sp

def get_user_playlists(sp):
    results = sp.current_user_playlists(limit=50)
    print(f"The number of playlists retrieved for me is {len(results)}")
    for i, item in enumerate(results['items']):
        print("%d %s" % (i, item['name']))

def get_user_top_artists(sp):
    # scope = 'user-top-read'
    # ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ['short_term', 'medium_term', 'long_term']:
        print("range:", sp_range)

    results = sp.current_user_top_artists(time_range=sp_range, limit=50)

    for i, item in enumerate(results['items']):
        print(i, item['name'])
    print()

@app.route('/')
def home():
    return "Mergify Flask Backend is running!"

@app.route('/login')
def login():
    scopes = "user-read-private playlist-read-private playlist-modify-private playlist-modify-public"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scopes.replace(' ', '%20')}"
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Capture the query parameters from Spotify's redirect
    code = request.args.get('code')

    if not code:
        return redirect(FRONTEND_URI)  # You can redirect to a custom error page if needed

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

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    sp = get_spotipy_client()
    get_user_playlists(sp)
    get_user_top_artists(sp)