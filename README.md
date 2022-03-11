# Databases-Python-Demo 

Adapted from [Databases-Java-Demo](https://github.com/ChristosHadjichristofi/Databases-Java-Demo) and [Databases-NodeJS-Demo](https://github.com/ChristosHadjichristofi/Databases-NodeJS-Demo), originally by [Christos Hadjichristofi](https://github.com/ChristosHadjichristofi).

## Dependencies

 - [Python](https://www.python.org/downloads/), with the additional libraries:
    - [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/)
    - [faker](https://faker.readthedocs.io/en/master/) (optional, for data generation)

(use pip3 install <module_name> to install directly, or create a virtual environment with the `venv` module)

## What does Flask do

Flask is a micro web framework used to create web applications. It uses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) as its templating engine, to generate static template files at runtime, and [Werkzeug](https://www.palletsprojects.com/p/werkzeug/) as its WSGI toolkit, to facilitate the communication between web server and application. When writing an app locally, Flask will launch a simple "development" server on which to run it.

## How to Execute SQL Queries with Python and Flask

In order to send queries to a database from a Python program, a connection between it and the databases' server must be established first. That is accomplished by a cursor object from the `Flask-MySQLdb` library, and using the appropriate methods (`execute`, `commit`).

## Project Structure

Generally, Flask allows some freedom of choice regarding the layout of the application's components. This demo follows the structure recommended by the [official documentation](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/), whereby a package, conventionally named "`flaskr`", contains the application's code and files, separated into folders for each category (models, controllers, HTML templates - views, static files such as css or images).

 - `__init__.py` configures the application, including the necessary information and credentials for the database
 - `routes.py` currently contains all the endpoints and corresponding controllers
 - `run.py` launches the simple, built-in server and runs the app on it

Run via the `flask run` command or `run.py`.

![landing](https://user-images.githubusercontent.com/40044042/156389573-9e6c1c3a-1488-4e39-913f-96dd11091adb.png)

![students](https://user-images.githubusercontent.com/40044042/156389596-a409b129-e9cb-4946-9d9d-47f113c1d8f3.png)

![grades](https://user-images.githubusercontent.com/40044042/156389628-1653aba7-c033-48d0-ac3a-df37374f0d1e.png)
