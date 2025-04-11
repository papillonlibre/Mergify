import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SpotifyAuth from '../components/SpotifyAuth';
import { getSpotifyAuthUrl } from '../utils/spotifyAuthLogic';

jest.mock('../utils/spotifyAuthLogic', () => ({
  getSpotifyAuthUrl: jest.fn(),
  getTokenFromUrl: jest.fn(() => null),
  
}));

describe('SpotifyAuth Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    getSpotifyAuthUrl.mockReturnValue('https://mocked-auth-url.com');
    // Mock window.location.assign using Object.defineProperty to avoid read-only issue with Jest
    Object.defineProperty(window, 'location', {
        value: { assign: jest.fn() },
        writable: true,
    });
  });

  test('renders the login button', () => {
    render(<SpotifyAuth />);
    const loginButton = screen.getByText(/Login to Spotify/i);
    expect(loginButton).toBeInTheDocument();
  });

  test('clicking login button redirects to Spotify auth URL', () => {
    render(<SpotifyAuth />);
    const loginButton = screen.getByText(/Login to Spotify/i);
    expect(getSpotifyAuthUrl).toHaveBeenCalledTimes(0);  // It shouldn't be called yet

    fireEvent.click(loginButton);
    expect(getSpotifyAuthUrl).toHaveBeenCalledTimes(1); // Should be called once

    // Log the URL to ensure it's correct
    console.log(getSpotifyAuthUrl());  // Should log 'https://mocked-auth-url.com'
    // Check that window.location.assign is called with the correct URL
    expect(window.location.assign).toHaveBeenCalledWith('https://mocked-auth-url.com');
  });

  test('does not show login button when token is present', () => {
    // Mock localStorage to have a token
    Storage.prototype.getItem = jest.fn(() => 'mocked-token');
    render(<SpotifyAuth />);

    const loginButton = screen.queryByText(/Login to Spotify/i);
    expect(loginButton).not.toBeInTheDocument();
  });
});
