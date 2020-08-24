from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField,TextField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    # first_name = StringField('(Optional) First Name')
    # last_name = StringField('(Optional) Last Name')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditForm(FlaskForm):
    """ Edit form for users """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    first_name = StringField('(Optional) First Name')
    last_name = StringField('(Optional) Last Name')

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""

class EditNotesForm(FlaskForm):
    """Edit form -- this form is intentionally blank."""
    notes= StringField('edit_notes', validators=[DataRequired()])