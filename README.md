# Databases-Python-Demo 

Adapted from [Databases-Java-Demo](https://github.com/ChristosHadjichristofi/Databases-Java-Demo) and [Databases-NodeJS-Demo](https://github.com/ChristosHadjichristofi/Databases-NodeJS-Demo), originally by [Christos Hadjichristofi](https://github.com/ChristosHadjichristofi).

## Dependencies

 - [MySQL](https://www.mysql.com/) for Windows
 - [Python](https://www.python.org/downloads/), with the additional libraries:
    - [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/)
    - [faker](https://faker.readthedocs.io/en/master/) (optional, for data generation)
    - [Flask-WTForms](https://flask-wtf.readthedocs.io/en/1.0.x/) and [email-validator](https://pypi.org/project/email-validator/) (optional, a more involved method of input validation)

(use `pip3 install <module_name>` to install directly, or create a virtual environment with the `venv` module)

## What does Flask do

Flask is a micro web framework used to create web applications. It uses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) as its templating engine, to generate static template files at runtime, and [Werkzeug](https://www.palletsprojects.com/p/werkzeug/) as its WSGI toolkit, to facilitate the communication between web server and application. When writing an app locally, Flask will launch a simple "development" server on which to run it.

## How to Execute SQL Queries with Python and Flask

In order to send queries to a database from a Python program, a connection between it and the databases' server must be established first. That is accomplished by a cursor object from the `Flask-MySQLdb` library, and using the appropriate methods (`execute`, `commit`).

## Flask-WTForms

This package integrates the [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) library with Flask. WTForms is used for secure input (form) validation and form rendering inside the templates. Each field of a FlaskForm class is essentially rendered as the corresponding input tag in HTML.

_For the purposes of this project, simple HTML forms with custom validation by the controllers are sufficient: see [v1.0.0](https://github.com/DimK19/Databases-Python-Demo/releases/tag/v1.0.0-alpha)._

## Project Structure

Generally, Flask allows some freedom of choice regarding the layout of the application's components. This demo follows the structure recommended by the [official documentation](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/), whereby a package, conventionally named "`flaskr`", contains the application's code and files, separated into folders for each category (models, controllers, HTML templates - views, static files such as css or images).

 - `__init__.py` configures the application, including the necessary information and credentials for the database
 - `routes.py` currently contains all the endpoints and corresponding controllers
 - `run.py` launches the simple, built-in server and runs the app on it

Run via the `flask run` command (set the environment variable `FLASK_APP` to `run.py`) or directly with `run.py`.

![landing](https://user-images.githubusercontent.com/40044042/156389573-9e6c1c3a-1488-4e39-913f-96dd11091adb.png)

![students](https://user-images.githubusercontent.com/40044042/156389596-a409b129-e9cb-4946-9d9d-47f113c1d8f3.png)

![grades](https://user-images.githubusercontent.com/40044042/156389628-1653aba7-c033-48d0-ac3a-df37374f0d1e.png)
