"""Forms for the application."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField


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


class RunModelForm(FlaskForm):
    """Class for model run form."""

    # model =
    submit = SubmitField("Run")
