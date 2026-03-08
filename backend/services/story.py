# ============================================================
# PROMPT AND THEATER — Story Generation Service
# Powered by Groq + Llama 3.3 70B
# ============================================================

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from backend.models.session import PlayerState
from backend.utils.prompts import (
    STORY_SYSTEM_PROMPT,
    OPENING_PROMPT,
    build_scene_prompt
)

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def clean_json_response(raw: str) -> str:
    raw = raw.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        return match.group(0)
    return raw


def generate_opening_scene() -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STORY_SYSTEM_PROMPT},
                {"role": "user", "content": OPENING_PROMPT}
            ],
            temperature=1.0,
            max_tokens=1024,
        )

        raw = response.choices[0].message.content
        cleaned = clean_json_response(raw)
        data = json.loads(cleaned)
        return data

    except json.JSONDecodeError as e:
        return _fallback_scene("The winds of Valdermoor carry an ill omen today.")
    except Exception as e:
        return _fallback_scene("The darkness of Valdermoor closes in around you.")


def generate_next_scene(player_state: PlayerState, choice: str) -> dict:
    try:
        prompt = build_scene_prompt(player_state, choice)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STORY_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
            max_tokens=1024,
        )

        raw = response.choices[0].message.content
        cleaned = clean_json_response(raw)
        data = json.loads(cleaned)
        return data

    except json.JSONDecodeError as e:
        return _fallback_scene("The shadows shift. Something has changed in Valdermoor.")
    except Exception as e:
        return _fallback_scene("The path ahead grows uncertain.")


def update_player_state(player_state: PlayerState, choice: str, scene_data: dict) -> PlayerState:
    player_state.decisions.append(choice[:80])
    player_state.scene += 1
    player_state.current_location = scene_data.get("location", player_state.current_location)

    if player_state.scene > 0 and player_state.scene % 8 == 0:
        player_state.act += 1

    choice_lower = choice.lower()

    if any(word in choice_lower for word in ["fight", "attack", "confront", "charge", "battle"]):
        damage = 15
        player_state.health = max(0, player_state.health - damage)
        player_state.gold += 5

    if any(word in choice_lower for word in ["steal", "deceive", "betray", "lie", "trick"]):
        player_state.reputation = max(0, player_state.reputation - 10)

    if any(word in choice_lower for word in ["help", "aid", "protect", "save", "defend"]):
        player_state.reputation = min(100, player_state.reputation + 8)

    if any(word in choice_lower for word in ["flee", "run", "escape", "retreat", "hide"]):
        player_state.reputation = max(0, player_state.reputation - 3)

    if player_state.health <= 0:
        player_state.is_alive = False

    return player_state


def _fallback_scene(narrative: str) -> dict:
    return {
        "narrative": narrative,
        "choices": [
            "1. Press forward into the unknown",
            "2. Take a moment to assess your surroundings",
            "3. Turn back and seek another path"
        ],
        "location": "Valdermoor",
        "mood": "dark",
        "image_prompt": "dark medieval fantasy landscape, ominous atmosphere, lone traveler, gothic ruins, crimson sky"
    }