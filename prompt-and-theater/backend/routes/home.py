# ============================================================
# PROMPT & THEATER — Home Route
# ============================================================

from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    """
    Renders the main home screen.
    The atmospheric title screen and THEATER button.
    """
    return render_template("index.html")