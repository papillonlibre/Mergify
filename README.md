# Mergify
Welcome to Mergify, a web app built on React that leverages the Spotify API to allow users to perform some advanced funcionality not natively supported in Spotify such as : merge multiple playlists together, indicate playlists that only appear in one playlist, and more!

## Important links
The app deployment can be accessed at: https://papillonlibre.github.io/Mergify/
The developer dashboard is at https://developer.spotify.com/dashboard if you have the right credentials.

## Dependencies needed

- For Tailwind, to integrate with React, it is necessary to ensure that the following packages are installed through npm with the following command: `npm install tailwindcss postcss autoprefixer`. Run this command from within the mergify root folder.
    - For Tailwind, the command `npx tailwindcss init` creates `tailwind.config.js` in the project root. This file is what configures Tailwind CSS for the project overall.

## How to host Flask websites
https://github.com/orgs/community/discussions/68841


## Python virtual env
Command is `venv\Scripts\activate` on Windows to activate the venv from within the `mergify\src\backend` folder.
From there, python `.\app.py` will run the Flask server.

## Authorization Flow

For this project, I chose to implement the Authorization Code Flow for better security practice and longer lasting tokens. This flow was implemented with session cookies. This should allow the Spotify Authorization to be more secure and subscribe to best practices as opposed to Implicit Grant Flow. Therefore, here is the workflow of the implemented authorization flow implemented for Mergify.

1. User visits https://papillonlibre.github.io/Mergify/
2. User clicks “Login to Spotify”  Button → redirects to Flask backend: https://your-flask-api.com/login TODO Once backend is hosted, update this comment
3. Flask redirects to Spotify login
4. After auth, Spotify redirects to: https://papillonlibre.github.io/Mergify/#/callback?code=...
5. Callback.js exchanges code with Flask backend: POST https://your-flask-api.com/callback TODO Once backend is hosted, update this comment
6. React saves access token and routes to /#/dashboard

This works because GitHub Pages handles my static files, HashRouter avoids 404s associated with the fact that GitHub Pages cannot handle Browser Router, and Flask runs separately and securely manages client secrets. 