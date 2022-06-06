from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, need to be used here
from dbdemo.student.forms import StudentForm
from dbdemo.student import student

@student.route("/students")
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
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@student.route("/students/create", methods = ["GET", "POST"]) ## "GET" by default
def createStudent():
    """
    Create new student in the database
    """
    form = StudentForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain user input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newStudent = form.__dict__
        query = "INSERT INTO students(first_name, last_name, email) VALUES ('{}', '{}', '{}');".format(newStudent['first_name'].data, newStudent['last_name'].data, newStudent['email'].data)
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

@student.route("/students/update/<int:studentID>", methods = ["POST"])
def updateStudent(studentID):
    """
    Update a student in the database, by id
    """
    form = StudentForm() ## see createStudent for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE students SET first_name = '{}', last_name = '{}', email = '{}' WHERE id = {};".format(updateData['first_name'].data, updateData['last_name'].data, updateData['email'].data, studentID)
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
    return redirect(url_for("student.getStudents"))

@student.route("/students/delete/<int:studentID>", methods = ["POST"])
def deleteStudent(studentID):
    """
    Delete student by id from database
    """
    query = f"DELETE FROM students WHERE id = {studentID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Student deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("student.getStudents"))
