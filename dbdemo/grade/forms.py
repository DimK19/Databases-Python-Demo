from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

class GradeForm(FlaskForm):
    student_id = SelectField(
        label = "Student",
        validators = [DataRequired(message = "Student is a required field.")],
        coerce = int
    )
    grade = IntegerField(
        label = "Grade",
        validators = [NumberRange(min = 0, max = 100, message = "Grade between 0 and 100 inclusive.")]
    )

    ## In a real scenario, where the courses would be a separate entity, the
    ## choices list below would be populated by the corresponding data
    ## retrieved from the database. See createGrade in routes.py for an example
    ## of this with student_id
    course_name = SelectField(
        label = "Course",
        validators = [DataRequired(message = "Course is a required field.")],
        choices = ["PAC", "PAS", "SHO", "DRI", "DEF", "PHY"]
    )

    submit = SubmitField("Create")
