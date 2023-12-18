"""Views for the application."""

from flask import flash, render_template, redirect, session, url_for
from io import BytesIO, StringIO
import pandas as pd

from .main import app
from .forms import UploadCsvForm, RunModelForm
from .utils import check_data_found


__all__ = ["index", "upload", "viewdata", "runmodels"]


# 404 ERROR HANDLING
@app.errorhandler(404)
def page_not_found(error):
    """Route for 404 response."""
    return render_template("404.html")


@app.route("/")
def index():
    """Route for homepage."""
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Route for data upload."""
    form = UploadCsvForm()
    # POST request
    if form.validate_on_submit():
        f = form.csv_file.data
        f_str = f.read().decode("utf-8")
        # Check if empty file was uploaded
        if f is None or not f_str:
            flash("Empty file uploaded.", "danger")
            return redirect(url_for(".upload"))
        # Read the file data as string and parse it
        df = pd.read_csv(StringIO(f_str), index_col=0)
        # TODO: might want to store a file and keep the path here
        # instead of the dataframe
        session["macro_df"] = df
        return redirect(url_for(".viewdata"))

    # GET request
    return render_template("upload.html", form=form)


@check_data_found
@app.route("/viewdata")
def viewdata():
    """Route for data view."""
    return render_template("view.html")


@check_data_found
@app.route("/runmodels")
def runmodels():
    """Route for model run."""
    form = RunModelForm()
    # POST request
    if form.validate_on_submit():
        return redirect(url_for(".runmodels"))

    # GET request
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

    return render_template(
        "run.html",
        form=form,
        models=all_models,
        valid_models=valid_models,
    )


# Custom Filter
# @app.app_template_filter("replace_value")
# def replace_value(value, arg):
#     return value.replace(arg, " ").title()
