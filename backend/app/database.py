from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------
# CONFIG CHEMIN BASE DE DONNÉES
# -------------------------------------------------------------------
# On se base sur la racine du projet "maavnica-smartcard"
BASE_DIR = Path(__file__).resolve().parents[2]

# Dossier "data" pour la base SQLite
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / "smartcard.db"

# IMPORTANT : chemin ABSOLU vers la base -> plus de surprise
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# -------------------------------------------------------------------
# ENGINE / SESSION / BASE
# -------------------------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # nécessaire avec SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dépendance FastAPI pour obtenir une session DB par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

