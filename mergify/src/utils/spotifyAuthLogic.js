const CLIENT_ID = '141d8896106f454abbf04bb2c5789ab4';
const REDIRECT_URI = 'https://papillonlibre.github.io/Mergify/callback/';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';
const SCOPES = [
  'user-read-private',
  'playlist-read-private',
  'playlist-modify-private',
  'playlist-modify-public'
];

export const getSpotifyAuthUrl = () => {
  return `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(
    REDIRECT_URI
  )}&response_type=${RESPONSE_TYPE}&scope=${encodeURIComponent(SCOPES.join(' '))}`;
};

export const getTokenFromUrl = () => {
  const hash = window.location.hash;
  if (!hash) return null;

  const token = hash.substring(1).split('&').find((elem) => elem.startsWith('access_token'))?.split('=')[1];
  window.location.hash = ''; // Clear the hash
  return token;
};
