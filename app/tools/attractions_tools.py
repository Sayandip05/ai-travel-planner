from crewai_tools import tool
import json

@tool("search_attractions")
def search_attractions(
    destination: str,
    preferences: str = "",
    weather_condition: str = "",
    budget: float = 500
) -> str:
    """
    Search for attractions and activities in destination based on preferences and weather.
    
    Args:
        destination: Target city/country
        preferences: User preferences (e.g., "museums, local food, history")
        weather_condition: Current weather condition to suggest indoor/outdoor
        budget: Remaining budget for activities in USD
    
    Returns:
        JSON string with curated attraction recommendations
    """
    mock_attractions = {
        "Paris": [
            {
                "name": "Louvre Museum",
                "category": "museum",
                "estimated_time_hours": 3.5,
                "cost": 17,
                "indoor": True,
                "description": "World's largest art museum, home to Mona Lisa and Venus de Milo. Perfect for rainy days."
            },
            {
                "name": "Musée d'Orsay",
                "category": "museum",
                "estimated_time_hours": 2.5,
                "cost": 16,
                "indoor": True,
                "description": "Impressionist masterpieces in a stunning Beaux-Arts railway station."
            },
            {
                "name": "Le Marais Food Tour",
                "category": "food experience",
                "estimated_time_hours": 3.0,
                "cost": 85,
                "indoor": False,
                "description": "Guided walking tour through historic district with stops at bakeries, cheese shops, and cafes."
            },
            {
                "name": "Eiffel Tower",
                "category": "landmark",
                "estimated_time_hours": 2.0,
                "cost": 28,
                "indoor": False,
                "description": "Iconic Parisian landmark with breathtaking city views. Best on clear days."
            },
            {
                "name": "Seine River Dinner Cruise",
                "category": "dining",
                "estimated_time_hours": 2.5,
                "cost": 95,
                "indoor": True,
                "description": "Elegant dinner cruise past illuminated monuments. Weather-independent."
            },
            {
                "name": "Versailles Palace",
                "category": "historical site",
                "estimated_time_hours": 4.0,
                "cost": 20,
                "indoor": True,
                "description": "Opulent royal château with famous Hall of Mirrors and extensive gardens."
            }
        ]
    }
    
    dest_lower = destination.lower()
    attractions = mock_attractions.get(dest_lower.title(), mock_attractions["Paris"])
    
    # Filter based on weather if provided
    if "rain" in weather_condition.lower() or "cold" in weather_condition.lower():
        # Prioritize indoor activities
        attractions = sorted(attractions, key=lambda x: (not x["indoor"], x["cost"]))
    
    # Filter by preferences
    pref_lower = preferences.lower()
    if pref_lower:
        filtered = []
        for attr in attractions:
            if any(p in attr["category"].lower() or p in attr["description"].lower() 
                   for p in pref_lower.split(',')):
                filtered.append(attr)
        if filtered:
            attractions = filtered
    
    # Filter by budget
    affordable = [a for a in attractions if a["cost"] <= budget][:6]
    
    return json.dumps({
        "destination": destination,
        "attractions": affordable,
        "total_options": len(affordable),
        "weather_adapted": bool(weather_condition),
        "preferences_applied": bool(preferences)
    }, indent=2)