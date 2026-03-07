# ============================================================
# PROMPT & THEATER — Tickets Route
# ============================================================

import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, render_template

tickets_bp = Blueprint("tickets", __name__)


def _load_tickets(app):
    """Load all saved tickets from the JSON file."""
    path = app.config["TICKETS_PATH"]
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_tickets(app, tickets):
    """Write all tickets back to the JSON file."""
    path = app.config["TICKETS_PATH"]
    with open(path, "w") as f:
        json.dump(tickets, f, indent=4)


# --------------------------------------------------------
# Page Route
# --------------------------------------------------------

@tickets_bp.route("/")
def tickets_page():
    """
    Renders the ticket management page.
    Create, watch, edit, delete tickets.
    """
    return render_template("tickets.html")


# --------------------------------------------------------
# API Routes
# --------------------------------------------------------

@tickets_bp.route("/all", methods=["GET"])
def get_all_tickets():
    """Return all saved tickets."""
    tickets = _load_tickets(current_app)
    return jsonify({
        "success": True,
        "tickets": tickets
    }), 200


@tickets_bp.route("/create", methods=["POST"])
def create_ticket():
    """
    Create a brand new ticket from a user prompt.
    Generates a unique ID and timestamps it.
    """
    data = request.get_json()

    if not data or not data.get("prompt"):
        return jsonify({
            "success": False,
            "error": "A prompt is required to create a ticket."
        }), 400

    prompt = data["prompt"].strip()

    if len(prompt) < 5:
        return jsonify({
            "success": False,
            "error": "Prompt is too short. Describe a scene."
        }), 400

    ticket = {
        "id": str(uuid.uuid4()),
        "title": data.get("title", "Untitled Scene").strip(),
        "prompt": prompt,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "duration": data.get("duration", None)
    }

    tickets = _load_tickets(current_app)
    tickets.append(ticket)
    _save_tickets(current_app, tickets)

    return jsonify({
        "success": True,
        "message": "Ticket created.",
        "ticket": ticket
    }), 201


@tickets_bp.route("/edit/<ticket_id>", methods=["PUT"])
def edit_ticket(ticket_id):
    """
    Edit an existing ticket by ID.
    User can update the title or prompt.
    """
    data = request.get_json()
    tickets = _load_tickets(current_app)

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            if "title" in data:
                ticket["title"] = data["title"].strip()
            if "prompt" in data:
                if len(data["prompt"].strip()) < 5:
                    return jsonify({
                        "success": False,
                        "error": "Prompt is too short."
                    }), 400
                ticket["prompt"] = data["prompt"].strip()
            ticket["updated_at"] = datetime.now().isoformat()
            _save_tickets(current_app, tickets)
            return jsonify({
                "success": True,
                "message": "Ticket updated.",
                "ticket": ticket
            }), 200

    return jsonify({
        "success": False,
        "error": "Ticket not found."
    }), 404


@tickets_bp.route("/delete/<ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    """
    Permanently delete a ticket by ID.
    """
    tickets = _load_tickets(current_app)
    updated = [t for t in tickets if t["id"] != ticket_id]

    if len(updated) == len(tickets):
        return jsonify({
            "success": False,
            "error": "Ticket not found."
        }), 404

    _save_tickets(current_app, updated)

    return jsonify({
        "success": True,
        "message": "Ticket deleted."
    }), 200


@tickets_bp.route("/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """
    Retrieve a single ticket by ID.
    """
    tickets = _load_tickets(current_app)

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return jsonify({
                "success": True,
                "ticket": ticket
            }), 200

    return jsonify({
        "success": False,
        "error": "Ticket not found."
    }), 404