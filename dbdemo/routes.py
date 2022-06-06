from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import app, db ## initially created by __init__.py, need to be used here

@app.route("/")
def index():
    try:
        ## create connection to database
        cur = db.connection.cursor()
        ## execute query
        cur.execute("SELECT g.grade, s.first_name, s.last_name FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'DRI' ORDER BY g.grade DESC LIMIT 1")
        ## cursor.fetchone() does not return the column names, only the row values
        ## thus we manually create a mapping between the two, the dictionary res
        column_names = [i[0] for i in cur.description]
        res = dict(zip(column_names, cur.fetchone()))
        best_dribbling_grade = res.get("grade")
        best_dribbler = res.get("first_name") + " " + res.get("last_name")

        cur.execute("SELECT g.grade, s.first_name, s.last_name FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'SHO' ORDER BY g.grade DESC LIMIT 1")
        res = dict(zip(column_names, cur.fetchone()))
        cur.close()
        best_shooting_grade = res.get("grade")
        best_shooter = res.get("first_name") + " " + res.get("last_name")

        return render_template("landing.html",
                               pageTitle = "Landing Page",
                               best_dribbling_grade = best_dribbling_grade,
                               best_dribbler = best_dribbler,
                               best_shooting_grade = best_shooting_grade,
                               best_shooter = best_shooter)
    except Exception as e:
        print(e)
        return render_template("landing.html", pageTitle = "Landing Page")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
