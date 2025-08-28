import os
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / ".env"
if env_path.exists():
    load_dotenv(env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

# Créer le moteur (connexion à la DB)
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Base pour les modèles
Base = declarative_base()

# Session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def ping_database() -> bool:
    """Retourne True si SELECT 1 fonctionne, sinon False."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print(f"[DB][PING] échec: {e}")
        return False
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()