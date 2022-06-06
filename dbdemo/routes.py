from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import app, db ## initially created by __init__.py, need to be used here
from dbdemo.forms import StudentForm, GradeForm

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
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/students/create", methods = ["GET", "POST"]) ## "GET" by default
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

@app.route("/students/update/<int:studentID>", methods = ["POST"])
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
    return redirect(url_for("getStudents"))

@app.route("/students/delete/<int:studentID>", methods = ["POST"])
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

@app.route("/grades/delete/<int:gradeID>", methods = ["POST"])
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
    return redirect(url_for("getGrades"))

@app.route("/grades/create", methods = ["GET", "POST"]) ## "GET" by default
def createGrade():
    """
    Create new grade in the database
    """
    form  = GradeForm()

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
            ## each tuple in the above list is in the format (id, full__name),
            ## and will be rendered in html as an <option> of the <select>
            ## element, with value = id and content = full_name
            cur.close()
            return render_template("create_grade.html", pageTitle = "Create Grade", form = form)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
