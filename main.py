
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from handlers.ingredients_handler import process_ingredients
from handlers.nutrition_handler import process_nutrition_info
from handlers.summary_handler import summarize_food_labels
from handlers.validate_handler import validate_fix_typo_labels

from schemas.schema import (
    IngredientsRequest,
    NutritionInfoRequest,
    AnalyzeResponse,
    MakeSummaryFoodRequest,
    ValidateRequest,
    AnalyzeValidateResponse
)

app = FastAPI(
    title="Noga Unified AI API",
    version="1.0.0",
    description="Unified OCR + Gemini API for Ingredients, Nutrition Info, Summary & Validation",
)

# Auto-initialize database on startup (for Railway deployment)
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting Noga AI API...")
    try:
        from init_db import init_database
        init_database()
    except Exception as e:
        print(f"⚠️  Database initialization skipped: {e}")
        print("⚠️  API will continue but database operations may fail")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": exc.detail
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Noga Unified AI API",
        "version": "1.0.0",
        "endpoints": [
            "/ocr-ingredients",
            "/ocr-nutrition-info",
            "/summary_foods",
            "/validate-fix-typo"
        ]
    }

@app.post("/ocr-ingredients", response_model=AnalyzeResponse)
def ocr_ingredients(req: IngredientsRequest):
    try:
        sources = {
            "ingredients": str(req.composition),
        }
        return process_ingredients(req.session_id, sources)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr-nutrition-info", response_model=AnalyzeResponse)
def ocr_nutrition_info(req: NutritionInfoRequest):
    try:
        sources = {
            "nutrition_info": str(req.nutrition_info),
        }
        return process_nutrition_info(req.session_id, sources)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summary_foods")
def summary_foods(req: MakeSummaryFoodRequest):
    try:
        data = {
            "ingredients": [ing.dict() for ing in req.ingredients],
            "nutrition_info": [nut.dict() for nut in req.nutrition_info],
        }
        result = summarize_food_labels(data)
        if result is None:
            raise HTTPException(status_code=204, detail="No content")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-fix-typo", response_model=AnalyzeValidateResponse)
def validate_fix_typo(req: ValidateRequest):
    try:
        data = {
            "ingredients": req.composition,
            "nutrition_info": req.nutrition_info
        }

        validated = validate_fix_typo_labels(data)

        if not validated:
            raise HTTPException(status_code=500, detail="Validation failed")

        return {
            "result": validated
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
