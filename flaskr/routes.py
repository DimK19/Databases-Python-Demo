import re
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from flaskr import app, db
from flaskr.forms import StudentForm

@app.route("/")
def index():
    try:
        ## create connection to database
        cur = db.connection.cursor()
        ## execute query
        cur.execute("SELECT g.grade, s.name, s.surname FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'DRI' ORDER BY g.grade DESC LIMIT 1")
        ## cursor.fetchone() does not return the column names, only the row values
        ## thus we manually create a mapping between the two, the dictionary res
        column_names = [i[0] for i in cur.description]
        res = dict(zip(column_names, cur.fetchone()))
        best_dribbling_grade = res.get("grade")
        best_dribbler = res.get("name") + " " + res.get("surname")

        cur.execute("SELECT g.grade, s.name, s.surname FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'SHO' ORDER BY g.grade DESC LIMIT 1")
        res = dict(zip(column_names, cur.fetchone()))
        cur.close()
        best_shooting_grade = res.get("grade")
        best_shooter = res.get("name") + " " + res.get("surname")

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
    """
    Retrieve students from database
    """
    try:
        form = StudentForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM students")
        column_names = [i[0] for i in cur.description]
        students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("students.html", students = students, pageTitle = "Students Page", form = form)
    except Exception as e:
        flash(str(e), "danger")
        abort(500)

@app.route("/students/create", methods = ["GET", "POST"]) ## "GET" by default
def createStudent():
    """
    Create new student in the database
    """
    form = StudentForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newStudent = form.__dict__
        query = "INSERT INTO students(name, surname, email) VALUES ('{}', '{}', '{}');".format(newStudent['name'].data, newStudent['surname'].data, newStudent['email'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Student inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_student.html", pageTitle = "Create Student", form = form)

@app.route("/students/update/<int:id>", methods = ["POST"])
def updateStudent(id):
    """
    Update a student in the database, by id
    """
    form = StudentForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE students SET name = '{}', surname = '{}', email = '{}' WHERE id = {};".format(updateData['name'].data, updateData['surname'].data, updateData['email'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Student updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getStudents"))

@app.route("/grades")
def getGrades():
    """
    Retrieve grades from database
    """
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM grades")
        column_names = [i[0] for i in cur.description]
        grades = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("grades.html", grades = grades, pageTitle = "Grades Page")
    except Exception as e:
        abort(500)
        print(e)

@app.route("/grades/delete/<int:id>", methods = ["POST"])
def deleteGrade(id):
    """
    Delete grade by id from database
    """
    query = f"DELETE FROM grades WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Grade deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getGrades"))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
