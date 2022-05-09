from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class StudentForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    surname = StringField(label = "Surname", validators = [DataRequired(message = "Surname is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    submit = SubmitField("Create")
