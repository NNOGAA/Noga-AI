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
        nutrition_info.append({
            "name": nut.get("name") or nut.get("nama", ""),
            "value": nut.get("value") or nut.get("nilai", ""),
            "type": nut.get("type", ""),
            "status": nut.get("status", "")
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
