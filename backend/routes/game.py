# ============================================================
# PROMPT AND THEATER — Game Routes
# FastAPI endpoints for all game logic
# ============================================================

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.models.session import PlayerState, SceneRequest, SceneResponse
from backend.services.story import (
    generate_opening_scene,
    generate_next_scene,
    update_player_state
)
from backend.services.image import generate_scene_image
import urllib.parse

router = APIRouter()

sessions: dict[str, PlayerState] = {}


@router.get("/image")
async def proxy_image(url: str):
    try:
        decoded_url = urllib.parse.unquote(url)
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
            response = await client.get(decoded_url)
            if response.status_code == 200:
                content_type = response.headers.get("content-type", "image/jpeg")
                return StreamingResponse(
                    iter([response.content]),
                    media_type=content_type
                )
    except Exception as e:
        raise HTTPException(status_code=504, detail=f"Image fetch failed: {str(e)}")
    raise HTTPException(status_code=404, detail="Image not available")


@router.post("/start", response_model=SceneResponse)
async def start_game(player_name: str = "Stranger"):
    try:
        player_state = PlayerState(player_name=player_name)
        scene_data = generate_opening_scene()

        raw_url = generate_scene_image(
            scene_data.get("image_prompt", "dark medieval fantasy landscape")
        )
        encoded_url = urllib.parse.quote(raw_url, safe='')
        image_url = f"/api/game/image?url={encoded_url}"

        sessions[player_state.session_id] = player_state

        return SceneResponse(
            session_id=player_state.session_id,
            narrative=scene_data.get("narrative", "Your adventure begins..."),
            choices=scene_data.get("choices", []),
            image_url=image_url,
            player_state=player_state,
            scene_number=player_state.scene,
            act=player_state.act,
            is_game_over=False
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/choice", response_model=SceneResponse)
async def make_choice(request: SceneRequest):
    try:
        session_id = request.session_id
        choice = request.choice

        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        if not choice:
            raise HTTPException(status_code=400, detail="No choice provided")

        player_state = sessions[session_id]

        if not player_state.is_alive:
            raise HTTPException(status_code=400, detail="Game over")

        scene_data = generate_next_scene(player_state, choice)
        player_state = update_player_state(player_state, choice, scene_data)

        raw_url = generate_scene_image(
            scene_data.get("image_prompt", "dark medieval fantasy landscape")
        )
        encoded_url = urllib.parse.quote(raw_url, safe='')
        image_url = f"/api/game/image?url={encoded_url}"

        sessions[session_id] = player_state

        is_game_over = not player_state.is_alive
        game_over_message = None

        if is_game_over:
            game_over_message = (
                f"Your story ends here in Valdermoor. "
                f"You survived {player_state.scene} scenes across {player_state.act} acts. "
                f"Your legend will be forgotten by morning."
            )

        return SceneResponse(
            session_id=session_id,
            narrative=scene_data.get("narrative", "The story continues..."),
            choices=scene_data.get("choices", []),
            image_url=image_url,
            player_state=player_state,
            scene_number=player_state.scene,
            act=player_state.act,
            is_game_over=is_game_over,
            game_over_message=game_over_message
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/{session_id}")
async def get_state(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]


@router.post("/restart/{session_id}")
async def restart_game(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session cleared. Ready for a new adventure."}