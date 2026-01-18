from crewai import Agent
from app.tools.hotel_tools import search_hotels
from langchain_groq import ChatGroq
import os

def create_hotel_agent():
    """Creates a specialized hotel search agent using Groq LLM"""
    
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    
    return Agent(
        role="Accommodation Specialist",
        goal="Find hotels that match the traveler's budget, preferences, and flight schedule for a comfortable stay",
        backstory="""You are a hospitality expert with deep knowledge of accommodations 
        worldwide. You understand how flight arrival times affect hotel check-in logistics, 
        the importance of location relative to attractions, and how to balance budget with 
        comfort. You know which neighborhoods are best for different types of travelers and 
        always consider proximity to transportation and key sites. You coordinate closely 
        with flight information to ensure seamless travel logistics.""",
        tools=[search_hotels],
        verbose=True,
        llm=llm,
        allow_delegation=False
    )