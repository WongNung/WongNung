# WongNung - a Group-based Film Review and Discovery Web Application
***Website retired, due to lack of funds.***

[![Code linting](https://github.com/WongNung/WongNung/actions/workflows/linting.yml/badge.svg)](https://github.com/WongNung/WongNung/actions/workflows/linting.yml)
[![Unit testing](https://github.com/WongNung/WongNung/actions/workflows/testing.yml/badge.svg)](https://github.com/WongNung/WongNung/actions/workflows/testing.yml)
[![codecov](https://codecov.io/gh/WongNung/WongNung/branch/master/graph/badge.svg?token=XICO479LGZ)](https://codecov.io/gh/WongNung/WongNung)

## What is WongNung?
**TL;DR: It's IMDB + Reddit**

“WongNung” is a community-driven review-aggregation web application for film where users can read, post reviews for film and discover groups of users (called Fandom) with similar film preferences. Users can also join those Fandoms to discover films that are reviewed by the members and keep themselves personalized to their film preferences.

<!-- Reserved for putting in installation + running the application -->
# Installation
Before you install, see the [Preparing the installation](#preparing-the-installation) for more details on what to do, after that you may choose either installation with [Docker](#install-with-docker-recommended) or installation by [yourself from source](#install-from-source). **It is HIGHLY recommended to use Docker.**

## Preparing the installation
0. Have the following requirements ready:
   * [TMDB API Key](https://www.themoviedb.org/documentation/api)
   
   Any of:
   * [Google OAuth Key + Secret](https://support.google.com/cloud/answer/6158849)
   * [Github OAuth Key + Secret](https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app)
   * [Discord OAuth Key + Secret](https://discord.com/developers/docs/topics/oauth2)

1. Clone this repository into a destination folder of your choice.
   ```sh
   git clone https://github.com/WongNung/WongNung.git WongNung
   cd WongNung
   ```

2. Copy the `.env.example` to `.env` and edit the values inside the file.
   
   List of environment variables:
   |    Variable     | Description                                                                                                                                       |
   | :-------------: | :------------------------------------------------------------------------------------------------------------------------------------------------ |
   |  `SECRET_KEY`   | Secret key for Django (See `.env` on how to get it)                                                                                               |
   | `TMDB_API_KEY`  | TMDB API key, you can have it easily by going to their [site](https://www.themoviedb.org/documentation/api).                                      |
   |     `DEBUG`     | You can either set this to True or False, True will run the server in development, False will be suitable for production.                         |
   | `ALLOWED_HOSTS` | **This is important when DEBUG=False.** When running server on production, you can control which hosts are allowed to visit endpoints of the app. |
   |    `APP_TZ`     | Sets the timezone of the application. **Recommended to leave as UTC.**                                                                            |
   |  `DATABASE_*`   | Settings for your PostgreSQL connection. **If you're installing with Docker, you should change only the PASSWORD.**                               |
   | `NPM_BIN_PATH`  | The full path to `npm`. **If you're installing from source, you need to change this.**                                                            |
   |     `HTTPS`     | **This is ignored when DEBUG=True.** If you're running the server on HTTPS, this should be changed.                                               |

3. Copy the `oauth-credentials.json.example` to `oauth-credentials.json` and edit add values to the file.
   
   For each OAuth key and secret you have, add them to the respective lines.
   It is not required to have every OAuth provider filled.
   
    Example:
   ```json
   {
    "github": {
      "client_id": "AAAAABBBBBCCCCCDDDDD",
      "secret": "AAAAABBBBBCCCCCDDDDDAAAAABBBBBCCCCCDDDDD"
    }
   }
   ```

## Install with Docker (recommended)
**We do not distribute our own Docker images.**

0. Make sure you have installed [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
   
   *Note: The two are likely bundled together in Docker Desktop. For Linux, read their [installation docs](https://docs.docker.com/compose/install/) for more information.*

1. You can build and start the application by,
   ```sh
   docker compose up -d --build
   ```

   * `up` is a command for Docker Compose. It will create containers and start them.
   * `-d` is an option for `up`. This tells Docker to detach from command line on start.
   * `--build` is an option for `up`. This tells Docker to build an image from the Dockerfile before creating containers.

2. You can now visit the application by going to `localhost:8000` in your browser.

3. **(Optional, but recommended)** You should create an admin account in the application,
   ```sh
   docker exec -it wongnung-app-1 /bin/bash
   ...
   python manage.py createsuperuser
   exit
   ```

**For further work with Docker installation, see [Maintenance with Docker](https://github.com/WongNung/WongNung/wiki/Maintenance-with-Docker).**

## Install from source
0. Make sure you have the following software/tools installed:
   * `Python` version 3.9 or greater
   * `Node.js` version 16 or greater
   * `PostgreSQL` server and client version 14
      * For Windows and Mac, the server and client is already bundled together.
      * For Linux, install `postgresql` and `postgresql-client`.

   If you will be running on production (`DEBUG=False`), there are additional tools required:
   * `gcc`
   * `Python headers` usually in `python3-dev` package
   * `libpq-dev`

1. Make sure your connection to PostgreSQL (using credentials in `.env`) works, usually you will need to modify `pg_hba.conf`

2. Navigate to `theme` and install node dependencies.
   ```sh
   cd theme/static_src
   npm install
   cd ../..  # Navigate back to main folder
   ```

3. Create a virtual environment in the main folder and install Python dependencies.
   ```sh
   python -m venv venv
   source ./venv/bin/activate  # or Windows: ./venv/Scripts/activate

   pip install -r requirements.txt

   # or if you run in production
   pip install -r requirements/prod.txt
   ```

4. Migrate to database with:
   ```sh
   python manage.py migrate
   python manage.py createcachetable
   ```

   **(Optional, but recommended)** You should create an admin account in the application.
   ```sh
   python manage.py createsuperuser
   ```

5. Choose either:
   * Run on development (`DEBUG=True`), open two terminal windows and each type different commands:
     ```sh
     python manage.py tailwind start
     python manage.py runserver 0.0.0.0:8000
     ```
   * Run on production (`DEBUG=False`), run the following commands,
     ```sh
     python manage.py collectstatic
     python manage.py runserver 0.0.0.0:8000
     ```

# Project Documents
* [Wiki Home](https://github.com/WongNung/WongNung/wiki)
* [Vision Statement](https://github.com/WongNung/WongNung/wiki/Vision-Statement)
* [Requirements](https://github.com/WongNung/WongNung/wiki/Requirements)
* [Task Board](https://trello.com/b/Wpyr4LHZ/wongnung)
