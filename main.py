from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
from utils.ai_insights import get_ai_insight
from database import SessionLocal, ProductivityRecord
from datetime import datetime, timedelta

app = FastAPI(title="AI Productivity Assistant", version="2.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
try:
    model = joblib.load("model/model.pkl")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class PredictionInput(BaseModel):
    hours_worked: float
    sleep_hours: float
    tasks_completed: int
    breaks_taken: int
    focus_level: float

class RoadmapInput(BaseModel):
    topic: str

def generate_recommendation(category: str) -> str:
    if category == "High":
        return "Great job! Keep your current routine consistent."
    elif category == "Medium":
        return "You’re doing okay, but try improving focus or sleep hours."
    else:
        return "You may need more rest or better focus management today."

@app.get("/")
def root():
    return {"message": "AI Productivity Assistant API is running"}

@app.post("/generate_roadmap")
def generate_roadmap(input_data: RoadmapInput):
    prompt = (
        f"Create a concise 5-step learning roadmap for '{input_data.topic}'. "
        "Format as a numbered list. Keep each step short."
    )
    roadmap = get_ai_insight(prompt, max_tokens=200)
    return {"roadmap": roadmap}

@app.post("/predict")
async def predict(input_data: PredictionInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Create dataframe for model
    data = pd.DataFrame([{
        "hours_worked": input_data.hours_worked,
        "sleep_hours": input_data.sleep_hours,
        "tasks_completed": input_data.tasks_completed,
        "breaks_taken": input_data.breaks_taken,
        "focus_level": input_data.focus_level
    }])
    
    try:
        prediction = model.predict(data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    recommendation = generate_recommendation(prediction)
    
    ai_prompt = (
        f"User productivity: {prediction}. "
        f"Stats: {input_data.hours_worked}h work, {input_data.sleep_hours}h sleep, "
        f"{input_data.tasks_completed} tasks, {input_data.breaks_taken} breaks. "
        "Give 3 short, actionable tips."
    )
    ai_text = get_ai_insight(ai_prompt, max_tokens=100)

    # Save to DB
    db = SessionLocal()
    try:
        record = ProductivityRecord(
            hours_worked=input_data.hours_worked,
            sleep_hours=input_data.sleep_hours,
            tasks_completed=input_data.tasks_completed,
            breaks_taken=input_data.breaks_taken,
            focus_level=input_data.focus_level,
            prediction=prediction
        )
        db.add(record)
        db.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        db.close()

    return {
        "prediction": prediction,
        "recommendation": recommendation,
        "ai_text": ai_text
    }

@app.get("/weekly_summary")
def weekly_summary():
    db = SessionLocal()
    try:
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        records = db.query(ProductivityRecord).filter(ProductivityRecord.timestamp >= one_week_ago).all()
        print(f"DEBUG: Found {len(records)} records for weekly summary")
        
        if not records:
            return {"summary": "No data yet for this week."}

        # Basic analytics
        total = len(records)
        high = sum(1 for r in records if r.prediction == "High")
        medium = sum(1 for r in records if r.prediction == "Medium")
        low = sum(1 for r in records if r.prediction == "Low")

        prompt = (
            f"Weekly stats: {high} High, {medium} Medium, {low} Low days ({total} total). "
            "Summarize performance in 3 sentences. Suggest 1 improvement."
        )
        print(f"DEBUG: Sending prompt to AI: {prompt}")
        ai_summary = get_ai_insight(prompt, max_tokens=150)
        print(f"DEBUG: AI response: {ai_summary}")

        return {"summary": ai_summary}
    except Exception as e:
        print(f"ERROR in weekly_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
