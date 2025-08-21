from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Ensure project root (containing the 'src' package) is on sys.path if run directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# When executing this file directly (python src/api/main.py), the project root
# may not be on sys.path, producing ModuleNotFoundError: 'src'. We keep logic
# minimal here to avoid surprises while still supporting direct execution.

app = FastAPI(title="Game API", version="0.1.0")


class HealthResponse(BaseModel):
    status: str
    database_url_set: bool


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", database_url_set=bool(os.getenv("DATABASE_URL")))


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    # Prefer package style path when possible; fallback to direct app object
    app_path = "src.api.main:app" if (PROJECT_ROOT / "src" / "api" / "main.py").exists() else app  # type: ignore
    uvicorn.run(app_path, host="0.0.0.0", port=8000, reload=True)
