"""Helper functions for the application."""

from functools import wraps
from typing import Callable

from flask import flash, redirect, session, url_for


def check_data_found(func: Callable) -> Callable:
    """Decorator to check if data availability."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session.get("macro_df") is None:
            flash("Data not found, please upload the data.", "danger")
            return redirect(url_for(".upload"))
        return func(*kwargs, **kwargs)

    return decorated_function
