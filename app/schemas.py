from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class TravelRequest(BaseModel):
    destination: str = Field(..., description="Destination city/country")
    start_date: date = Field(..., description="Travel start date")
    end_date: date = Field(..., description="Travel end date")
    budget: float = Field(..., description="Total budget in USD")
    preferences: List[str] = Field(
        default=[], 
        description="User preferences (e.g., museums, food, adventure)"
    )
    travelers: int = Field(default=1, description="Number of travelers")

class FlightOption(BaseModel):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    duration_hours: float
    price: float
    booking_class: str
    notes: Optional[str] = None

class HotelOption(BaseModel):
    name: str
    location: str
    price_per_night: float
    total_price: float
    rating: float
    amenities: List[str]
    check_in_date: str
    check_out_date: str
    notes: Optional[str] = None

class WeatherInfo(BaseModel):
    avg_temp_high: float
    avg_temp_low: float
    condition: str
    precipitation_chance: float
    recommendations: List[str]

class Attraction(BaseModel):
    name: str
    category: str
    estimated_time_hours: float
    cost: float
    indoor: bool
    description: str

class TravelPlan(BaseModel):
    destination: str
    dates: str
    flights: List[FlightOption]
    hotels: List[HotelOption]
    weather: WeatherInfo
    attractions: List[Attraction]
    total_estimated_cost: float
    langfuse_trace_url: Optional[str] = None
    reasoning_summary: str