"""Views for the application."""

from io import StringIO

import pandas as pd
from flask import flash, redirect, render_template, session, url_for

from .forms import RunModelsForm, UploadCsvForm
from .main import app
from .utils import check_data_found


__all__ = ["index", "upload_data", "view_data", "run_models"]


# 404 ERROR HANDLING
@app.errorhandler(404)
def page_not_found(error):
    """Route for 404 response."""
    return render_template("404.html")


@app.route("/")
def index():
    """Route for homepage."""
    return render_template("index.html")


@app.route("/upload-data", methods=["GET", "POST"])
def upload_data():
    """Route for data upload."""
    form = UploadCsvForm()
    # POST request
    if form.validate_on_submit():
        f = form.csv_file.data
        f_str = f.read().decode("utf-8")
        # Check if empty file was uploaded
        if f is None or not f_str:
            flash("Empty file uploaded.", "danger")
            return redirect(url_for(".upload_data"))
        # Read the file data as string and parse it
        df = pd.read_csv(StringIO(f_str), index_col=0)
        # TODO: might want to store a file and keep the path here
        # instead of the dataframe
        session["macro_df"] = df
        return redirect(url_for(".view_data"))

    # GET request
    return render_template("upload_data.html", form=form)


@app.route("/view-data")
@check_data_found
def view_data():
    """Route for data view."""
    return render_template("view_data.html")


@app.route("/run-models", methods=["GET", "POST"])
@check_data_found
def run_models():
    """Route for models run."""
    form = RunModelsForm()
    # Define all models
    all_models = {
        "model_admission": {
            "name": "Model at Admission",
            "file": "model_admission.pkl",
        },
        "model_24hs": {"name": "Model at 24hs", "file": "model_24hs.pkl"},
        "model_cascade": {
            "name": "Cascade Model",
            "file": "model_cascade.pkl",
        },
        "model_invalid": {
            "name": "Example of non-suitable Model",
            "file": "model_cascade.pkl",
        },
    }
    # TODO: Filter invalid models
    valid_models = ["model_admission", "model_24hs", "model_cascade"]
    # Set dynamic model choices
    form.models.choices = [
        (val["file"], val["name"])
        for key, val in all_models.items()
        if key in valid_models
    ]

    # POST request
    if form.validate_on_submit():
        # TODO: checks and run and stuff
        return redirect(url_for(".view_output"))

    # GET request
    return render_template(
        "run_models.html",
        form=form,
        models=all_models,
        valid_models=valid_models,
    )


@app.route("/view-output")
@check_data_found
def view_output():
    """Route for model output."""
    # GET request
    return render_template("view_output.html")


# Custom Filter
# @app.app_template_filter("replace_value")
# def replace_value(value, arg):
#     return value.replace(arg, " ").title()
