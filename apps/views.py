# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask import render_template, request, redirect, session, url_for
from io import BytesIO, StringIO
from jinja2 import TemplateNotFound
import pandas as pd

# App modules
from apps import app
from .models import df_variables


# App main route + generic routing
@app.route("/", defaults={"path": "index.html"})
@app.route("/")
def index():
    session["juclinical_df"] = None
    session["juclinical_verified"] = False
    try:
        return render_template("pages/index.html")
    except TemplateNotFound:
        return render_template("pages/index.html"), 404


@app.route("/upload", methods=["GET", "POST"])
def upload():
    session["juclinical_df"] = None
    session["juclinical_verified"] = False
    if request.method == "POST":
        if "file" not in request.files:
            return render_template(
                "pages/upload_data.html",
                error="No file uploaded.",
                session=session,
            )
        file = request.files["file"]
        if file.filename == "":
            return render_template(
                "pages/upload_data.html",
                error="Invalid file name.",
                session=session,
            )
        csv_data = file.read().decode("utf-8")
        csv_file = BytesIO(csv_data.encode("utf-8"))
        df = pd.read_csv(csv_file, index_col=0)
        session["juclinical_df"] = df
        return redirect(url_for("viewdata"))

    return render_template("pages/upload_data.html", session=session)


@app.route("/input_manually", methods=["GET", "POST"])
def input_manually():
    session["juclinical_df"] = None
    session["juclinical_verified"] = False
    if request.method == "POST":
        # TODO: Verificar que los datos sean correctos
        df = pd.DataFrame({k: [v] for k, v in request.form.items()})
        session["juclinical_df"] = df
        return redirect(url_for("viewdata"))

    return render_template(
        "pages/input_manually.html", session=session, df_variables=df_variables
    )


@app.route("/viewdata")
def viewdata():
    return render_template("pages/view_data.html", session=session)


@app.route("/runmodels")
def runmodels():
    session["juclinical_verified"] = True
    model_folder = "models/"
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
        "pages/run_models.html",
        session=session,
        models=all_models,
        valid_models=valid_models,
    )


# Custom Filter
@app.template_filter("replace_value")
def replace_value(value, arg):
    return value.replace(arg, " ").title()
