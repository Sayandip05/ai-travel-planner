from crewai import Agent
from app.tools.weather_tools import get_weather_forecast
from langchain_groq import ChatGroq
import os

def create_weather_agent():
    """Creates a specialized weather analysis agent using Groq LLM"""
    
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    
    return Agent(
        role="Weather and Packing Advisor",
        goal="Provide accurate weather forecasts and practical packing recommendations to ensure travelers are prepared",
        backstory="""You are a meteorologist and travel consultant who specializes in 
        helping travelers prepare for weather conditions at their destinations. You understand 
        seasonal patterns, microclimates, and how weather impacts travel activities. You provide 
        specific, actionable packing advice and help travelers plan activities around expected 
        weather conditions. You always consider both temperature and precipitation when making 
        recommendations.""",
        tools=[get_weather_forecast],
        verbose=True,
        llm=llm,
        allow_delegation=False
    )