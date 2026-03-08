from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4


class PlayerState(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    player_name: str = "Stranger"
    health: int = 100
    max_health: int = 100
    gold: int = 10
    reputation: int = 50
    inventory: list[str] = Field(default_factory=list)
    allies: list[str] = Field(default_factory=list)
    enemies: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    current_location: str = "Unknown"
    act: int = 1
    scene: int = 0
    is_alive: bool = True
    ending: Optional[str] = None


class SceneRequest(BaseModel):
    session_id: Optional[str] = None
    player_state: Optional[PlayerState] = None
    choice: Optional[str] = None


class SceneResponse(BaseModel):
    session_id: str
    narrative: str
    choices: list[str]
    image_url: str
    player_state: PlayerState
    scene_number: int
    act: int
    is_game_over: bool = False
    game_over_message: Optional[str] = None