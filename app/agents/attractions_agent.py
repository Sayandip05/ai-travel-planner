from crewai import Agent
from app.tools.attractions_tools import search_attractions
from langchain_groq import ChatGroq
import os

def create_attractions_agent():
    """Creates a specialized attractions and activities agent using Groq LLM"""
    
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.7
    )
    
    return Agent(
        role="Local Activities Curator",
        goal="Curate personalized attraction recommendations that match traveler preferences, weather conditions, and remaining budget",
        backstory="""You are a destination expert and cultural guide with extensive knowledge 
        of attractions, restaurants, and experiences across major cities. You understand how to 
        match activities to different traveler profiles - from art enthusiasts to food lovers to 
        history buffs. You consider practical factors like weather conditions (suggesting indoor 
        activities on rainy days), time requirements, costs, and how to create a balanced itinerary. 
        You have insider knowledge about which attractions are truly worth visiting and which are 
        tourist traps.""",
        tools=[search_attractions],
        verbose=True,
        llm=llm,
        allow_delegation=False
    )