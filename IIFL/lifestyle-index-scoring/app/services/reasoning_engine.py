# app/services/reasoning_engine.py

import json
from typing import List

from fastapi import HTTPException

from ..services.vertex_client import call_gemini_vision
from ..schemas import GeminiRawSignals, DetectedAsset, LocationContext
from ..scoring_config import normalize_asset_name
from ..logger import logger

BASE_EXTRA_INSTRUCTION = """
You are an underwriting assistant scoring household lifestyle from photos.

You MUST:
- Look at all uploaded images of the customer's living environment (home interior, exterior, vehicles, appliances).
- Identify only lifestyle-related assets that you see (NOT people).
- Be conservative: if unsure, give lower confidence.
- Consider typical Indian context.

You MUST respond ONLY in JSON with this structure:

{
  "assets": [
    {
      "name": "AIR_CONDITIONER",
      "confidence": 0.93,
      "quantity": 2,
      "extra": {
        "brand": "Daikin",
        "room_type": "bedroom"
      }
    }
  ],
  "notes": "free-text reasoning and assumptions here"
}

Where:
- name: short UPPER_SNAKE_CASE identifier (e.g., AIR_CONDITIONER, REFRIGERATOR, SMART_TV, CAR, TWO_WHEELER, GATED_COMMUNITY, MODULAR_KITCHEN, LUXURY_INTERIORS)
- confidence is between 0 and 1.
- quantity is at least 1.
- Do not invent assets you cannot see clearly.
"""


def _extract_json_block(text: str) -> str:
    """
    Try to robustly extract a JSON object from the model output.
    Handles cases like:
      ```json
      { ... }
      ```
    or extra text before/after.
    """
    txt = text.strip()

    # Handle fenced code blocks ```json ... ```
    if txt.startswith("```"):
        # Remove leading and trailing fences
        # e.g., ```json\n{...}\n```
        lines = txt.splitlines()
        # drop first and last fence lines if they start with ```
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        txt = "\n".join(lines).strip()
        # remove optional 'json' at very start
        if txt.lower().startswith("json"):
            txt = txt[4:].strip()

    # Fallback: find first '{' and last '}' to extract raw JSON object
    if "{" in txt and "}" in txt:
        start = txt.find("{")
        end = txt.rfind("}")
        if start != -1 and end != -1 and end > start:
            txt = txt[start : end + 1].strip()

    return txt


def extract_lifestyle_signals_from_images(
    image_bytes_list: List[bytes],
    location: LocationContext,
) -> GeminiRawSignals:
    """
    Calls Gemini Vision, asks for structured JSON, and parses into GeminiRawSignals.
    """
    user_prompt = f"""
The household is located in the Indian state: {location.state}.
City (may be empty or small town): {location.city or "unknown"}.

Identify visual lifestyle assets and output STRICT JSON as specified.
Remember to be conservative; if the image is blurry or ambiguous, 
use a confidence <= 0.5.
"""

    # ---- Call Gemini Vision ----
    try:
        response = call_gemini_vision(
            prompt=user_prompt,
            image_bytes_list=image_bytes_list,
            extra_system_instruction=BASE_EXTRA_INSTRUCTION,
        )
    except Exception as e:
        logger.exception("Gemini Vision call failed.")
        raise HTTPException(status_code=500, detail=f"Gemini Vision error: {e}")

    text = getattr(response, "text", None)
    if not text:
        logger.error("Empty response from Gemini Vision.")
        raise HTTPException(
            status_code=500,
            detail="Empty response from Gemini Vision",
        )

    # ---- Extract JSON part ----
    json_str = _extract_json_block(text)

    try:
        raw = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error(
            "Failed to parse JSON from Gemini Vision: %s | Raw text (truncated): %s",
            e,
            text[:500],
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse JSON from Gemini Vision: {e}. Response text (truncated): {text[:500]}",
        )

    # ---- Parse assets safely ----
    assets: List[DetectedAsset] = []
    raw_assets = raw.get("assets", []) or []

    for a in raw_assets:
        try:
            name = normalize_asset_name(a.get("name", ""))
            if not name:
                continue

            # confidence: clamp to [0, 1]
            try:
                confidence = float(a.get("confidence", 0.0))
            except (TypeError, ValueError):
                confidence = 0.0
            confidence = max(0.0, min(1.0, confidence))

            # quantity: at least 1
            try:
                quantity = int(a.get("quantity", 1))
            except (TypeError, ValueError):
                quantity = 1
            if quantity < 1:
                quantity = 1

            extra = a.get("extra", {}) or {}

            asset = DetectedAsset(
                name=name,
                confidence=confidence,
                quantity=quantity,
                extra=extra,
            )
            assets.append(asset)
        except Exception as ex:
            logger.warning("Skipping malformed asset entry: %s | Error: %s", a, ex)
            continue

    # ---- Build and return structured signals ----
    notes = raw.get("notes")
    if notes is not None and not isinstance(notes, str):
        notes = str(notes)

    gemini_signals = GeminiRawSignals(
        assets=assets,
        notes=notes,
    )

    logger.info(
        "Extracted %d assets from Gemini Vision for state=%s, city=%s",
        len(assets),
        location.state,
        location.city or "N/A",
    )

    return gemini_signals
