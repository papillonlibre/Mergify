const CLIENT_ID = '141d8896106f454abbf04bb2c5789ab4';
// const REDIRECT_URI = 'https://papillonlibre.github.io/Mergify/#/callback';
const REDIRECT_URI = 'http://localhost:3000/Mergify/callback';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';
const SCOPES = [
  'user-read-private',
  'playlist-read-private',
  'playlist-modify-private',
  'playlist-modify-public'
];

export const getSpotifyAuthUrl = () => {
  return `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&response_type=code&redirect_uri=${encodeURIComponent(
    REDIRECT_URI
  )}&response_type=${RESPONSE_TYPE}&scope=${encodeURIComponent(SCOPES.join(' '))}`;
};
