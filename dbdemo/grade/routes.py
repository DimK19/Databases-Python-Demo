from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import db ## initially created by __init__.py, needs to be used here
from dbdemo.grade import grade
from dbdemo.grade.forms import GradeForm

@grade.route("/grades")
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

@grade.route("/grades/delete/<int:gradeID>", methods = ["POST"])
def deleteGrade(gradeID):
    """
    Delete grade by id from database
    """
    query = f"DELETE FROM grades WHERE id = {gradeID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Grade deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("grade.getGrades"))

@grade.route("/grades/create", methods = ["GET", "POST"]) ## "GET" by default
def createGrade():
    """
    Create new grade in the database
    """
    form = GradeForm() ## This is an object of a class that inherits FlaskForm
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
    if(request.method == "POST"):
        newGrade = form.__dict__

        query = "INSERT INTO grades(course_name, grade, student_id) VALUES ('{}', '{}', '{}');".format(
            newGrade['course_name'].data,
            newGrade['grade'].data,
            newGrade['student_id'].data
        )

        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Grade inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            print(str(e))
    ## else, response for GET request
    else:
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT id, CONCAT(last_name, ", ", first_name) FROM students;')
            form.student_id.choices = list(cur.fetchall())
            ## each tuple in the above list is in the format (id, full name),
            ## and will be rendered in html as an <option> of the <select>
            ## element, with value = id and content = full_name
            cur.close()
            return render_template("create_grade.html", pageTitle = "Create Grade", form = form)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
