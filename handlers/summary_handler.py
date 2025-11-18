from typing import List, Dict, Optional, Union, Any
import re

from functions.make_summary import make_summary
from models.table_health import GOOD, BAD, NEUTRAL


def _clean(text: str) -> str:
    text = re.sub(r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip().lower()


def _classify(name: str) -> tuple:
    name_clean = _clean(name)
    if name_clean in GOOD:
        return "good", GOOD[name_clean]
    if name_clean in BAD:
        return "bad", BAD[name_clean]
    if name_clean in NEUTRAL:
        return "neutral", NEUTRAL[name_clean]
    return "neutral", "No clear consensus exists yet. Best consumed in moderation."


def _classify_nutrition(name: str, value: str, unit: str) -> str:
    try:
        val = float(value)
    except (ValueError, TypeError):
        return "neutral"

    name_lower = name.lower()
    unit_lower = unit.lower()

    if name_lower in ("sugar", "sugars"):
        if unit_lower in ("g", "gram", "grams"):
            if val >= 22.5: return "bad"
            elif val > 5: return "neutral"
            else: return "good"

    elif name_lower in ("sodium", "salt", "natrium"):
        if unit_lower == "mg" and val >= 2000: return "bad"
        elif unit_lower in ("g", "gram", "grams") and val >= 2: return "bad"
        else: return "good"

    elif name_lower in ("saturated fat", "lemak jenuh"):
        if unit_lower in ("g", "gram", "grams") and val > 5: return "bad"
        else: return "neutral"

    elif name_lower in ("trans fat"):
        if val > 0: return "bad"
        else: return "good"

    elif name_lower in ("protein"):
        if unit_lower in ("g", "gram", "grams") and val >= 10: return "good"
        else: return "neutral"

    return "neutral"


def summarize_food_labels(
    data: Dict[str, Any]
) -> Optional[Dict[str, Union[None, str, List[Any]]]]:
    ingredients = []
    for ing in data.get("ingredients", []):
        name = ing.get("name") or ing.get("nama", "")
        detail = ing.get("detail", "")
        status = ing.get("status", "")

        if detail in ("add by user", ""):
            status, detail = _classify(name)

        ingredients.append({
            "name": name,
            "status": status,
            "detail": detail
        })

    nutrition_info = []
    for nut in data.get("nutrition_info", []):
        name = nut.get("name") or nut.get("nama", "")
        value = nut.get("value") or nut.get("nilai", "")
        unit = nut.get("type", "")
        status = _classify_nutrition(name, value, unit)

        nutrition_info.append({
            "name": name,
            "value": value,
            "type": unit,
            "status": status
        })

    data["ingredients"] = ingredients
    data["nutrition_info"] = nutrition_info

    if not ingredients:
        return {
            "name": None,
            "status": "",
            "detail": ""
        }

    print(f"Input: {data}")
    summary = make_summary(data)

    response = {
        "status": "success",
        "data": summary
    }
    print(f"Response: {response}")

    return response
