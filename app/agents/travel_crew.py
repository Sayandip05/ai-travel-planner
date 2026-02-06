from crewai import Crew, Task, Process
from app.agents.flight_agent import create_flight_agent
from app.agents.hotel_agent import create_hotel_agent
from app.agents.weather_agent import create_weather_agent
from app.agents.attractions_agent import create_attractions_agent

def create_travel_planning_crew(destination: str, start_date: str, end_date: str, budget: float, preferences: list):
    """
    Creates a crew of specialized agents that work together to plan a complete trip.
    
    This demonstrates Agent-to-Agent collaboration where each agent's output
    becomes context for subsequent agents, enabling intelligent coordination.
    """
    
    # Create all specialized agents
    flight_agent = create_flight_agent()
    hotel_agent = create_hotel_agent()
    weather_agent = create_weather_agent()
    attractions_agent = create_attractions_agent()
    
    # Calculate budget allocations (this is a simple heuristic)
    flight_budget = budget * 0.4
    hotel_budget_per_night = (budget * 0.35) / max(1, (end_date - start_date).days)
    activities_budget = budget * 0.25
    
    preferences_str = ", ".join(preferences) if preferences else "general sightseeing"
    
    # Task 1: Flight Search
    # This agent runs first and its output is passed to subsequent agents
    flight_task = Task(
        description=f"""
        Find the best flight options to {destination} for travel from {start_date} to {end_date}.
        Maximum flight budget: ${flight_budget:.2f}
        
        Requirements:
        1. Search for available flights using the search_flights tool
        2. Analyze options considering price, convenience, and arrival time
        3. Pay special attention to arrival times as they affect hotel check-in
        4. Recommend your top 2 flight options with clear reasoning
        
        Output your recommendations as structured JSON with flight details and reasoning.
        """,
        expected_output="JSON with recommended flights including arrival times and analysis",
        agent=flight_agent
    )
    
    # Task 2: Weather Forecast
    # Runs in parallel with flights, informs packing and activities
    weather_task = Task(
        description=f"""
        Get weather forecast for {destination} during the travel period {start_date} to {end_date}.
        
        Requirements:
        1. Use the weather forecast tool to get conditions
        2. Provide temperature ranges and precipitation probability
        3. Give specific packing recommendations
        4. Suggest whether indoor or outdoor activities are preferable
        
        Output weather information as structured JSON with actionable recommendations.
        """,
        expected_output="JSON with weather forecast and packing recommendations",
        agent=weather_agent
    )
    
    # Task 3: Hotel Search
    # This agent receives flight information as context and adjusts recommendations accordingly
    hotel_task = Task(
        description=f"""
        Find the best hotel accommodations in {destination} for the trip.
        Maximum budget per night: ${hotel_budget_per_night:.2f}
        Travel dates: {start_date} to {end_date}
        Traveler preferences: {preferences_str}
        
        IMPORTANT: Review the flight arrival time from the previous task. If the arrival is:
        - Before 3 PM: Suggest hotels with early check-in or negotiate arrival details
        - After 10 PM: Note that late check-in should be confirmed
        
        Requirements:
        1. Use search_hotels tool with appropriate check-in/check-out dates
        2. Consider the flight arrival time for check-in recommendations
        3. Match hotel location to preferences (museums, food districts, etc.)
        4. Provide 2-3 hotel options with reasoning
        
        Output recommendations as structured JSON with hotel details and reasoning.
        """,
        expected_output="JSON with hotel recommendations coordinated with flight arrival",
        agent=hotel_agent,
        context=[flight_task]  # This task receives flight_task output as context
    )
    
    # Task 4: Attractions and Activities
    # This agent receives both weather and preferences to curate activities
    attractions_task = Task(
        description=f"""
        Curate a personalized list of attractions and activities in {destination}.
        Remaining budget for activities: ${activities_budget:.2f}
        Traveler preferences: {preferences_str}
        
        IMPORTANT: Review the weather forecast from the previous task.
        - If rainy or cold weather is expected, prioritize indoor attractions
        - If weather is good, include outdoor experiences
        
        Requirements:
        1. Use search_attractions tool with preferences and weather info
        2. Create a balanced mix of activities matching preferences
        3. Consider weather conditions for indoor/outdoor recommendations
        4. Ensure total cost fits within activities budget
        5. Provide 4-6 curated recommendations with time estimates
        
        Output as structured JSON with attraction details and reasoning.
        """,
        expected_output="JSON with curated attractions adapted to weather and preferences",
        agent=attractions_agent,
        context=[weather_task]  # This task receives weather_task output as context
    )
    
    # Create the crew with sequential process
    # This ensures tasks execute in order with context passing
    crew = Crew(
        agents=[flight_agent, weather_agent, hotel_agent, attractions_agent],
        tasks=[flight_task, weather_task, hotel_task, attractions_task],
        process=Process.sequential,  # Tasks run in order, passing context
        verbose=True
    )
    
    return crew