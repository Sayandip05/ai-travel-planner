from crewai import Agent
from app.tools.flight_tools import search_flights
from langchain_groq import ChatGroq
import os

def create_flight_agent():
    """Creates a specialized flight search agent using Groq LLM"""
    
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    
    return Agent(
        role="Flight Search Specialist",
        goal="Find optimal flight options that balance cost, convenience, and travel comfort within the user's budget",
        backstory="""You are an experienced travel agent with 15 years of expertise in 
        international flight bookings. You understand airline routes, pricing patterns, 
        layover strategies, and how arrival times impact the overall travel experience. 
        You always consider factors like jet lag, connection times, and arrival convenience 
        when making recommendations. You prioritize value over just finding the cheapest option.""",
        tools=[search_flights],
        verbose=True,
        llm=llm,
        allow_delegation=False
    )