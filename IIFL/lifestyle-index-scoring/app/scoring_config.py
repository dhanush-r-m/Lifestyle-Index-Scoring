# app/scoring_config.py

from typing import Dict, Literal, TypedDict
from .location_config import ClimateZone, MetroFlag


class AssetWeight(TypedDict):
    base: float
    metro_multiplier: float
    non_metro_multiplier: float
    climate_adjust: Dict[ClimateZone, float]


ASSET_WEIGHTS: Dict[str, AssetWeight] = {
    # -------------------- APPLIANCES --------------------
    "AIR_CONDITIONER": {
        "base": 12.0,
        "metro_multiplier": 1.6,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 0.4,
            "hot_humid": 0.7,
            "temperate": 1.2,
            "cold": 0.2,
        },
    },
    "REFRIGERATOR": {
        "base": 8.0,
        "metro_multiplier": 1.0,
        "non_metro_multiplier": 1.2,
        "climate_adjust": {
            "hot_arid": 1.1,
            "hot_humid": 1.3,
            "temperate": 0.9,
            "cold": 0.8,
        },
    },
    "WASHING_MACHINE": {
        "base": 7.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.1,
            "temperate": 1.2,
            "cold": 1.0,
        },
    },
    "MICROWAVE_OVEN": {
        "base": 4.5,
        "metro_multiplier": 1.3,
        "non_metro_multiplier": 0.9,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.1,
            "cold": 1.0,
        },
    },

    # -------------------- ELECTRONICS --------------------
    "SMART_TV": {
        "base": 7.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "LAPTOP": {
        "base": 6.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "TABLET": {
        "base": 4.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },

    # -------------------- VEHICLES --------------------
    "CAR": {
        "base": 15.0,
        "metro_multiplier": 1.0,
        "non_metro_multiplier": 1.3,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "TWO_WHEELER": {
        "base": 4.0,
        "metro_multiplier": 0.8,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "ELECTRIC_SCOOTER": {
        "base": 6.5,
        "metro_multiplier": 1.4,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.2,
            "temperate": 1.2,
            "cold": 0.8,
        },
    },

    # -------------------- HOME & LIVING --------------------
    "GATED_COMMUNITY": {
        "base": 10.0,
        "metro_multiplier": 1.3,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "MODULAR_KITCHEN": {
        "base": 5.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "LUXURY_INTERIORS": {
        "base": 15.0,
        "metro_multiplier": 1.1,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "HOME_GYM": {
        "base": 9.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.1,
            "temperate": 1.2,
            "cold": 1.0,
        },
    },
    "SWIMMING_POOL": {
        "base": 18.0,
        "metro_multiplier": 1.3,
        "non_metro_multiplier": 1.2,
        "climate_adjust": {
            "hot_arid": 0.9,
            "hot_humid": 1.3,
            "temperate": 1.1,
            "cold": 0.3,
        },
    },
    "SOLAR_PANELS": {
        "base": 7.0,
        "metro_multiplier": 1.1,
        "non_metro_multiplier": 1.3,
        "climate_adjust": {
            "hot_arid": 1.2,
            "hot_humid": 0.8,
            "temperate": 1.0,
            "cold": 0.7,
        },
    },

    # -------------------- LIFESTYLE INDICATORS --------------------
    "PET_DOG": {
        "base": 5.0,
        "metro_multiplier": 1.1,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.2,
            "temperate": 1.0,
            "cold": 1.0,
        },
    },
    "SMART_HOME_DEVICES": {
        "base": 8.0,
        "metro_multiplier": 1.4,
        "non_metro_multiplier": 1.0,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.1,
            "cold": 1.0,
        },
    },
    "PREMIUM_FURNITURE": {
        "base": 10.0,
        "metro_multiplier": 1.2,
        "non_metro_multiplier": 1.1,
        "climate_adjust": {
            "hot_arid": 1.0,
            "hot_humid": 1.0,
            "temperate": 1.1,
            "cold": 1.0,
        },
    },
}


def normalize_asset_name(name: str) -> str:
    return name.strip().upper().replace(" ", "_")
