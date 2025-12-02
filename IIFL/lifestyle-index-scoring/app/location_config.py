# app/location_config.py

from typing import Literal, TypedDict, Dict

ClimateZone = Literal["hot_arid", "hot_humid", "temperate", "cold"]
MetroFlag = Literal["metro", "non_metro"]


class StateProfile(TypedDict):
    climate: ClimateZone
    metro_flag: MetroFlag


# Climate Zone Mapping (IMD-style)
# hot_arid      → Rajasthan, Haryana, parts of North India
# hot_humid     → Coastal states, NE India, Bengal
# temperate     → Karnataka, Kerala highlands, Telangana, MP highlands
# cold          → Himalayan states, J&K, Ladakh

STATE_PROFILES: Dict[str, StateProfile] = {
    # -------- South India --------
    "KARNATAKA": {"climate": "temperate", "metro_flag": "metro"},
    "KERALA": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "TAMIL NADU": {"climate": "hot_humid", "metro_flag": "metro"},
    "TELANGANA": {"climate": "hot_arid", "metro_flag": "metro"},
    "ANDHRA PRADESH": {"climate": "hot_humid", "metro_flag": "non_metro"},

    # -------- West India --------
    "MAHARASHTRA": {"climate": "hot_humid", "metro_flag": "metro"},
    "GOA": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "GUJARAT": {"climate": "hot_arid", "metro_flag": "metro"},

    # -------- North India --------
    "DELHI": {"climate": "hot_arid", "metro_flag": "metro"},
    "RAJASTHAN": {"climate": "hot_arid", "metro_flag": "non_metro"},
    "HARYANA": {"climate": "hot_arid", "metro_flag": "metro"},
    "PUNJAB": {"climate": "hot_arid", "metro_flag": "non_metro"},
    "UTTAR PRADESH": {"climate": "hot_arid", "metro_flag": "non_metro"},
    "UTTARAKHAND": {"climate": "cold", "metro_flag": "non_metro"},
    "HIMACHAL PRADESH": {"climate": "cold", "metro_flag": "non_metro"},
    "JAMMU AND KASHMIR": {"climate": "cold", "metro_flag": "non_metro"},

    # -------- Central India --------
    "MADHYA PRADESH": {"climate": "hot_arid", "metro_flag": "non_metro"},
    "CHHATTISGARH": {"climate": "hot_humid", "metro_flag": "non_metro"},

    # -------- East India --------
    "WEST BENGAL": {"climate": "hot_humid", "metro_flag": "metro"},
    "ODISHA": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "BIHAR": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "JHARKHAND": {"climate": "hot_humid", "metro_flag": "non_metro"},

    # -------- North-East India --------
    "ASSAM": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "ARUNACHAL PRADESH": {"climate": "temperate", "metro_flag": "non_metro"},
    "MEGHALAYA": {"climate": "temperate", "metro_flag": "non_metro"},
    "MANIPUR": {"climate": "temperate", "metro_flag": "non_metro"},
    "MIZORAM": {"climate": "temperate", "metro_flag": "non_metro"},
    "NAGALAND": {"climate": "temperate", "metro_flag": "non_metro"},
    "TRIPURA": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "SIKKIM": {"climate": "cold", "metro_flag": "non_metro"},

    # -------- Union Territories --------
    "ANDAMAN AND NICOBAR ISLANDS": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "CHANDIGARH": {"climate": "hot_arid", "metro_flag": "metro"},
    "DADRA AND NAGAR HAVELI AND DAMAN AND DIU": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "LAKSHADWEEP": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "PUDUCHERRY": {"climate": "hot_humid", "metro_flag": "non_metro"},
    "LADAKH": {"climate": "cold", "metro_flag": "non_metro"},
}


def get_state_profile(state_name: str) -> StateProfile:
    """
    Normalize state name and return climate + metro classification.
    If unknown, default to: metro: non_metro, climate: temperate
    """
    key = (state_name or "").strip().upper()
    return STATE_PROFILES.get(key, {"climate": "temperate", "metro_flag": "non_metro"})
