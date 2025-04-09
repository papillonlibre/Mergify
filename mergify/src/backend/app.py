# backend/app.py
from flask import Flask, redirect, request, jsonify, make_response
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow cross-origin from React frontend

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
FRONTEND_URI = os.getenv("FRONTEND_URI")

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
    app.run(debug=True, port=5000)
