from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class TaskAddForm(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()])
    user_email = StringField("User email", validators=[DataRequired(), Email()])
    text = StringField("Task", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("Add task")


class TaskEditForm(TaskAddForm):
    is_completed = BooleanField("Task completed")
    submit = SubmitField("Edit task")


class TaskDropForm(TaskEditForm):
    confirm_deletion = BooleanField("Confirm deletion")
    submit = SubmitField("Delete task")
