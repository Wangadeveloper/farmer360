from flask import Blueprint

stories_bp = Blueprint(
    "stories", __name__,
    template_folder="templates",
    static_folder="static"
)

from .routes import *
