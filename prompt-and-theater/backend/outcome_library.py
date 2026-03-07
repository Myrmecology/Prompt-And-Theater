# ============================================================
# PROMPT & THEATER — Outcome Library
# The Local LLM Vocabulary
# Atomic Movements + Composed Behaviors
# Add to this file to expand the system forever
# ============================================================


class OutcomeLibrary:
    """
    The complete vocabulary of Prompt & Theater.

    ATOMICS — Single body part movements. The smallest
    possible unit of animation.

    BEHAVIORS — Composed sequences of atomics that produce
    recognizable actions, emotions, and events.

    To expand: simply add new entries to either dictionary.
    The intent engine will pick them up automatically.
    """

    def __init__(self):
        self.atomics = self._load_atomics()
        self.behaviors = self._load_behaviors()

    # --------------------------------------------------------
    # ATOMIC MOVEMENTS
    # Each atomic is one body part doing one thing.
    # body_part: head, torso, left_arm, right_arm,
    #            left_leg, right_leg, whole_body
    # --------------------------------------------------------

    def _load_atomics(self) -> dict:
        return {

            # --- Head ---
            "head_nod": {
                "label": "Head Nod",
                "triggers": ["nod", "nodding", "agrees", "yes"],
                "body_part": "head",
                "movement": "rotate_down_up",
                "default_duration": 600,
                "sound": "whoosh_soft",
            },
            "head_shake": {
                "label": "Head Shake",
                "triggers": ["shakes head", "disagrees", "no"],
                "body_part": "head",
                "movement": "rotate_left_right",
                "default_duration": 600,
                "sound": None,
            },
            "head_tilt": {
                "label": "Head Tilt",
                "triggers": ["tilts head", "confused look", "curious"],
                "body_part": "head",
                "movement": "rotate_side",
                "default_duration": 500,
                "sound": None,
            },
            "head_down": {
                "label": "Head Down",
                "triggers": ["looks down", "hangs head", "bows head"],
                "body_part": "head",
                "movement": "rotate_down",
                "default_duration": 700,
                "sound": None,
            },
            "head_up": {
                "label": "Head Up",
                "triggers": ["looks up", "gazes up", "stares up"],
                "body_part": "head",
                "movement": "rotate_up",
                "default_duration": 500,
                "sound": None,
            },

            # --- Torso ---
            "torso_lean_forward": {
                "label": "Lean Forward",
                "triggers": ["leans forward", "leans in", "bends forward"],
                "body_part": "torso",
                "movement": "rotate_forward",
                "default_duration": 600,
                "sound": None,
            },
            "torso_lean_back": {
                "label": "Lean Back",
                "triggers": ["leans back", "recoils", "steps back"],
                "body_part": "torso",
                "movement": "rotate_back",
                "default_duration": 600,
                "sound": None,
            },
            "torso_twist_left": {
                "label": "Torso Twist Left",
                "triggers": ["turns left", "looks left", "twists left"],
                "body_part": "torso",
                "movement": "rotate_left",
                "default_duration": 400,
                "sound": None,
            },
            "torso_twist_right": {
                "label": "Torso Twist Right",
                "triggers": ["turns right", "looks right", "twists right"],
                "body_part": "torso",
                "movement": "rotate_right",
                "default_duration": 400,
                "sound": None,
            },

            # --- Arms ---
            "right_arm_raise": {
                "label": "Right Arm Raise",
                "triggers": ["raises right arm", "right arm up", "right hand up"],
                "body_part": "right_arm",
                "movement": "raise",
                "default_duration": 500,
                "sound": None,
            },
            "left_arm_raise": {
                "label": "Left Arm Raise",
                "triggers": ["raises left arm", "left arm up", "left hand up"],
                "body_part": "left_arm",
                "movement": "raise",
                "default_duration": 500,
                "sound": None,
            },
            "both_arms_raise": {
                "label": "Both Arms Raise",
                "triggers": ["raises arms", "arms up", "hands up"],
                "body_part": "both_arms",
                "movement": "raise",
                "default_duration": 500,
                "sound": None,
            },
            "right_arm_swing": {
                "label": "Right Arm Swing",
                "triggers": ["swings right arm", "right arm swing"],
                "body_part": "right_arm",
                "movement": "swing_forward",
                "default_duration": 400,
                "sound": None,
            },
            "left_arm_swing": {
                "label": "Left Arm Swing",
                "triggers": ["swings left arm", "left arm swing"],
                "body_part": "left_arm",
                "movement": "swing_forward",
                "default_duration": 400,
                "sound": None,
            },
            "arms_cover_face": {
                "label": "Arms Cover Face",
                "triggers": ["covers face", "hides face", "face in hands"],
                "body_part": "both_arms",
                "movement": "raise_to_face",
                "default_duration": 600,
                "sound": None,
            },
            "arms_crossed": {
                "label": "Arms Crossed",
                "triggers": ["crosses arms", "arms folded", "folds arms"],
                "body_part": "both_arms",
                "movement": "cross",
                "default_duration": 500,
                "sound": None,
            },
            "right_arm_point": {
                "label": "Right Arm Point",
                "triggers": ["points", "pointing", "gestures toward"],
                "body_part": "right_arm",
                "movement": "extend_point",
                "default_duration": 600,
                "sound": None,
            },

            # --- Legs ---
            "left_leg_lift": {
                "label": "Left Leg Lift",
                "triggers": ["left leg lifts", "lifts left leg", "left knee up"],
                "body_part": "left_leg",
                "movement": "lift",
                "default_duration": 400,
                "sound": None,
            },
            "right_leg_lift": {
                "label": "Right Leg Lift",
                "triggers": ["right leg lifts", "lifts right leg", "right knee up"],
                "body_part": "right_leg",
                "movement": "lift",
                "default_duration": 400,
                "sound": None,
            },
            "legs_wide_stance": {
                "label": "Wide Stance",
                "triggers": ["wide stance", "legs apart", "plants feet"],
                "body_part": "both_legs",
                "movement": "spread",
                "default_duration": 400,
                "sound": None,
            },
            "legs_together": {
                "label": "Legs Together",
                "triggers": ["feet together", "stands straight", "legs together"],
                "body_part": "both_legs",
                "movement": "close",
                "default_duration": 300,
                "sound": None,
            },

            # --- Whole Body ---
            "whole_body_shake": {
                "label": "Whole Body Shake",
                "triggers": ["shakes", "trembles", "quivers", "shivers"],
                "body_part": "whole_body",
                "movement": "oscillate",
                "default_duration": 1000,
                "sound": None,
            },
            "whole_body_jump": {
                "label": "Jump",
                "triggers": ["jumps", "leaps", "hops"],
                "body_part": "whole_body",
                "movement": "jump",
                "default_duration": 600,
                "sound": "thud",
            },
            "whole_body_spin": {
                "label": "Spin",
                "triggers": ["spins", "twirls", "rotates"],
                "body_part": "whole_body",
                "movement": "spin_360",
                "default_duration": 800,
                "sound": "whoosh_soft",
            },
            "whole_body_fall": {
                "label": "Fall Down",
                "triggers": ["falls", "collapses", "drops to ground", "falls down"],
                "body_part": "whole_body",
                "movement": "fall",
                "default_duration": 800,
                "sound": "thud",
            },
            "whole_body_crouch": {
                "label": "Crouch",
                "triggers": ["crouches", "ducks", "squats"],
                "body_part": "whole_body",
                "movement": "crouch",
                "default_duration": 500,
                "sound": None,
            },
        }

    # --------------------------------------------------------
    # BEHAVIORS
    # Composed sequences of atomics that form full actions.
    # Add new behaviors here to expand the local LLM.
    # --------------------------------------------------------

    def _load_behaviors(self) -> dict:
        return {

            # --- Locomotion ---
            "walk": {
                "label": "Walking",
                "triggers": [
                    "walk", "walks", "walking", "strolls",
                    "approaches", "moves toward", "goes to"
                ],
                "atoms": [
                    "left_leg_lift", "right_arm_swing",
                    "right_leg_lift", "left_arm_swing"
                ],
                "default_duration": 2000,
                "loop": True,
                "sound": "footsteps",
                "props": [],
                "emotion": "neutral",
            },
            "run": {
                "label": "Running",
                "triggers": [
                    "run", "runs", "running", "sprints",
                    "sprinting", "dashes", "flees", "chases"
                ],
                "atoms": [
                    "left_leg_lift", "right_arm_swing",
                    "right_leg_lift", "left_arm_swing",
                    "torso_lean_forward"
                ],
                "default_duration": 2000,
                "loop": True,
                "sound": "footsteps_fast",
                "props": [],
                "emotion": "neutral",
            },
            "run_away": {
                "label": "Running Away",
                "triggers": [
                    "runs away", "run away", "flees", "escapes",
                    "bolts away", "takes off running"
                ],
                "atoms": [
                    "torso_lean_forward", "left_leg_lift",
                    "right_arm_swing", "right_leg_lift",
                    "left_arm_swing", "head_tilt"
                ],
                "default_duration": 2500,
                "loop": False,
                "sound": "footsteps_fast",
                "props": [],
                "emotion": "scared",
            },
            "jog_in_place": {
                "label": "Jogging In Place",
                "triggers": [
                    "jogs in place", "jogging in place",
                    "jogging", "jogs", "jog"
                ],
                "atoms": [
                    "left_leg_lift", "right_arm_swing",
                    "right_leg_lift", "left_arm_swing"
                ],
                "default_duration": 3000,
                "loop": True,
                "sound": "footsteps_fast",
                "props": [],
                "emotion": "neutral",
            },

            # --- Emotions ---
            "cry": {
                "label": "Crying",
                "triggers": [
                    "cry", "cries", "crying", "weeps",
                    "weeping", "sobs", "sobbing", "tears"
                ],
                "atoms": [
                    "head_down", "whole_body_shake",
                    "arms_cover_face", "torso_lean_forward"
                ],
                "default_duration": 3000,
                "loop": True,
                "sound": "crying",
                "props": [],
                "emotion": "sad",
            },
            "laugh": {
                "label": "Laughing",
                "triggers": [
                    "laugh", "laughs", "laughing", "cackles",
                    "giggles", "hysterical", "bursts out laughing"
                ],
                "atoms": [
                    "torso_lean_forward", "whole_body_shake",
                    "head_tilt", "both_arms_raise"
                ],
                "default_duration": 2500,
                "loop": True,
                "sound": "laughter",
                "props": [],
                "emotion": "happy",
            },
            "scared": {
                "label": "Scared",
                "triggers": [
                    "scared", "frightened", "terrified", "afraid",
                    "looks scared", "in fear", "horrified", "shocked"
                ],
                "atoms": [
                    "torso_lean_back", "both_arms_raise",
                    "whole_body_shake", "head_tilt"
                ],
                "default_duration": 2000,
                "loop": False,
                "sound": "scream",
                "props": [],
                "emotion": "scared",
            },
            "angry": {
                "label": "Angry",
                "triggers": [
                    "angry", "anger", "furious", "rage",
                    "mad", "enraged", "yells", "yelling", "screams"
                ],
                "atoms": [
                    "whole_body_shake", "right_arm_point",
                    "torso_lean_forward", "head_nod"
                ],
                "default_duration": 2000,
                "loop": False,
                "sound": "yelling",
                "props": [],
                "emotion": "angry",
            },
            "celebrate": {
                "label": "Celebrating",
                "triggers": [
                    "celebrate", "celebrates", "celebrating",
                    "cheers", "victory dance", "victorious",
                    "pumps fist", "jumps for joy"
                ],
                "atoms": [
                    "both_arms_raise", "whole_body_jump",
                    "whole_body_spin", "head_nod"
                ],
                "default_duration": 3000,
                "loop": False,
                "sound": "cheer",
                "props": [],
                "emotion": "happy",
            },
            "argue": {
                "label": "Arguing",
                "triggers": [
                    "argue", "argues", "arguing", "argument",
                    "confronts", "confrontation", "disputes"
                ],
                "atoms": [
                    "right_arm_point", "torso_lean_forward",
                    "head_shake", "whole_body_shake"
                ],
                "default_duration": 3000,
                "loop": True,
                "sound": "yelling",
                "props": [],
                "emotion": "angry",
            },

            # --- Social ---
            "wave": {
                "label": "Waving",
                "triggers": [
                    "wave", "waves", "waving", "greets",
                    "says hello", "hello"
                ],
                "atoms": ["right_arm_raise", "right_arm_swing"],
                "default_duration": 1500,
                "loop": False,
                "sound": None,
                "props": [],
                "emotion": "happy",
            },
            "dance": {
                "label": "Dancing",
                "triggers": [
                    "dance", "dances", "dancing", "boogie",
                    "groove", "grooves", "bust a move"
                ],
                "atoms": [
                    "whole_body_spin", "both_arms_raise",
                    "left_leg_lift", "right_leg_lift",
                    "torso_twist_left", "torso_twist_right"
                ],
                "default_duration": 4000,
                "loop": True,
                "sound": None,
                "props": [],
                "emotion": "happy",
            },
            "hug": {
                "label": "Hugging",
                "triggers": [
                    "hug", "hugs", "hugging", "embrace",
                    "embraces", "embracing"
                ],
                "atoms": [
                    "both_arms_raise", "torso_lean_forward",
                    "head_nod"
                ],
                "default_duration": 2000,
                "loop": False,
                "sound": None,
                "props": [],
                "emotion": "happy",
            },
            "sit_down": {
                "label": "Sitting Down",
                "triggers": [
                    "sits", "sits down", "sitting", "takes a seat",
                    "sits on", "plops down"
                ],
                "atoms": [
                    "whole_body_crouch", "torso_lean_forward",
                    "legs_together"
                ],
                "default_duration": 1000,
                "loop": False,
                "sound": None,
                "props": [],
                "emotion": "neutral",
            },
            "stand_up": {
                "label": "Standing Up",
                "triggers": [
                    "stands up", "gets up", "rises", "stand up",
                    "stands", "gets to their feet"
                ],
                "atoms": [
                    "torso_lean_forward", "legs_wide_stance",
                    "both_arms_raise", "legs_together"
                ],
                "default_duration": 1000,
                "loop": False,
                "sound": None,
                "props": [],
                "emotion": "neutral",
            },

            # --- Combat ---
            "punch": {
                "label": "Punching",
                "triggers": [
                    "punch", "punches", "punching", "hits",
                    "strikes", "swings at"
                ],
                "atoms": [
                    "legs_wide_stance", "torso_twist_right",
                    "right_arm_swing", "torso_twist_left",
                    "left_arm_swing"
                ],
                "default_duration": 800,
                "loop": False,
                "sound": "punch_impact",
                "props": [],
                "emotion": "angry",
            },
            "boxing_match": {
                "label": "Boxing Match",
                "triggers": [
                    "boxing", "box", "fight", "fighting",
                    "brawl", "fistfight", "boxing match",
                    "duke it out"
                ],
                "atoms": [
                    "legs_wide_stance", "right_arm_swing",
                    "left_arm_swing", "torso_twist_left",
                    "torso_twist_right", "whole_body_crouch",
                    "head_tilt"
                ],
                "default_duration": 10000,
                "loop": True,
                "sound": "punch_impact",
                "props": [],
                "emotion": "angry",
            },
            "knocked_out": {
                "label": "Knocked Out",
                "triggers": [
                    "knocked out", "ko", "knocked down",
                    "beaten", "loses the fight", "goes down"
                ],
                "atoms": [
                    "whole_body_fall", "head_down",
                    "arms_cover_face"
                ],
                "default_duration": 2000,
                "loop": False,
                "sound": "thud",
                "props": [],
                "emotion": "neutral",
            },

            # --- Events / Props ---
            "hit_by_car": {
                "label": "Hit By Car",
                "triggers": [
                    "hit by a car", "run over", "car hits",
                    "gets hit", "struck by car", "car runs over",
                    "car drives by and run"
                ],
                "atoms": [
                    "whole_body_fall", "whole_body_spin",
                    "whole_body_shake"
                ],
                "default_duration": 2000,
                "loop": False,
                "sound": "car_impact",
                "props": ["car"],
                "emotion": "neutral",
            },
            "car_drives_by": {
                "label": "Car Drives By",
                "triggers": [
                    "car drives by", "car passes",
                    "car goes by", "vehicle passes"
                ],
                "atoms": [],
                "default_duration": 2000,
                "loop": False,
                "sound": "car_engine",
                "props": ["car"],
                "emotion": "neutral",
            },
            "get_in_car": {
                "label": "Gets In Car",
                "triggers": [
                    "gets in", "gets inside", "climbs in",
                    "gets into the car", "enters the car"
                ],
                "atoms": [
                    "walk", "whole_body_crouch",
                    "torso_lean_forward"
                ],
                "default_duration": 2500,
                "loop": False,
                "sound": "car_door",
                "props": ["car"],
                "emotion": "neutral",
            },
            "plane_crash": {
                "label": "Plane Crash",
                "triggers": [
                    "plane crashes", "plane crash",
                    "airplane crashes", "crashes into",
                    "plane crashes into"
                ],
                "atoms": [
                    "whole_body_fall", "whole_body_shake"
                ],
                "default_duration": 3000,
                "loop": False,
                "sound": "explosion",
                "props": ["plane", "fire"],
                "emotion": "scared",
            },
            "idle": {
                "label": "Standing Idle",
                "triggers": [
                    "stands", "standing", "idle",
                    "waits", "waiting", "doing nothing"
                ],
                "atoms": ["whole_body_shake"],
                "default_duration": 2000,
                "loop": True,
                "sound": None,
                "props": [],
                "emotion": "neutral",
            },
            "stop_light": {
                "label": "Waiting At Stop Light",
                "triggers": [
                    "stop light", "stoplight", "traffic light",
                    "red light", "waits at light"
                ],
                "atoms": [
                    "jog_in_place", "head_tilt", "head_up"
                ],
                "default_duration": 3000,
                "loop": True,
                "sound": None,
                "props": ["stoplight"],
                "emotion": "neutral",
            },
        }