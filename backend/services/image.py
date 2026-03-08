# ============================================================
# PROMPT AND THEATER — Image Generation Service
# Powered by Pollinations.ai (Free, no API key required)
# ============================================================

import httpx
import urllib.parse
from backend.utils.prompts import build_image_prompt


POLLINATIONS_BASE_URL = "https://image.pollinations.ai/prompt/"

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 576
IMAGE_MODEL = "flux"


def generate_scene_image(image_prompt: str) -> str:
    try:
        full_prompt = build_image_prompt(image_prompt)
        encoded_prompt = urllib.parse.quote(full_prompt)

        image_url = (
            f"{POLLINATIONS_BASE_URL}{encoded_prompt}"
            f"?width={IMAGE_WIDTH}"
            f"&height={IMAGE_HEIGHT}"
            f"&model={IMAGE_MODEL}"
            f"&nologo=true"
            f"&enhance=true"
        )

        return image_url

    except Exception as e:
        return _fallback_image_url()


def verify_image_url(url: str) -> bool:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.head(url)
            return response.status_code == 200
    except Exception:
        return False


def _fallback_image_url() -> str:
    fallback_prompt = (
        "dark medieval fantasy landscape, "
        "ominous castle on a hill, "
        "crimson sky, gothic atmosphere, "
        "highly detailed oil painting"
    )
    encoded = urllib.parse.quote(fallback_prompt)
    return (
        f"{POLLINATIONS_BASE_URL}{encoded}"
        f"?width={IMAGE_WIDTH}"
        f"&height={IMAGE_HEIGHT}"
        f"&model={IMAGE_MODEL}"
        f"&nologo=true"
    )