from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class StudentForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Required field.")])

    surname = StringField(label = "Surname", validators = [DataRequired(message = "Required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Required field."), Email(message = "Invalid email format")])

    submit = SubmitField("Create")
