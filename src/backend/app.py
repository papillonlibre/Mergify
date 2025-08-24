from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import requests
import os
import logging
from dotenv import load_dotenv

from spotify_service import (
    get_spotipy_client,
    get_user_playlists,
    get_liked_exclusive_songs,
    fetch_top_artists, SCOPES
)

# Load env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")

# --- ROUTES ---

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
    code = request.args.get('code')
    if not code:
        return redirect(FRONTEND_URI)
    return redirect(f"{FRONTEND_URI}/callback?code={code}")

@app.route('/exchange_token', methods=["POST"])
def exchange_token():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code found"}), 400

    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token_data = r.json()
    if r.status_code != 200 or "access_token" not in token_data:
        return jsonify({"error": "Token exchange failed", "details": token_data}), 400

    return jsonify({
        "access_token": token_data["access_token"],
        "refresh_token": token_data.get("refresh_token")
    })

@app.route('/fetch_playlists')
def fetch_playlists():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing access token"}), 401
    sp = get_spotipy_client(token)
    return jsonify({"playlists": get_user_playlists(sp)})

@app.route('/get_liked_songs')
def liked_songs():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing access token"}), 401
    sp = get_spotipy_client(token)
    return jsonify({"liked_songs": get_liked_exclusive_songs(sp)})

@app.route('/user/top-artists')
def top_artists():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Missing access token"}), 401

    requested_range = request.args.get("range")
    limit = int(request.args.get("limit", 5))
    simple = request.args.get("simple", "false").lower() == "true"

    try:
        sp = get_spotipy_client(token)
        return jsonify(fetch_top_artists(sp, requested_range, limit, simple))
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Error fetching top artists: {e}")
        return jsonify({"error": "Failed to fetch top artists"}), 500

@app.route('/test-spotify')
def test_spotify():
    try:
        sp = get_spotipy_client()
        return jsonify({
            "playlists": get_user_playlists(sp),
            "top_artists": fetch_top_artists(sp, limit=5, simple=True)
        })
    except Exception as e:
        logger.error(f"Test route error: {e}")
        return jsonify({"error": "Spotify test failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
