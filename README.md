# Project Name

A dual Python project containing a Pygame-based game and a FastAPI backend, fully automated via VSCode Tasks (no bash scripts needed). One-command setup, isolated virtual environments, Dockerized PostgreSQL database, and ready-to-run debug configurations.

## Features
- Separate virtual environments for game (`src/game/.venv`) and API (`src/api/.venv`)
- PostgreSQL via `docker-compose`
- Alembic-ready structure (versions folder ignored until created)
- Comprehensive VSCode tasks for setup, running, testing, cleaning
- Debug configurations for both game and API

## Quick Start
1. Open the folder in VSCode
2. Run: `Tasks: Run Task` -> `Setup: Complete Project`
3. Run: `Run: Game` or `Run: API Development`
4. (Optional) Press F5 and pick a debug configuration

## Environment Variables
Copy `.env.example` to `.env` and adjust values. The API uses `DATABASE_URL`.

## VSCode Tasks Overview
| Task                    | Purpose                          |
| ----------------------- | -------------------------------- |
| Setup: Complete Project | Runs all setup (envs, deps, db)  |
| Setup: Game Environment | Creates & installs game venv     |
| Setup: API Environment  | Creates & installs API venv      |
| Setup: Database         | Starts Docker PostgreSQL & waits |
| Run: Game               | Launches Pygame loop             |
| Run: API Development    | Uvicorn reload server            |
| Run: API Production     | Uvicorn without reload           |
| Database: Start         | Starts DB container              |
| Database: Stop          | Stops DB container               |
| Database: Reset         | Destroys & recreates DB          |
| Test: Game              | Pytest for game                  |
| Test: API               | Pytest for API                   |
| Clean: All              | Remove envs, docker data, caches |

## Project Layout
```
src/
  game/
    main.py
    requirements.txt
  api/
    main.py
    requirements.txt
```

## Testing
Use tasks: `Test: Game`, `Test: API`. They activate correct venv automatically.

## Adding Alembic
Create `src/api/database/alembic.ini` and versions folder, configure `script_location` etc. Then extend tasks for migrations.

## License
MIT
