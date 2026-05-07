import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
	sys.path.insert(0, str(ROOT_DIR))

from backend.database import Base, engine
from backend import models  # noqa: F401

# Create all database tables.
Base.metadata.create_all(bind=engine)
print("Database initialized.")
