# app/routers/score_router.py

from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from ..schemas import (
    LifestyleScoreResponse,
    LocationContext,
)
from ..services.reasoning_engine import extract_lifestyle_signals_from_images
from ..services.scoring_engine import (
    score_lifestyle,
    persona_and_explanation_from_score,
)

router = APIRouter(prefix="/score", tags=["lifestyle"])


@router.post(
    "/lifestyle",
    response_model=LifestyleScoreResponse,
    summary="Compute lifestyle index from uploaded household images and location info",
)
async def score_lifestyle_endpoint(
    images: List[UploadFile] = File(..., description="Upload 1–10 household images"),
    state: str = Form(..., description="Indian state (e.g., Karnataka, Rajasthan)"),
    city: str = Form("", description="City / town name"),
    pincode: str = Form("", description="Pincode"),
):
    # -----------------------------
    # Validate uploaded images
    # -----------------------------
    if not images:
        raise HTTPException(status_code=400, detail="At least one image is required.")

    if len(images) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed.")

    # -----------------------------
    # Convert uploaded files → bytes
    # -----------------------------
    image_bytes_list: List[bytes] = []
    for img in images:
        content = await img.read()
        if not content:
            continue
        image_bytes_list.append(content)

    if not image_bytes_list:
        raise HTTPException(status_code=400, detail="Uploaded images are empty or invalid.")

    # -----------------------------
    # Prepare location context
    # -----------------------------
    location = LocationContext(
        state=state,
        city=city or None,
        pincode=pincode or None,
    )

    # -----------------------------
    # STEP 1: Gemini Vision (reasoning_engine)
    # Extract structured asset signals from images
    # -----------------------------
    raw_signals = extract_lifestyle_signals_from_images(
        image_bytes_list=image_bytes_list,
        location=location,
    )

    # -----------------------------
    # STEP 2: Rule-based lifestyle scoring
    # -----------------------------
    lifestyle_index, breakdown = score_lifestyle(
        raw_signals=raw_signals,
        location=location,
    )

    # -----------------------------
    # STEP 3: Persona + explanation (simple English)
    # -----------------------------
    persona, persona_explanation = persona_and_explanation_from_score(lifestyle_index)

    # -----------------------------
    # Combine final explanation
    # -----------------------------
    final_explanation = (
        f"{persona_explanation} "
        f"Your lifestyle index is {lifestyle_index:.1f} based on detected assets "
        f"and your state context ({breakdown.metro_flag}, {breakdown.climate_zone}). "
        "For example, in hot-arid states like Rajasthan, an air-conditioner is treated "
        "closer to a necessity, while in temperate metro states like Karnataka "
        "(e.g., Bengaluru), the same AC contributes more towards lifestyle scoring."
    )

    # -----------------------------
    # Return final response
    # -----------------------------
    return LifestyleScoreResponse(
        lifestyle_index=lifestyle_index,
        persona_hint=persona,
        breakdown=breakdown,
        location_context=location,
        gemini_raw=raw_signals,
        explanation=final_explanation,
    )
