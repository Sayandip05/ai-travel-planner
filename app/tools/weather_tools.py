from crewai_tools import tool
import json
from datetime import datetime

@tool("search_hotels")
def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    budget_per_night: float,
    preferences: str = "",
    flight_arrival_time: str = ""
) -> str:
    """
    Search for hotel options in destination based on dates and budget.
    
    Args:
        destination: Target city/country
        check_in: Check-in date (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
        check_out: Check-out date (YYYY-MM-DD)
        budget_per_night: Maximum price per night in USD
        preferences: User preferences for filtering hotels
        flight_arrival_time: Optional arrival time to adjust check-in recommendations
    
    Returns:
        JSON string with hotel options including pricing, location, and amenities
    """
    if 'T' in check_in:
        arrival_dt = datetime.fromisoformat(check_in.split('+')[0].replace('Z', ''))
        check_in_date = arrival_dt.date().isoformat()
        early_arrival = arrival_dt.hour < 15
    else:
        check_in_date = check_in
        early_arrival = False
    
    nights = (datetime.fromisoformat(check_out) - datetime.fromisoformat(check_in_date)).days
    
    mock_hotels = [
        {
            "name": "Le Marais Boutique Hotel",
            "location": "Le Marais District - Central Paris, walkable to museums",
            "price_per_night": min(budget_per_night, 180),
            "total_price": min(budget_per_night, 180) * nights,
            "rating": 4.5,
            "amenities": ["Free WiFi", "Breakfast included", "Walking distance to Louvre", "24/7 reception"],
            "check_in_date": check_in_date,
            "check_out_date": check_out,
            "notes": "Early check-in available at no extra cost" if early_arrival else "Standard check-in from 3 PM"
        },
        {
            "name": "Montmartre View Hotel",
            "location": "Montmartre - Artistic district with panoramic views",
            "price_per_night": min(budget_per_night * 0.7, 120),
            "total_price": min(budget_per_night * 0.7, 120) * nights,
            "rating": 4.2,
            "amenities": ["Free WiFi", "Rooftop terrace", "Near Sacré-Cœur", "Metro access"],
            "check_in_date": check_in_date,
            "check_out_date": check_out,
            "notes": "Budget-friendly option in charming neighborhood"
        },
        {
            "name": "Latin Quarter Historic Inn",
            "location": "Latin Quarter - Near Pantheon and Sorbonne",
            "price_per_night": min(budget_per_night * 0.85, 150),
            "total_price": min(budget_per_night * 0.85, 150) * nights,
            "rating": 4.4,
            "amenities": ["Free WiFi", "Continental breakfast", "Historic building", "Central location"],
            "check_in_date": check_in_date,
            "check_out_date": check_out,
            "notes": "Perfect for exploring Left Bank cafes and bookshops"
        }
    ]
    
    affordable = [h for h in mock_hotels if h["price_per_night"] <= budget_per_night]
    
    return json.dumps({
        "hotels": affordable,
        "destination": destination,
        "nights": nights,
        "early_arrival_detected": early_arrival,
        "check_in": check_in_date,
        "check_out": check_out,
        "total_options": len(affordable)
    }, indent=2)