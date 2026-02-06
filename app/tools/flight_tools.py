from crewai_tools import tool
import json

@tool("search_flights")
def search_flights(destination: str, start_date: str, end_date: str, budget: float) -> str:
    """
    Search for flight options to a destination within budget.
    
    Args:
        destination: Target city/country
        start_date: Departure date (YYYY-MM-DD)
        end_date: Return date (YYYY-MM-DD)
        budget: Maximum flight budget in USD
    
    Returns:
        JSON string with flight options including airline, times, price, and details
    """
    mock_flights = [
        {
            "airline": "Air France",
            "flight_number": "AF123",
            "departure_time": f"{start_date}T08:00:00",
            "arrival_time": f"{start_date}T20:30:00",
            "duration_hours": 8.5,
            "price": min(budget * 0.4, 850),
            "booking_class": "Economy",
            "notes": "Direct flight, arrives evening - comfortable arrival time for check-in"
        },
        {
            "airline": "British Airways",
            "flight_number": "BA456",
            "departure_time": f"{start_date}T14:00:00",
            "arrival_time": f"{start_date}T02:30:00",
            "duration_hours": 10.5,
            "price": min(budget * 0.3, 650),
            "booking_class": "Economy",
            "notes": "One layover in London, overnight arrival - may need early check-in"
        },
        {
            "airline": "Lufthansa",
            "flight_number": "LH789",
            "departure_time": f"{start_date}T11:00:00",
            "arrival_time": f"{start_date}T13:15:00",
            "duration_hours": 9.25,
            "price": min(budget * 0.35, 720),
            "booking_class": "Economy",
            "notes": "One stop in Frankfurt, afternoon arrival"
        }
    ]
    
    affordable = [f for f in mock_flights if f["price"] <= budget]
    
    return json.dumps({
        "flights": affordable,
        "destination": destination,
        "outbound_date": start_date,
        "return_date": end_date,
        "currency": "USD",
        "total_options": len(affordable)
    }, indent=2)