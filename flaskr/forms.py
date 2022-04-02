from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class StudentForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    surname = StringField(label = "Surname", validators = [DataRequired(message = "Surname is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    submit = SubmitField("Create")
