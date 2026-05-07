import os
from dataclasses import dataclass


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Customer Service Platform")
    db_url: str = os.getenv("DB_URL", "sqlite:///./customer_service.db")
    model_dir: str = os.getenv("MODEL_DIR", "./models/fine_tuned_encoder")
    base_model: str = os.getenv(
        "BASE_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.45"))


settings = Settings()
