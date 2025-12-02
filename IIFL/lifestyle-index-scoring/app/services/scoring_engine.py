# app/services/scoring_engine.py

from typing import Dict, Tuple

from ..schemas import (
    GeminiRawSignals,
    LocationContext,
    LifestyleScoreBreakdown,
    LifestylePersona,
)
from ..location_config import get_state_profile, ClimateZone, MetroFlag
from ..scoring_config import ASSET_WEIGHTS, normalize_asset_name
from .persona_explanations import PERSONA_EXPLANATIONS


def _compute_asset_score_for_state(
    asset_name: str,
    quantity: int,
    confidence: float,
    metro_flag: MetroFlag,
    climate_zone: ClimateZone,
) -> float:
    """
    Compute contribution of a single asset given state context.
    Uses base weight, metro/non-metro multiplier, climate adjustment,
    quantity and model confidence.
    """
    key = normalize_asset_name(asset_name)
    config = ASSET_WEIGHTS.get(key)
    if not config:
        # Unknown asset → no contribution
        return 0.0

    metro_mult = (
        config["metro_multiplier"]
        if metro_flag == "metro"
        else config["non_metro_multiplier"]
    )
    climate_mult = config["climate_adjust"].get(climate_zone, 1.0)

    base = config["base"]
    raw = base * quantity * confidence * metro_mult * climate_mult
    return raw


def infer_persona_from_score(normalized_score: float) -> LifestylePersona:
    """
    Map a normalized lifestyle score (0–100) to a simple, common-English persona.
    Buckets can be tuned as needed.
    """
    if normalized_score >= 80:
        return "HIGH_INCOME_LIFESTYLE"
    if normalized_score >= 65:
        return "TREND_FOLLOWER"
    if normalized_score >= 55:
        return "TECH_FRIENDLY_USER"
    if normalized_score >= 45:
        return "HOME_COMFORT_LOVER"
    if normalized_score >= 35:
        return "CAREFUL_PLANNER"
    if normalized_score >= 25:
        return "TRADITIONAL_LIFESTYLE"
    if normalized_score >= 15:
        return "DISCOUNT_SEEKER"
    return "LOW_INCOME_LIFESTYLE"


def persona_and_explanation_from_score(
    normalized_score: float,
) -> Tuple[LifestylePersona, str]:
    """
    Convenience helper:
    - infer persona from score
    - fetch human-readable explanation from PERSONA_EXPLANATIONS
    """
    persona = infer_persona_from_score(normalized_score)
    explanation = PERSONA_EXPLANATIONS.get(
        persona,
        "Your lifestyle pattern was analyzed based on detected items.",
    )
    return persona, explanation


def score_lifestyle(
    raw_signals: GeminiRawSignals,
    location: LocationContext,
) -> Tuple[float, LifestyleScoreBreakdown]:
    """
    Core scoring function.
    Returns:
      - normalized lifestyle index (0–100)
      - detailed breakdown object
    """
    profile = get_state_profile(location.state)
    climate_zone: ClimateZone = profile["climate"]
    metro_flag: MetroFlag = profile["metro_flag"]

    asset_contributions: Dict[str, float] = {}
    total_raw_score = 0.0

    for asset in raw_signals.assets:
        contrib = _compute_asset_score_for_state(
            asset_name=asset.name,
            quantity=asset.quantity,
            confidence=asset.confidence,
            metro_flag=metro_flag,
            climate_zone=climate_zone,
        )
        if contrib <= 0:
            continue

        total_raw_score += contrib
        asset_contributions[asset.name] = (
            asset_contributions.get(asset.name, 0.0) + contrib
        )

    # Convert "raw" score to 0–100 band with a simple linear saturation curve.
    # Assumption: raw_score ~ 80 corresponds to lifestyle_index ~ 100.
    raw_for_100 = 80.0
    normalized = (total_raw_score / raw_for_100) * 100.0 if raw_for_100 > 0 else 0.0
    normalized = max(0.0, min(100.0, normalized))  # clamp 0–100

    breakdown = LifestyleScoreBreakdown(
        total_score=round(total_raw_score, 2),
        normalized_score=round(normalized, 2),
        max_score=100.0,
        asset_contributions={
            k: round(v, 2) for k, v in asset_contributions.items()
        },
        location_adjustments={
            # Simple example multipliers; can be expanded later
            "metro_flag_multiplier": 1.0 if metro_flag == "metro" else 0.9,
            "climate_zone": climate_zone,
        },
        metro_flag=metro_flag,
        climate_zone=climate_zone,
    )

    return normalized, breakdown
