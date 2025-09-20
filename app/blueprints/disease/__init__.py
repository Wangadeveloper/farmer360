from flask import Blueprint

# Define blueprint
disease_bp = Blueprint(
    "disease", __name__,
    template_folder="templates",
    static_folder="static"
)

from . import routes  # Import routes so they are registered

