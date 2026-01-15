# AI Travel Planner - Multi-Agent System

A production-grade travel planning system built with CrewAI, demonstrating Agent-to-Agent (A2A) collaboration and intelligent task orchestration.

## Overview

This project showcases a real-world implementation of multi-agent AI systems where specialized agents collaborate to create comprehensive travel plans. Each agent has specific expertise and uses custom tools to gather information, while a coordinator ensures seamless information flow between agents.

## Architecture

### Agent Responsibilities

**Flight Agent**: Searches for optimal flight options considering price, convenience, and arrival times. Uses mock flight API data to simulate real booking platforms.

**Hotel Agent**: Finds accommodations coordinated with flight arrival times. Automatically adjusts check-in recommendations based on when flights land, demonstrating context awareness between agents.

**Weather Agent**: Provides weather forecasts and packing recommendations. Influences downstream decisions by informing which activities should be indoor versus outdoor.

**Attractions Agent**: Curates personalized activities based on traveler preferences and weather conditions. Demonstrates how agent outputs inform subsequent agent reasoning.

### Key Design Patterns

**Sequential Task Execution**: Tasks execute in a defined order, with each agent's output becoming context for subsequent agents. This models real-world planning where flight details inform hotel bookings, and weather forecasts influence activity selection.

**Context Passing**: Agents access previous task outputs through CrewAI's context mechanism, enabling intelligent coordination without direct agent-to-agent communication.

**Tool Abstraction**: Each agent uses specialized tools that encapsulate data retrieval logic, making the system modular and testable.

## Technology Stack

**CrewAI**: Multi-agent orchestration framework
**Groq**: Fast LLM inference for agent reasoning
**FastAPI**: REST API layer for production deployment
**Langfuse**: Observability and tracing (ready for integration)
**Docker**: Containerization for reproducible deployments

## Installation

Clone the repository and navigate to the project directory.

Install dependencies using pip install from the requirements file.

Create a .env file with your Groq API key using the format shown in .env.example.

## Usage

### Test Single Agent

Run the single agent test to verify the Flight Agent works independently:
```bash
python test_single_agent.py
```

This demonstrates how one agent uses its tool, reasons about results, and produces output.

### Test Full Multi-Agent Crew

Run the full crew test to see agent collaboration:
```bash
python test_full_crew.py
```

Watch the terminal output to see how agents pass context to each other and how decisions from one agent inform the next.

### Run FastAPI Server

Start the production API server:
```bash
uvicorn app.main:app --reload
```

Access the interactive API documentation at http://localhost:8000/docs

Send a POST request to /api/plan with travel parameters to create a complete travel plan.

### Docker Deployment

Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at http://localhost:8000

## Project Structure

The project follows a clean architecture with separation of concerns. Agents are defined in the agents directory, tools in the tools directory, and the FastAPI application in main.py. Configuration is centralized in config.py and data models are defined in schemas.py.

## Observability

The system is instrumented for Langfuse integration, providing visibility into agent reasoning chains, tool usage, and decision-making processes. This is essential for debugging and understanding multi-agent behavior in production.

To enable Langfuse tracing, add your Langfuse API keys to the .env file and the system will automatically start sending trace data.

## Portfolio Highlights

This project demonstrates several production-relevant skills:

**Multi-Agent System Design**: Proper decomposition of responsibilities with clear agent boundaries and coordination patterns.

**Context Management**: Implementation of sequential task execution where agent outputs inform downstream decisions, simulating real-world collaborative workflows.

**API Design**: Clean FastAPI implementation with proper error handling, CORS configuration, and structured responses.

**Observability**: Integration-ready tracing and logging for understanding agent behavior in production environments.

**Containerization**: Docker configuration for reproducible deployments across different environments.

**Tool Abstraction**: Modular design where tools can be swapped from mock to real APIs without changing agent logic.

## Future Enhancements

Integration with real APIs (Amadeus for flights, Booking.com for hotels, OpenWeatherMap for weather) would transform this from a demonstration into a production service. Adding Langfuse dashboard analysis would provide insights into agent performance and decision quality. Implementing async task execution for parallel agent operations would improve response times. Adding user authentication and persistent storage would enable full production deployment.

## License

MIT License - See LICENSE file for details.