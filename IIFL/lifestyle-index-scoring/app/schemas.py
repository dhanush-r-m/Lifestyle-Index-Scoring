# app/schemas.py

from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field


# Layman-friendly persona labels
LifestylePersona = Literal[
    "HIGH_EARNING_COMFORT_SEEKER",       # Previously "AFFLUENT"
    "TRENDSETTER_AND_INFLUENCER",        # Previously "OPINION_LEADER"
    "TECH_SAVVY_MODERN_USER",            # Previously "TECHNOLOGY_MAVERICK"
    "IMPULSIVE_BUYER",                   # Previously "IMPULSIVE_SPENDER"
    "DEAL_AND_DISCOUNT_LOVER",           # Previously "OFFER_ENTHUSIAST"
    "HEALTH_AND_ECO_FRIENDLY_USER",      # Previously "ECO_WELLNESS_DIGITALIST"
    "FAMILY_FIRST_AND_COMMUNITY_ORIENTED", # Previously "COLLECTIVIST"
    "SAFE_AND_CAREFUL_PLANNER",          # Previously "CAUTIOUS_PLANNER"
    "TRADITIONAL_HOME_FOCUSED",          # Previously "MATURE_TRADITIONALIST"
    "FINANCIALLY_CONSTRAINED_USER",      # Previously "STRUGGLER"
    "HOME_COMFORT_AND_WARMTH_SEEKER",    # Previously "NESTLER"
    "LOW_TRUST_MINIMAL_TECH_USER",       # Previously "TECH_TRUST_SKEPTIC"
]


class LocationContext(BaseModel):
    state: str = Field(..., description="Indian state (ex: Karnataka, Rajasthan)")
    city: Optional[str] = Field(None, description="City or town name")
    pincode: Optional[str] = None


class DetectedAsset(BaseModel):
    name: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    quantity: int = 1
    extra: Dict[str, str] = Field(default_factory=dict)


class GeminiRawSignals(BaseModel):
    assets: List[DetectedAsset]
    notes: Optional[str] = None


class LifestyleScoreBreakdown(BaseModel):
    total_score: float
    normalized_score: float
    max_score: float
    asset_contributions: Dict[str, float]
    location_adjustments: Dict[str, float]
    metro_flag: str
    climate_zone: str


class LifestyleScoreResponse(BaseModel):
    lifestyle_index: float = Field(..., ge=0.0, le=100.0)
    persona_hint: Optional[LifestylePersona] = None
    breakdown: LifestyleScoreBreakdown
    location_context: LocationContext
    gemini_raw: GeminiRawSignals
    explanation: str


class ErrorResponse(BaseModel):
    detail: str
