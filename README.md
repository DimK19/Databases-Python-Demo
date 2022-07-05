# Databases-Python-Demo

Adapted from [Databases-Java-Demo](https://github.com/ChristosHadjichristofi/Databases-Java-Demo) and [Databases-NodeJS-Demo](https://github.com/ChristosHadjichristofi/Databases-NodeJS-Demo), originally by [Christos Hadjichristofi](https://github.com/ChristosHadjichristofi).

Implementation in PHP [here](https://github.com/cpefkianakis/Databases-PHP-Demo).

## Dependencies

 - [MySQL](https://www.mysql.com/) for Windows
 - [Python](https://www.python.org/downloads/), with the additional libraries:
    - [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    - [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/)
    - [faker](https://faker.readthedocs.io/en/master/) (for data generation)
    - [Flask-WTForms](https://flask-wtf.readthedocs.io/en/1.0.x/) and [email-validator](https://pypi.org/project/email-validator/) (a more involved method of input validation)

Use `pip3 install <package_name>` to install each individual Python package (library) directly for the entire system, or create a virtual environment with the [`venv`](https://docs.python.org/3/library/venv.html) module. The necessary packages for this app are listed in `requirements.txt` and can be installed all together via `pip install -r requirements.txt`.

## What does Flask do

Flask is a micro web framework used to create web applications. It uses [Jinja](https://jinja.palletsprojects.com/en/3.0.x/) as its templating engine, to generate static template files at runtime, and [Werkzeug](https://www.palletsprojects.com/p/werkzeug/) as its WSGI toolkit, to facilitate the communication between web server and application. When writing an app locally, Flask will launch a simple "development" server on which to run it.

## How to Execute SQL Queries with Python and Flask

In order to send queries to a database from a Python program, a connection between it and the databases' server must be established first. That is accomplished by a cursor object from the `Flask-MySQLdb` library, and using the appropriate methods (`execute`, `commit`).

## Flask-WTForms

This package integrates the [WTForms](https://wtforms.readthedocs.io/en/3.0.x/) library with Flask. WTForms is used for secure input (form) validation and form rendering inside the templates. It provides security features such as [CSRF protection](https://en.wikipedia.org/wiki/Cross-site_request_forgery). Each field of a `FlaskForm` class is essentially rendered as the corresponding input tag in HTML.

## Project Structure

Generally, Flask allows some freedom of choice regarding the layout of the application's components. This demo follows the structure recommended by the [official documentation](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/), whereby a package, arbitrarily named "`dbdemo`", contains the application's code and files, separated into folders for each category (models, controllers, HTML templates - views, static files such as css or images).

Additionally, it utilizes Blueprints, a Flask structure that divides the app into sub-modules. Each of those is supposed to represent an entity of the database, and contains its own __init__ file, and corresponding form and route declarations.

 - `__init__.py` configures the application, including the necessary information and credentials for the database
 - Each module folder contains:
    - an `__init__` file that initializes the Blueprint
    - a `routes.py` file with the relevant endpoints and corresponding controllers
 - `run.py` launches the simple, built-in server and runs the app on it
 - all HTML templates are stored together in the `templates` folder, but could also be separated per Blueprint

Run via the `flask run` command (set the environment variable `FLASK_APP` to `run.py`) or directly with `run.py`.

_The demo's toy database is created and populated by_ `db-project-demo.sql`.

## Good Practices

 1. Never upload passwords or API keys to github. One simple way to secure your passwords is to store them in a separate file, that will be included in `.gitignore`:

    _dbdemo/config.json_
    ```json
    {
        "MYSQL_USER": "dbuser",
        "MYSQL_PASSWORD": "dbpass",
        "MYSQL_DB": "dbname",
        "MYSQL_HOST": "localhost",
        "SECRET_KEY": "key",
        "WTF_CSRF_SECRET_KEY": "key"
    }
    ```
    Import the credentials in `__init__.py` by replacing the `app.config` commands with:
    ```python
    import json
    ## ...
    app.config.from_file("config.json", load = json.load)
    ```
    
## Note for Linux users

Applications that run without `sudo` privileges often are not allowed to connect to MySQL with the _root_ user. In order to overcome this problem, you should create a new MySQL user an grant him privileges for this demo application. Follow these steps:

1. Open a terminal and precede the `mysql` command with `sudo` to invoke it with the privileges of the root Ubuntu user in order to gain access to the root MySQL user. This can be done using  
`sudo mysql -u root -p`.
2. Create a new MySQL user using:  
`mysql> CREATE USER 'type_username'@'localhost' IDENTIFIED BY 'type_your_password_here_123';`
3. Grant the user root privileges on the application's database using:  
`mysql> GRANT ALL PRIVILEGES ON demo.* TO 'type_username'@'localhost' WITH GRANT OPTION;`
4. Reload the grant tables to ensure that the new privileges are put into effect using:
`FLUSH PRIVILEGES;`.
5. Exit MySQL with `mysql> exit;`.
7. Go to `dbdemo/__init__.py` and change the `app.config["MYSQL_USER"]` and `app.config["MYSQL_PASSWORD"]` lines according to the username and the password you chose before.

For more details read [this](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql).
    
## Screenshots

![landing](https://user-images.githubusercontent.com/40044042/156389573-9e6c1c3a-1488-4e39-913f-96dd11091adb.png)

![students](https://user-images.githubusercontent.com/40044042/156389596-a409b129-e9cb-4946-9d9d-47f113c1d8f3.png)

![grades](https://user-images.githubusercontent.com/40044042/156389628-1653aba7-c033-48d0-ac3a-df37374f0d1e.png)
