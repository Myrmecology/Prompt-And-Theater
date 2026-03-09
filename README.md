# Prompt And Theater
# FOR A VIDEO DEMO OF THIS PROJECT, PLEASE VISIT: https://www.youtube.com/watch?v=lsOPsR4aRPQ&t=7s

A browser-based, dark medieval choose your own adventure game where no two playthroughs are ever the same. Every scene is generated dynamically, every image is unique, and every decision you make shapes the world around you.

---

## What It Is

Prompt And Theater is a fully procedural narrative RPG set in the dark medieval world of Valdermoor. The story never repeats. The images never repeat. Your choices have real consequences that carry forward through every act of the adventure.

---

## Features

- Dynamically generated story and narrative on every playthrough
- Unique scene illustrations generated for every single scene
- Session memory — the world remembers every decision you make
- Player stats — Health, Gold, Reputation and Act tracked in real time
- Inventory system with live sidebar display
- Decision log tracking every choice made during a run
- Cinematic act transition screens as the story deepens
- Typewriter narrative effect for atmospheric text delivery
- Cinematic fade transitions between every scene
- Game over screen with full run summary
- Fully responsive layout

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | HTML, CSS, JavaScript |
| Story Generation | Groq API — Llama 3.3 70B |
| Image Generation | Pollinations.ai — Flux |
| Templating | Jinja2 |
| Server | Uvicorn |

---

## Project Structure
```
prompt-and-theater/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── backend/
│   ├── routes/
│   │   └── game.py
│   ├── services/
│   │   ├── story.py
│   │   └── image.py
│   ├── models/
│   │   └── session.py
│   └── utils/
│       └── prompts.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   ├── fonts/
│   └── images/
└── templates/
    └── index.html
```

---

## Requirements

- Python 3.10 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com)

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/Myrmecology/Prompt-And-Theater.git
cd prompt-and-theater
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create your environment file**

Create a `.env` file in the root of the project with the following:
```
GROQ_API_KEY=your_groq_api_key_here
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
SECRET_KEY=your_secret_key_here
```

---

## Running The App
```bash
source venv/Scripts/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then open your browser and go to:
```
http://127.0.0.1:8000
```

---

## How To Play

1. Enter your name on the title screen
2. Click **Begin Your Fate**
3. Read the opening scene and the AI generated illustration
4. Choose from three options at the bottom of the screen
5. Every choice affects your Health, Gold, Reputation and the story itself
6. Survive as long as you can in the world of Valdermoor

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |
| `APP_ENV` | Environment — development or production |
| `APP_HOST` | Host address — default 127.0.0.1 |
| `APP_PORT` | Port — default 8000 |
| `SECRET_KEY` | A random secret string for session security |

---

