from flask import Flask
from flask import render_template
from flask import request
from flask_mysqldb import MySQL
from flaskr import app, db

@app.route("/")
def index():
    print("what")
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM grades, students WHERE course_name = 'DRI' AND grades.student_id = students.id ORDER BY grade DESC LIMIT 1")
        column_names = [i[0] for i in cur.description]
        res = dict(zip(column_names, cur.fetchone()))
        best_dribbling_grade = res.get("grade")
        best_dribbler = res.get("name") + " " + res.get("surname")

        cur.execute("SELECT * FROM grades, students WHERE course_name = 'SHO' AND grades.student_id = students.id ORDER BY grade DESC LIMIT 1")
        res = dict(zip(column_names, cur.fetchone()))
        best_shooting_grade = res.get("grade")
        best_shooter = res.get("name") + " " + res.get("surname")

        print(best_dribbler)
        print(best_shooter)
        return render_template("landing.html",
                               pageTitle = "Landing Page",
                               best_dribbling_grade = best_dribbling_grade,
                               best_dribbler = best_dribbler,
                               best_shooting_grade = best_shooting_grade,
                               best_shooter = best_shooter)
    except Exception as e:
        print(e)
        return render_template("landing.html", pageTitle = "Landing Page")


@app.route("/students")
def getStudents():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM students")
        column_names = [i[0] for i in cur.description]
        students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("students.html", students = students, pageTitle = "Students Page")
    except Exception as e:
        print(e)

@app.route("/grades")
def getGrades():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM grades")
        column_names = [i[0] for i in cur.description]
        grades = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("grades.html", grades = grades, pageTitle = "Grades Page")
    except Exception as e:
        print(e)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html", pageTitle = "Not Found"), 404
