from flask import Blueprint

chemicals_bp = Blueprint(
    "chemicals", __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes
