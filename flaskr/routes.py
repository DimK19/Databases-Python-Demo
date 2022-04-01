import re
from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from flaskr import app, db

@app.route("/")
def index():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT g.grade, s.name, s.surname FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'DRI' ORDER BY g.grade DESC LIMIT 1")
        column_names = [i[0] for i in cur.description]
        res = dict(zip(column_names, cur.fetchone()))
        best_dribbling_grade = res.get("grade")
        best_dribbler = res.get("name") + " " + res.get("surname")

        cur.execute("SELECT g.grade, s.name, s.surname FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'SHO' ORDER BY g.grade DESC LIMIT 1")
        res = dict(zip(column_names, cur.fetchone()))
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
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM students")
        column_names = [i[0] for i in cur.description]
        students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("students.html", students = students, pageTitle = "Students Page")
    except Exception as e:
        flash(str(e), "danger")
        abort(500)

@app.route("/students/create", methods = ["GET", "POST"]) ## "GET" by default
def createStudent():
    if(request.method == "POST"):
        newStudent = request.form
        messages = validateStudent(newStudent)
        if(not messages):
            query = "INSERT INTO students(name, surname, email) VALUES ('{}', '{}', '{}');".format(newStudent['name'], newStudent['surname'], newStudent['email'])
            try:
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                cur.close()
                flash("Student inserted successfully", "success")
                return redirect(url_for("index"))
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
        else:
            for m in messages:
                flash(m, "danger")

    ## else, response for GET request
    return render_template("create_student.html", pageTitle = "Create Student")

def validateStudent(student):
    """
    Return a list of error messages. If empty, the data inserted is valid.
    """
    MESSAGE_REQUIRED_NAME = "Name is a required field"
    MESSAGE_REQUIRED_SURNAME = "Surname is a required field"
    MESSAGE_REQUIRED_EMAIL = "Email is a required field"
    MESSAGE_INVALID_EMAIL = "Invalid email format"
    messages = []
    if(not student["name"]):
        messages.append(MESSAGE_REQUIRED_NAME)
    if(not student["surname"]):
        messages.append(MESSAGE_REQUIRED_SURNAME)
    if(not student["email"]):
        messages.append(MESSAGE_REQUIRED_EMAIL)
    elif(not re.fullmatch(r"\w+@\w+(\.\w+)+", student["email"])):
        ## https://docs.python.org/3/library/re.html#re.fullmatch
        messages.append(MESSAGE_INVALID_EMAIL)

    return messages

@app.route("/students/update/<int:id>", methods = ["POST"])
def updateStudent(id):
    updateData = request.form
    messages = validateStudent(updateData)
    if(not messages):
        query = "UPDATE students SET name = '{}', surname = '{}', email = '{}' WHERE id = {};".format(updateData['name'], updateData['surname'], updateData['email'], id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Student updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for m in messages:
            flash(m, "danger")
    return redirect(url_for("getStudents"))

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
        abort(500)
        print(e)

@app.route("/grades/delete/<int:id>", methods = ["POST"])
def deleteGrade(id):
    updateData = request.form
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
