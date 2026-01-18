from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import TravelRequest, TravelPlan
from app.agents.travel_crew import create_travel_planning_crew
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Travel Planner",
    description="Multi-agent travel planning system using CrewAI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "AI Travel Planner API",
        "endpoints": {
            "plan": "/api/plan",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/plan", response_model=TravelPlan)
async def create_travel_plan(request: TravelRequest):
    """
    Create a complete travel plan using multi-agent collaboration.
    
    This endpoint demonstrates A2A (Agent-to-Agent) orchestration where:
    1. Flight Agent finds optimal flights
    2. Weather Agent provides forecast and packing advice
    3. Hotel Agent coordinates accommodations with flight arrival
    4. Attractions Agent curates activities based on weather and preferences
    """
    try:
        logger.info(f"Creating travel plan for {request.destination}")
        
        # Create the specialized crew
        crew = create_travel_planning_crew(
            destination=request.destination,
            start_date=request.start_date.isoformat(),
            end_date=request.end_date.isoformat(),
            budget=request.budget,
            preferences=request.preferences
        )
        
        # Execute the crew - agents will collaborate sequentially
        result = crew.kickoff()
        
        # Parse the result (in production, you'd have more robust parsing)
        logger.info("Travel plan created successfully")
        
        # For now, return a structured response
        # In production, you'd parse the agent outputs more carefully
        return TravelPlan(
            destination=request.destination,
            dates=f"{request.start_date} to {request.end_date}",
            flights=[],  # Would be populated from flight_agent output
            hotels=[],   # Would be populated from hotel_agent output
            weather={    # Would be populated from weather_agent output
                "avg_temp_high": 45,
                "avg_temp_low": 37,
                "condition": "cold",
                "precipitation_chance": 0.4,
                "recommendations": ["Pack warm layers"]
            },
            attractions=[],  # Would be populated from attractions_agent output
            total_estimated_cost=request.budget * 0.85,
            reasoning_summary=str(result),
            langfuse_trace_url=None
        )
        
    except Exception as e:
        logger.error(f"Error creating travel plan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)