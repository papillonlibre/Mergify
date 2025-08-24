import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Spotify credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

# Scopes your app needs
SCOPES = [
    'playlist-read-private',
    'user-top-read',
    'user-library-read',
    'playlist-modify-public',
    'playlist-modify-private',
    'playlist-read-collaborative'
]

def get_spotipy_client(access_token=None):
    """Create a Spotipy client, either from a raw access_token or via OAuth."""
    try:
        if access_token:
            return spotipy.Spotify(auth=access_token)
        
        auth_manager = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=' '.join(SCOPES)
        )
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        logger.error(f"Error creating Spotify client: {e}")
        raise

def get_user_playlists(sp):
    """Return names of the user's playlists."""
    try:
        results = sp.current_user_playlists(limit=50)
        return [item['name'] for item in results['items']]
    except SpotifyException as e:
        logger.error(f"Spotify error fetching playlists: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching playlists: {e}")
        return []

def get_liked_exclusive_songs(sp):
    """Return liked songs that are not in the user's own playlists."""
    user_id = sp.current_user()["id"]

    # Get all liked songs
    liked_songs = []
    limit, offset = 50, 0
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results['items']
        if not items:
            break
        liked_songs.extend(items)
        offset += limit

    liked_ids = {item['track']['id'] for item in liked_songs if item['track']}

    # Collect tracks from user's own playlists
    own_ids = set()
    offset = 0
    while True:
        playlists = sp.current_user_playlists(limit=50, offset=offset)
        if not playlists['items']:
            break
        for playlist in playlists['items']:
            if playlist['owner']['id'] == user_id:
                track_offset = 0
                while True:
                    tracks = sp.playlist_tracks(playlist['id'], offset=track_offset)
                    if not tracks['items']:
                        break
                    for item in tracks['items']:
                        track = item.get('track')
                        if track:
                            own_ids.add(track['id'])
                    track_offset += len(tracks['items'])
        offset += 50

    only_liked = liked_ids - own_ids
    return [item['track']['name'] for item in liked_songs if item['track']['id'] in only_liked]

def fetch_top_artists(sp, requested_range=None, limit=5, simple=False):
    """Fetch user's top artists for one or multiple ranges."""
    valid_ranges = ['short_term', 'medium_term', 'long_term']
    if requested_range and requested_range not in valid_ranges:
        raise ValueError("Invalid range value")

    result = {}
    ranges = [requested_range] if requested_range else valid_ranges

    for r in ranges:
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
    return result
