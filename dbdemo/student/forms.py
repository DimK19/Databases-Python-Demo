from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class StudentForm(FlaskForm):
    first_name = StringField(label = "First name", validators = [DataRequired(message = "First name is a required field.")])

    last_name = StringField(label = "Last name", validators = [DataRequired(message = "Last name is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    submit = SubmitField("Create")
