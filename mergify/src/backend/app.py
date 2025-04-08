# backend/app.py
from flask import Flask, redirect, request, jsonify, make_response
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from React dev server

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

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
    code = request.json.get("code")

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

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    if not access_token:
        return jsonify({"error": "Token exchange failed", "details": token_data}), 400

    # Create response and set HttpOnly cookie
    resp = make_response(redirect(FRONTEND_URI))
    resp.set_cookie("spotify_access_token", access_token, httponly=True, secure=False, samesite="Lax")
    resp.set_cookie("spotify_refresh_token", refresh_token, httponly=True, secure=False, samesite="Lax")

    return resp

if __name__ == '__main__':
    app.run(debug=True, port=5000)
