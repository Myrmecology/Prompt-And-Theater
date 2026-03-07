# ============================================================
# PROMPT & THEATER — Intent Engine
# The Local LLM — Reads prompts, builds animation sequences
# ============================================================

import re
from backend.outcome_library import OutcomeLibrary


class IntentEngine:
    """
    The brain of Prompt & Theater.

    Reads a natural language prompt from the user,
    extracts meaning, and returns a structured animation
    sequence the theater can play back.

    No external API. No internet required.
    Fully local. Fully expandable.
    """

    def __init__(self):
        self.library = OutcomeLibrary()

    # --------------------------------------------------------
    # Main Entry Point
    # --------------------------------------------------------

    def process(self, prompt: str) -> list:
        """
        Takes a raw user prompt and returns a list of
        animation events in order of occurrence.

        Each event is a dict the frontend animation engine
        can read and execute directly.
        """
        prompt = prompt.lower().strip()
        sentences = self._split_into_sentences(prompt)
        sequence = []

        for sentence in sentences:
            events = self._extract_events(sentence)
            sequence.extend(events)

        if not sequence:
            sequence = self._fallback_sequence()

        sequence = self._resolve_durations(prompt, sequence)
        sequence = self._assign_figures(sequence)

        return sequence

    # --------------------------------------------------------
    # Sentence Splitting
    # --------------------------------------------------------

    def _split_into_sentences(self, prompt: str) -> list:
        """
        Splits the prompt into individual sentences or
        clauses so each action can be processed separately.
        """
        prompt = re.sub(r"\band\b", ".", prompt)
        prompt = re.sub(r"\bthen\b", ".", prompt)
        prompt = re.sub(r"\bafter that\b", ".", prompt)
        prompt = re.sub(r"\bafterwards\b", ".", prompt)
        prompt = re.sub(r"\bnext\b", ".", prompt)
        prompt = re.sub(r"\bsuddenly\b", ".", prompt)
        prompt = re.sub(r"\bwhile\b", ".", prompt)

        raw = re.split(r"[.,;!?\n]+", prompt)
        return [s.strip() for s in raw if s.strip()]

    # --------------------------------------------------------
    # Event Extraction
    # --------------------------------------------------------

    def _extract_events(self, sentence: str) -> list:
        """
        Scans a single sentence and maps it to one or
        more animation events from the outcome library.
        """
        events = []
        matched = False

        for behavior_id, behavior in self.library.behaviors.items():
            for trigger in behavior["triggers"]:
                if trigger in sentence:
                    event = self._build_event(behavior_id, behavior, sentence)
                    events.append(event)
                    matched = True
                    break

        if not matched:
            for atomic_id, atomic in self.library.atomics.items():
                for trigger in atomic["triggers"]:
                    if trigger in sentence:
                        event = self._build_atomic_event(
                            atomic_id, atomic, sentence
                        )
                        events.append(event)
                        matched = True
                        break

        return events

    # --------------------------------------------------------
    # Event Builders
    # --------------------------------------------------------

    def _build_event(
        self, behavior_id: str, behavior: dict, sentence: str
    ) -> dict:
        """
        Builds a full behavior animation event.
        """
        figure = self._detect_figure(sentence)
        duration = self._detect_duration(sentence) or behavior.get(
            "default_duration", 2000
        )

        return {
            "type": "behavior",
            "id": behavior_id,
            "label": behavior["label"],
            "figure": figure,
            "atoms": behavior["atoms"],
            "duration": duration,
            "loop": behavior.get("loop", False),
            "sound": behavior.get("sound", None),
            "props": behavior.get("props", []),
            "emotion": behavior.get("emotion", None),
        }

    def _build_atomic_event(
        self, atomic_id: str, atomic: dict, sentence: str
    ) -> dict:
        """
        Builds a single atomic movement event.
        """
        figure = self._detect_figure(sentence)
        duration = self._detect_duration(sentence) or atomic.get(
            "default_duration", 500
        )

        return {
            "type": "atomic",
            "id": atomic_id,
            "label": atomic["label"],
            "figure": figure,
            "body_part": atomic["body_part"],
            "movement": atomic["movement"],
            "duration": duration,
            "sound": atomic.get("sound", None),
        }

    # --------------------------------------------------------
    # Figure Detection
    # --------------------------------------------------------

    def _detect_figure(self, sentence: str) -> str:
        """
        Determines which stick figure an event applies to.
        Returns 'both', 'figure_a', or 'figure_b'.
        """
        both_triggers = [
            "both", "they", "together", "each other",
            "two figures", "both figures"
        ]
        figure_b_triggers = [
            "other", "second", "figure b", "the other one",
            "another figure"
        ]

        for trigger in both_triggers:
            if trigger in sentence:
                return "both"

        for trigger in figure_b_triggers:
            if trigger in sentence:
                return "figure_b"

        return "figure_a"

    # --------------------------------------------------------
    # Duration Detection
    # --------------------------------------------------------

    def _detect_duration(self, sentence: str) -> int:
        """
        Looks for time references in the sentence and
        returns a duration in milliseconds.
        """
        patterns = [
            (r"(\d+)\s*minute[s]?", 60000),
            (r"(\d+)\s*second[s]?", 1000),
            (r"for a (while|bit|moment)", 3000),
            (r"quickly|fast|brief", 800),
            (r"slowly|slow|long", 5000),
        ]

        for pattern, multiplier in patterns:
            match = re.search(pattern, sentence)
            if match:
                if match.lastindex and match.group(1).isdigit():
                    return int(match.group(1)) * multiplier
                return multiplier

        return None

    # --------------------------------------------------------
    # Duration Resolver
    # --------------------------------------------------------

    def _resolve_durations(self, prompt: str, sequence: list) -> list:
        """
        Does a final pass over the full sequence to
        make sure durations are reasonable and consistent.
        """
        for event in sequence:
            if event["duration"] is None:
                event["duration"] = 2000
            event["duration"] = max(500, min(event["duration"], 300000))
        return sequence

    # --------------------------------------------------------
    # Figure Assignment
    # --------------------------------------------------------

    def _assign_figures(self, sequence: list) -> list:
        """
        Does a final pass to ensure figure assignments
        make logical sense across the full sequence.
        Fills in gaps where figure couldn't be detected.
        """
        last_figure = "figure_a"
        for event in sequence:
            if event["figure"] == "figure_a":
                last_figure = "figure_a"
            elif event["figure"] == "figure_b":
                last_figure = "figure_b"
            elif event["figure"] == "both":
                last_figure = "both"
            else:
                event["figure"] = last_figure
        return sequence

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    def _fallback_sequence(self) -> list:
        """
        If nothing in the prompt matched anything in the
        library, return a default idle sequence so the
        theater never plays nothing.
        """
        return [
            {
                "type": "behavior",
                "id": "idle",
                "label": "Standing Idle",
                "figure": "both",
                "atoms": ["stand", "breathe"],
                "duration": 3000,
                "loop": False,
                "sound": None,
                "props": [],
                "emotion": "neutral",
            }
        ]