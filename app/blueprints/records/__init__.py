from flask import Blueprint

records_bp = Blueprint(
    "records", __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes
