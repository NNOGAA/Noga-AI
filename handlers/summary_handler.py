from typing import List, Dict, Optional, Union, Any

from functions.make_summary import make_summary


def summarize_food_labels(
    data: Dict[str, Any]
) -> Optional[Dict[str, Union[None, str, List[Any]]]]:
    ingredients = []
    for ing in data.get("ingredients", []):
        normalized = {
            "name": ing.get("name") or ing.get("nama", ""),
            "status": ing.get("status", ""),
            "detail": ing.get("detail", "")
        }
        ingredients.append(normalized)

    data["ingredients"] = ingredients

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
