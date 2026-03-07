# ============================================================
# PROMPT & THEATER — Theater Route
# ============================================================

from flask import Blueprint, request, jsonify, render_template
from backend.intent_engine import IntentEngine

theater_bp = Blueprint("theater", __name__)
intent_engine = IntentEngine()


# --------------------------------------------------------
# Page Route
# --------------------------------------------------------

@theater_bp.route("/")
def theater_page():
    """
    Renders the theater page.
    This is where the animation plays.
    """
    return render_template("theater.html")


# --------------------------------------------------------
# API Routes
# --------------------------------------------------------

@theater_bp.route("/process", methods=["POST"])
def process_prompt():
    """
    Receives a ticket prompt and runs it through
    the intent engine. Returns a structured animation
    sequence the frontend will use to drive the theater.
    """
    data = request.get_json()

    if not data or not data.get("prompt"):
        return jsonify({
            "success": False,
            "error": "No prompt provided."
        }), 400

    prompt = data["prompt"].strip()

    try:
        animation_sequence = intent_engine.process(prompt)

        return jsonify({
            "success": True,
            "prompt": prompt,
            "sequence": animation_sequence
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Theater engine failed: {str(e)}"
        }), 500


@theater_bp.route("/preview/<ticket_id>", methods=["GET"])
def preview_ticket(ticket_id):
    """
    Load and process a saved ticket by ID
    directly for theater playback.
    """
    import os
    import json
    from flask import current_app

    tickets_path = current_app.config["TICKETS_PATH"]

    if not os.path.exists(tickets_path):
        return jsonify({
            "success": False,
            "error": "No tickets found."
        }), 404

    with open(tickets_path, "r") as f:
        tickets = json.load(f)

    ticket = next((t for t in tickets if t["id"] == ticket_id), None)

    if not ticket:
        return jsonify({
            "success": False,
            "error": "Ticket not found."
        }), 404

    try:
        animation_sequence = intent_engine.process(ticket["prompt"])

        return jsonify({
            "success": True,
            "ticket": ticket,
            "sequence": animation_sequence
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Theater engine failed: {str(e)}"
        }), 500