from flask import Blueprint

finance_bp = Blueprint(
    "finance", __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes
