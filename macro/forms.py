"""Forms for the application."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import InputRequired


class UploadCsvForm(FlaskForm):
    """Class for CSV upload form."""

    csv_file = FileField(
        "CSV file",
        validators=[
            FileRequired(),
            FileAllowed(["csv"], "Invalid file type.")
        ],
    )
    submit = SubmitField("Upload")


class RunModelsForm(FlaskForm):
    """Class for models run form."""

    models = SelectMultipleField(
        "Select model(s)",
        validators=[InputRequired()],
        render_kw={"placeholder": "Select model(s)"},
    )
    submit = SubmitField("Run")
