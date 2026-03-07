# ============================================================
# PROMPT & THEATER — Sound Engine
# All sounds synthesized in code. No external files needed.
# Generates Web Audio API instructions for the frontend.
# ============================================================


class SoundEngine:
    """
    Generates sound synthesis instructions that the
    frontend Web Audio API will execute in the browser.

    Every sound is defined as a recipe — a set of
    parameters the browser uses to synthesize the
    sound in real time using pure JavaScript.

    To add new sounds: add a new entry to _load_sounds()
    The frontend will pick it up automatically.

    Sound Types:
    - oscillator  : tonal sounds, hums, engines
    - noise       : percussive, impact, organic sounds
    - composite   : layered combination of multiple sounds
    """

    def __init__(self):
        self.sounds = self._load_sounds()

    def get(self, sound_id: str) -> dict | None:
        """
        Returns the synthesis recipe for a sound by ID.
        Returns None if the sound doesn't exist.
        """
        return self.sounds.get(sound_id, None)

    def get_all(self) -> dict:
        """
        Returns the entire sound library.
        Used by the frontend to preload all sounds.
        """
        return self.sounds

    # --------------------------------------------------------
    # SOUND LIBRARY
    # Each sound is a synthesis recipe for the Web Audio API
    # --------------------------------------------------------

    def _load_sounds(self) -> dict:
        return {

            # --- Footsteps ---
            "footsteps": {
                "label": "Footsteps Walking",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "brown",
                        "frequency": 80,
                        "attack": 0.001,
                        "decay": 0.08,
                        "sustain": 0.0,
                        "release": 0.05,
                        "volume": 0.4,
                        "filter": "lowpass",
                        "filter_frequency": 200,
                    }
                ],
                "tempo": 500,
                "repeat": True,
            },

            "footsteps_fast": {
                "label": "Footsteps Running",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "brown",
                        "frequency": 100,
                        "attack": 0.001,
                        "decay": 0.05,
                        "sustain": 0.0,
                        "release": 0.03,
                        "volume": 0.6,
                        "filter": "lowpass",
                        "filter_frequency": 250,
                    }
                ],
                "tempo": 250,
                "repeat": True,
            },

            # --- Impacts ---
            "thud": {
                "label": "Thud / Fall Impact",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 120,
                        "frequency_end": 40,
                        "attack": 0.001,
                        "decay": 0.3,
                        "sustain": 0.0,
                        "release": 0.2,
                        "volume": 0.8,
                    },
                    {
                        "type": "noise",
                        "color": "brown",
                        "attack": 0.001,
                        "decay": 0.15,
                        "sustain": 0.0,
                        "release": 0.1,
                        "volume": 0.5,
                        "filter": "lowpass",
                        "filter_frequency": 300,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "punch_impact": {
                "label": "Punch Impact",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.001,
                        "decay": 0.08,
                        "sustain": 0.0,
                        "release": 0.05,
                        "volume": 0.7,
                        "filter": "bandpass",
                        "filter_frequency": 800,
                    },
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 200,
                        "frequency_end": 80,
                        "attack": 0.001,
                        "decay": 0.1,
                        "sustain": 0.0,
                        "release": 0.05,
                        "volume": 0.5,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "car_impact": {
                "label": "Car Impact",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.001,
                        "decay": 0.4,
                        "sustain": 0.1,
                        "release": 0.3,
                        "volume": 0.9,
                        "filter": "lowpass",
                        "filter_frequency": 1000,
                    },
                    {
                        "type": "oscillator",
                        "wave": "sawtooth",
                        "frequency_start": 300,
                        "frequency_end": 50,
                        "attack": 0.001,
                        "decay": 0.5,
                        "sustain": 0.0,
                        "release": 0.3,
                        "volume": 0.7,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            # --- Vehicles ---
            "car_engine": {
                "label": "Car Engine Passing",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sawtooth",
                        "frequency_start": 80,
                        "frequency_end": 120,
                        "attack": 0.3,
                        "decay": 0.0,
                        "sustain": 0.8,
                        "release": 0.5,
                        "volume": 0.5,
                        "filter": "lowpass",
                        "filter_frequency": 400,
                    },
                    {
                        "type": "noise",
                        "color": "brown",
                        "attack": 0.3,
                        "decay": 0.0,
                        "sustain": 0.6,
                        "release": 0.5,
                        "volume": 0.3,
                        "filter": "lowpass",
                        "filter_frequency": 300,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "car_door": {
                "label": "Car Door",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.001,
                        "decay": 0.2,
                        "sustain": 0.0,
                        "release": 0.1,
                        "volume": 0.6,
                        "filter": "bandpass",
                        "filter_frequency": 600,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            # --- Human Sounds ---
            "crying": {
                "label": "Crying",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 300,
                        "frequency_end": 250,
                        "attack": 0.2,
                        "decay": 0.3,
                        "sustain": 0.5,
                        "release": 0.4,
                        "volume": 0.4,
                        "tremolo": True,
                        "tremolo_rate": 5,
                        "tremolo_depth": 0.3,
                    },
                    {
                        "type": "noise",
                        "color": "pink",
                        "attack": 0.1,
                        "decay": 0.2,
                        "sustain": 0.3,
                        "release": 0.3,
                        "volume": 0.2,
                        "filter": "bandpass",
                        "filter_frequency": 500,
                    }
                ],
                "tempo": 800,
                "repeat": True,
            },

            "laughter": {
                "label": "Laughter",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 400,
                        "frequency_end": 350,
                        "attack": 0.05,
                        "decay": 0.1,
                        "sustain": 0.2,
                        "release": 0.1,
                        "volume": 0.5,
                        "tremolo": True,
                        "tremolo_rate": 8,
                        "tremolo_depth": 0.6,
                    }
                ],
                "tempo": 300,
                "repeat": True,
            },

            "yelling": {
                "label": "Yelling",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sawtooth",
                        "frequency_start": 250,
                        "frequency_end": 300,
                        "attack": 0.05,
                        "decay": 0.1,
                        "sustain": 0.6,
                        "release": 0.2,
                        "volume": 0.7,
                        "filter": "bandpass",
                        "filter_frequency": 1200,
                    },
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.05,
                        "decay": 0.1,
                        "sustain": 0.4,
                        "release": 0.2,
                        "volume": 0.3,
                        "filter": "highpass",
                        "filter_frequency": 800,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "scream": {
                "label": "Scream",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sawtooth",
                        "frequency_start": 500,
                        "frequency_end": 700,
                        "attack": 0.02,
                        "decay": 0.1,
                        "sustain": 0.7,
                        "release": 0.3,
                        "volume": 0.8,
                        "filter": "bandpass",
                        "filter_frequency": 2000,
                    },
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.02,
                        "decay": 0.05,
                        "sustain": 0.5,
                        "release": 0.2,
                        "volume": 0.4,
                        "filter": "highpass",
                        "filter_frequency": 1000,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "cheer": {
                "label": "Crowd Cheer",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "pink",
                        "attack": 0.3,
                        "decay": 0.2,
                        "sustain": 0.6,
                        "release": 0.5,
                        "volume": 0.6,
                        "filter": "bandpass",
                        "filter_frequency": 1500,
                    },
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 600,
                        "frequency_end": 800,
                        "attack": 0.3,
                        "decay": 0.2,
                        "sustain": 0.4,
                        "release": 0.5,
                        "volume": 0.3,
                        "tremolo": True,
                        "tremolo_rate": 12,
                        "tremolo_depth": 0.4,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            # --- Atmosphere ---
            "whoosh_soft": {
                "label": "Soft Whoosh",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.05,
                        "decay": 0.15,
                        "sustain": 0.0,
                        "release": 0.1,
                        "volume": 0.3,
                        "filter": "bandpass",
                        "filter_frequency": 2000,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            "explosion": {
                "label": "Explosion",
                "type": "composite",
                "layers": [
                    {
                        "type": "noise",
                        "color": "brown",
                        "attack": 0.001,
                        "decay": 0.8,
                        "sustain": 0.3,
                        "release": 1.0,
                        "volume": 1.0,
                        "filter": "lowpass",
                        "filter_frequency": 800,
                    },
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 150,
                        "frequency_end": 20,
                        "attack": 0.001,
                        "decay": 1.0,
                        "sustain": 0.0,
                        "release": 0.5,
                        "volume": 0.9,
                    },
                    {
                        "type": "noise",
                        "color": "white",
                        "attack": 0.001,
                        "decay": 0.3,
                        "sustain": 0.0,
                        "release": 0.2,
                        "volume": 0.6,
                        "filter": "highpass",
                        "filter_frequency": 1000,
                    }
                ],
                "tempo": None,
                "repeat": False,
            },

            # --- Ambient Home Screen ---
            "ambient_dark": {
                "label": "Dark Ambient Atmosphere",
                "type": "composite",
                "layers": [
                    {
                        "type": "oscillator",
                        "wave": "sine",
                        "frequency_start": 60,
                        "frequency_end": 55,
                        "attack": 2.0,
                        "decay": 0.0,
                        "sustain": 1.0,
                        "release": 2.0,
                        "volume": 0.15,
                        "tremolo": True,
                        "tremolo_rate": 0.2,
                        "tremolo_depth": 0.1,
                    },
                    {
                        "type": "noise",
                        "color": "brown",
                        "attack": 2.0,
                        "decay": 0.0,
                        "sustain": 1.0,
                        "release": 2.0,
                        "volume": 0.08,
                        "filter": "lowpass",
                        "filter_frequency": 150,
                    }
                ],
                "tempo": None,
                "repeat": True,
            },
        }