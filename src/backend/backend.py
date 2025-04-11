import spotipy
from spotipy.oauth2 import SpotifyOAuth

def authentication_manager():
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                               redirect_uri="https://papillonlibre.github.io/Mergify/",
                                               scope=scope, 
                                               ))

if __name__=="__main__":
    authentication_manager()