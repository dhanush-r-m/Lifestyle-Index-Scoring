# app/services/vertex_client.py

import vertexai
from vertexai.generative_models import GenerativeModel, Image
from typing import List, Any
from ..config import get_settings

settings = get_settings()

# Initialize Vertex AI once per server startup
vertexai.init(
    project=settings.gcp_project_id,
    location=settings.gcp_region
)


def build_vision_model() -> GenerativeModel:
    """Return the configured Gemini Vision model."""
    return GenerativeModel(settings.gemini_vision_model)


def make_image_parts(image_bytes_list: List[bytes]) -> List[Image]:
    """Convert raw bytes to Gemini Image objects."""
    return [Image.from_bytes(b) for b in image_bytes_list]


def call_gemini_vision(
    prompt: str,
    image_bytes_list: List[bytes],
    extra_system_instruction: str | None = None,
) -> Any:
    """
    Generic call to Gemini Vision supporting up to 10 images.
    Returns raw model response (caller will handle .text parsing).
    """

    # ----- Validation -----
    if not image_bytes_list:
        raise ValueError("At least one image is required.")

    if len(image_bytes_list) > 10:
        raise ValueError("Maximum 10 images are allowed.")

    # ----- Build model -----
    model = build_vision_model()

    # ----- Build content list -----
    contents: List[Any] = []

    if extra_system_instruction:
        contents.append(extra_system_instruction)

    contents.append(prompt)
    contents.extend(make_image_parts(image_bytes_list))

    # ----- Gemini call -----
    response = model.generate_content(contents)

    return response
