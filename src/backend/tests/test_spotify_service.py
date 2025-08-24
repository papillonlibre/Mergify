import unittest
from unittest.mock import MagicMock
from backend.spotify_service import (
    get_user_playlists,
    get_liked_exclusive_songs,
    fetch_top_artists
)

class TestSpotifyService(unittest.TestCase):

    def test_get_user_playlists_returns_names(self):
        sp = MagicMock()
        sp.current_user_playlists.return_value = {
            "items": [{"name": "Playlist A"}, {"name": "Playlist B"}]
        }
        playlists = get_user_playlists(sp)
        self.assertEqual(playlists, ["Playlist A", "Playlist B"])
        
    def test_get_user_playlists_returns_names_none(self):
        sp = MagicMock()
        sp.current_user_playlists.return_value = {"items": []}
        playlists = get_user_playlists(sp)
        self.assertEqual(playlists, [])


    def test_get_liked_exclusive_songs(self):
        sp = MagicMock()
        sp.current_user.return_value = {"id": "user123"}

        # Fake liked songs
        sp.current_user_saved_tracks.side_effect = [
            {"items": [{"track": {"id": "t1", "name": "Song A"}}]},
            {"items": []},
        ]

        # Fake playlists owned by user
        sp.current_user_playlists.side_effect = [
            {"items": [{"id": "pl1", "owner": {"id": "user123"}}]},
            {"items": []},
        ]

        # Fake tracks in that playlist
        sp.playlist_tracks.side_effect = [
            {"items": [{"track": {"id": "t2", "name": "Song B"}}]},
            {"items": []},
        ]

        songs = get_liked_exclusive_songs(sp)
        self.assertEqual(songs, ["Song A"])

    def test_fetch_top_artists_simple(self):
        sp = MagicMock()
        sp.current_user_top_artists.return_value = {
            "items": [
                {"name": "Artist A", "genres": ["rock"], "images": [{"url": "imgA"}]},
                {"name": "Artist B", "genres": ["pop"], "images": [{"url": "imgB"}]},
            ]
        }
        result = fetch_top_artists(sp, requested_range="short_term", limit=2, simple=True)
        self.assertIn("short_term", result)
        self.assertEqual(result["short_term"], ["Artist A", "Artist B"])

    def test_fetch_top_artists_detailed(self):
        sp = MagicMock()
        sp.current_user_top_artists.return_value = {
            "items": [
                {"name": "Artist A", "genres": ["rock"], "images": [{"url": "imgA"}]},
            ]
        }
        result = fetch_top_artists(sp, requested_range="short_term", limit=1, simple=False)
        self.assertEqual(result["short_term"][0]["name"], "Artist A")
        self.assertIn("genres", result["short_term"][0])
        self.assertIn("image", result["short_term"][0])

    def test_fetch_top_artists_invalid_range(self):
        sp = MagicMock()
        with self.assertRaises(ValueError):
            fetch_top_artists(sp, requested_range="invalid")

if __name__ == "__main__":
    unittest.main()
