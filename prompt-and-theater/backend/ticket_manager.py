# ============================================================
# PROMPT & THEATER — Ticket Manager
# Handles all ticket file operations cleanly
# ============================================================

import os
import json
import uuid
from datetime import datetime


class TicketManager:
    """
    Handles all reading, writing, updating and deleting
    of tickets from the local JSON storage file.

    Tickets are stored as a flat JSON array.
    Each ticket is a self contained dictionary.
    """

    def __init__(self, tickets_path: str):
        self.tickets_path = tickets_path
        self._ensure_file()

    # --------------------------------------------------------
    # File Safety
    # --------------------------------------------------------

    def _ensure_file(self):
        """
        Makes sure the tickets file exists on disk.
        Creates it with an empty array if it doesn't.
        """
        if not os.path.exists(self.tickets_path):
            os.makedirs(
                os.path.dirname(self.tickets_path),
                exist_ok=True
            )
            self._write([])

    # --------------------------------------------------------
    # Read / Write
    # --------------------------------------------------------

    def _read(self) -> list:
        """
        Reads all tickets from disk.
        Returns empty list if file is corrupted or missing.
        """
        try:
            with open(self.tickets_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write(self, tickets: list):
        """
        Writes the full tickets list back to disk.
        Always writes clean formatted JSON.
        """
        with open(self.tickets_path, "w", encoding="utf-8") as f:
            json.dump(tickets, f, indent=4, ensure_ascii=False)

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def get_all(self) -> list:
        """
        Returns all saved tickets sorted by
        most recently updated first.
        """
        tickets = self._read()
        return sorted(
            tickets,
            key=lambda t: t.get("updated_at", ""),
            reverse=True
        )

    def get_by_id(self, ticket_id: str) -> dict | None:
        """
        Returns a single ticket by its unique ID.
        Returns None if not found.
        """
        tickets = self._read()
        for ticket in tickets:
            if ticket.get("id") == ticket_id:
                return ticket
        return None

    def create(self, title: str, prompt: str, duration=None) -> dict:
        """
        Creates a new ticket and saves it to disk.
        Returns the newly created ticket.
        """
        ticket = {
            "id": str(uuid.uuid4()),
            "title": title.strip() if title else "Untitled Scene",
            "prompt": prompt.strip(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "duration": duration,
            "play_count": 0,
        }

        tickets = self._read()
        tickets.append(ticket)
        self._write(tickets)

        return ticket

    def update(self, ticket_id: str, updates: dict) -> dict | None:
        """
        Updates an existing ticket by ID.
        Only updates fields that are provided.
        Returns the updated ticket or None if not found.
        """
        tickets = self._read()

        for i, ticket in enumerate(tickets):
            if ticket.get("id") == ticket_id:
                allowed_fields = ["title", "prompt", "duration"]
                for field in allowed_fields:
                    if field in updates and updates[field] is not None:
                        tickets[i][field] = (
                            updates[field].strip()
                            if isinstance(updates[field], str)
                            else updates[field]
                        )
                tickets[i]["updated_at"] = datetime.now().isoformat()
                self._write(tickets)
                return tickets[i]

        return None

    def delete(self, ticket_id: str) -> bool:
        """
        Deletes a ticket by ID.
        Returns True if deleted, False if not found.
        """
        tickets = self._read()
        updated = [t for t in tickets if t.get("id") != ticket_id]

        if len(updated) == len(tickets):
            return False

        self._write(updated)
        return True

    def increment_play_count(self, ticket_id: str):
        """
        Increments the play count each time a ticket
        is watched in the theater.
        """
        tickets = self._read()
        for i, ticket in enumerate(tickets):
            if ticket.get("id") == ticket_id:
                tickets[i]["play_count"] = (
                    tickets[i].get("play_count", 0) + 1
                )
                self._write(tickets)
                return

    def count(self) -> int:
        """
        Returns the total number of saved tickets.
        """
        return len(self._read())