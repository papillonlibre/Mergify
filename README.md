# Mergify
Welcome to Mergify, a web app built on React that leverages the Spotify API to allow users to perform some advanced funcionality not natively supported in Spotify such as : merge multiple playlists together, indicate playlists that only appear in one playlist, and more! This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Important links
The app deployment can be accessed at: https://papillonlibre.github.io/Mergify/
The developer dashboard is at https://developer.spotify.com/dashboard if you have the right credentials.

## Dependencies needed

- For Tailwind, to integrate with React, it is necessary to ensure that the following packages are installed through npm with the following command: `npm install tailwindcss postcss autoprefixer`. Run this command from within the mergify root folder.
    - For Tailwind, the command `npx tailwindcss init -p` creates `tailwind.config.js` in the project root. This file is what configures Tailwind CSS for the project overall.

## How to host Flask websites
https://github.com/orgs/community/discussions/68841


## Python virtual env

Steps to create the virtual env
- `pip install virtualenv`
- `virtualenv venv`
- activate the venv
- `pip install -r requirements.txt`
Command is `venv\Scripts\activate` on Windows to activate the venv from within the `mergify\src\backend` folder.

## Starting the Flask Server
From the `mergify\src\backend` folder, assuming the virtual environment is activated as described in Python virtual env, `python .\app.py` will run the Flask server.

## Authorization Flow

For this project, I chose to implement the Authorization Code Flow for better security practice and longer lasting tokens. This flow was implemented with session cookies. This should allow the Spotify Authorization to be more secure and subscribe to best practices as opposed to Implicit Grant Flow. The basis of this implementation (conducted on a Flask Python server on the backend) was based on the [Spotify example flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow).Therefore, here is the workflow of the implemented authorization flow implemented for Mergify.

1. User visits https://papillonlibre.github.io/Mergify/
2. User clicks “Login to Spotify”  Button → redirects to Flask backend: https://your-flask-api.com/login TODO Once backend is hosted, update this comment
3. Flask redirects to Spotify login
4. After auth, Spotify redirects to: https://papillonlibre.github.io/Mergify/#/callback?code=...
5. Callback.js exchanges code with Flask backend: POST https://your-flask-api.com/callback TODO Once backend is hosted, update this comment
6. React saves access token and routes to /#/dashboard

This works because GitHub Pages handles my static files, HashRouter avoids 404s associated with the fact that GitHub Pages cannot handle Browser Router, and Flask runs separately and securely manages client secrets. 


## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
