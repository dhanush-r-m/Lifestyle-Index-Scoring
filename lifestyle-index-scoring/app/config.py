# app/config.py
import os
from functools import lru_cache
from pydantic import BaseSettings, Field, AnyHttpUrl
from typing import Optional


class Settings(BaseSettings):
    # FastAPI
    app_name: str = "Lifestyle Index Scoring Service"
    app_version: str = "1.0.0"
    app_description: str = (
        "Lifestyle index scoring using Vertex AI Gemini Vision + state-aware rules"
    )

    # CORS
    backend_cors_origins: list[AnyHttpUrl] = []

    # Google / Vertex AI
    gcp_project_id: str = Field(..., env="GCP_PROJECT_ID")
    gcp_region: str = Field("asia-south1", env="GCP_REGION")  # good for India
    gemini_vision_model: str = Field(
        "gemini-1.5-flash-001", env="GEMINI_VISION_MODEL"
    )  # you can change to latest

    # Scoring
    base_score_max: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
