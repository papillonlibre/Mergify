# Mergify

## Application Goal
- leverage Spotify API to merge playlists together
## Important links
Can be accessed at: https://papillonlibre.github.io/Mergify/
The dashboard is at https://developer.spotify.com/dashboard

## Dependencies needed

- For Tailwind, to integrate with React, it is necessary to ensure that the following packages are installed through npm with the following command: `npm install tailwindcss postcss autoprefixer`. Run this command from within the mergify root folder.
    - For Tailwind, the command `npx tailwindcss init` creates `tailwind.config.js` in the project root. This file is what configures Tailwind CSS for the project overall.

## How to host Flask websites
https://github.com/orgs/community/discussions/68841


## Python virtual env
Command is venv\Scripts\activate on Windows to activate the venv

## Authorization Flow

For this project, I chose to implement the Authorization Code Flow for better security practice and longer lasting tokens. This flow was implemented with session cookies. This should allow the Spotify Authorization to be more secure and subscribe to best practices as opposed to Implicit Grant Flow. Therefore, here is the workflow of the implemented authorization flow implemented for Mergify.

