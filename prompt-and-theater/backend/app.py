# ============================================================
# PROMPT & THEATER — Flask Application Factory
# ============================================================

import os
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["DEBUG"] = True
    app.config["TICKETS_PATH"] = os.path.join(
        os.path.dirname(__file__), "../data/tickets/saved_tickets.json"
    )
    app.config["OUTCOMES_PATH"] = os.path.join(
        os.path.dirname(__file__), "../data/outcomes"
    )

    # --------------------------------------------------------
    # CORS
    # --------------------------------------------------------
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})

    # --------------------------------------------------------
    # Register Blueprints
    # --------------------------------------------------------
    from backend.routes.home import home_bp
    from backend.routes.tickets import tickets_bp
    from backend.routes.theater import theater_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(tickets_bp, url_prefix="/api/tickets")
    app.register_blueprint(theater_bp, url_prefix="/api/theater")

    # --------------------------------------------------------
    # Ensure Data Directories Exist
    # --------------------------------------------------------
    _ensure_data_files(app)

    return app


def _ensure_data_files(app):
    """
    Makes sure all required data files and folders exist
    on first run so nothing crashes on a fresh install.
    """
    tickets_path = app.config["TICKETS_PATH"]
    outcomes_path = app.config["OUTCOMES_PATH"]

    # Create tickets file if it doesn't exist
    if not os.path.exists(tickets_path):
        os.makedirs(os.path.dirname(tickets_path), exist_ok=True)
        with open(tickets_path, "w") as f:
            f.write("[]")

    # Create outcomes directory if it doesn't exist
    os.makedirs(outcomes_path, exist_ok=True)