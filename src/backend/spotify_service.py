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

def paginate_spotify(sp_func, limit=50, **kwargs):
    """Generic paginator for Spotify endpoints that uses limit/offset"""
    results = []
    offset = 0
    while True:
        page = sp_func(limit=limit, offset=offset, **kwargs)
        items = page.get('items', [])
        if not items:
            break
        results.extend(items)
        offset += limit
    return results

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
        playlists = paginate_spotify(sp.current_user_playlists)
        return [p['name'] for p in playlists]
    except SpotifyException as e:
        logger.error(f"Spotify error fetching playlists: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching playlists: {e}")
        return []

def get_liked_exclusive_songs(sp):
    """Return liked songs that are not in the user's own playlists."""
    user_id = sp.current_user()["id"]

    liked_songs = paginate_spotify(sp.current_user_saved_tracks)
    liked_ids = {item['track']['id'] for item in liked_songs if item['track']}

    own_ids = set()
    playlists = paginate_spotify(sp.current_user_playlists)
    for playlist in playlists:
        if playlist['owner']['id'] != user_id:
            continue
        tracks = paginate_spotify(sp.playlist_tracks, playlist_id=playlist['id'])
        for item in tracks:
            track = item.get('track')
            if track:
                own_ids.add(track['id'])

    only_liked = liked_ids - own_ids
    # Return richer metadata for each liked song
    return [
        {
            "id": item['track']['id'],
            "name": item['track']['name'],
            "artists": [a['name'] for a in item['track']['artists']],
            "album": item['track']['album']['name'],
            "image": item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
        }
        for item in liked_songs if item['track']['id'] in only_liked
    ]

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
