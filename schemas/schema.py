from typing import List, Any, Union, Optional, Dict
from pydantic import BaseModel, HttpUrl, Field, validator

class IngredientItem(BaseModel):
    nama: str
    status: str
    detail: str

class NutritionInfoItem(BaseModel):
    nama: str
    nilai: Union[int, float]
    type: str
    status: str

class NutritionItem(BaseModel):
    nama: str
    nilai: Union[int, float]
    type: str
    status: str
    input: Optional[Any] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class IngredientsRequest(BaseModel):
    session_id: str
    composition: HttpUrl

class NutritionInfoRequest(BaseModel):
    session_id: str
    nutrition_info: HttpUrl

class AnalyzeResponse(BaseModel):
    status: str
    data: Dict[str, List]

class RawIngredient(BaseModel):
    name: str
    status: str
    detail: str

class RawNutritionInfo(BaseModel):
    nama: str
    nilai: Union[int, float, str]
    type: str
    status: str

    @validator("nilai", pre=True)
    def coerce_nilai_to_str(cls, v):
        return str(v)

class MakeSummaryFoodRequest(BaseModel):
    ingredients: List[RawIngredient]
    nutrition_info: List[RawNutritionInfo]

class ItemSummary(BaseModel):
    nama: str
    type: str
    nilai: float
    status: str

class RecommendationResponse(BaseModel):
    nama: Optional[str]
    status: str
    data: List[dict]
    detail: Optional[str] = None

class ValidateInputSummaryRequest(BaseModel):
    ingredients: List[dict]

class ValidateInputNutritionInfoRequest(BaseModel):
    nutrition_info: List[dict]

class ValidateRequest(BaseModel):
    composition: HttpUrl
    nutrition_info: HttpUrl

class ValidatedItem(BaseModel):
    original: str
    corrected: str
    is_valid: Optional[bool] = None
    is_nutrition: Optional[bool] = None

class ValidateResponse(BaseModel):
    validated_ingredients: List[dict]

class AnalyzeValidateResponse(BaseModel):
    result: ValidateResponse

class RecognitionFoodRequest(BaseModel):
    foods: HttpUrl

class RecognitionFoodResponse(BaseModel):
    status: str
    foods_detected: List[str]

class MakeRecommendationRequest(BaseModel):
    name: str
    status: str
    detail: str
    ingredients: List[IngredientItem]
    nutrition_info: List[NutritionInfoItem]

class RecommendationDataItem(BaseModel):
    name: str
    status: str
    detail: str
    ingredients: List[IngredientItem]
    nutrition_info: List[NutritionInfoItem]

class RecommendationResponse(BaseModel):
    status: str
    data: List[RecommendationDataItem]
