import streamlit as st
import requests
import json
from datetime import date, timedelta

# Page config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Title and introduction
st.title("✈️ AI Travel Planner")
st.markdown("Plan your dream trip with our multi-agent AI crew.")

# Sidebar for inputs
with st.sidebar:
    st.header("Trip Details")
    destination = st.text_input("Destination", "Paris, France")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date.today() + timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", date.today() + timedelta(days=37))
        
    budget = st.number_input("Budget (USD)", min_value=500, value=3000, step=100)
    travelers = st.number_input("Travelers", min_value=1, value=2, step=1)
    
    preferences = st.multiselect(
        "Interests",
        ["Culture", "Food", "Adventure", "Relaxation", "Shopping", "History", "Nature"],
        ["Culture", "Food"]
    )
    
    if st.button("Generate Plan", type="primary"):
        with st.spinner("AI Agents are working on your plan..."):
            try:
                # Prepare payload
                payload = {
                    "destination": destination,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "budget": budget,
                    "preferences": preferences,
                    "travelers": travelers
                }
                
                # Call API
                # Note: Assumes backend is running on localhost:8000
                response = requests.post("http://localhost:8000/api/plan", json=payload)
                
                if response.status_code == 200:
                    st.session_state.plan = response.json()
                    st.success("Plan generated successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")

# Display results
if "plan" in st.session_state:
    plan = st.session_state.plan
    
    st.header(f"Trip to {plan.get('destination')}")
    st.subheader(f"Dates: {plan.get('dates')}")
    st.info(f"Total Estimated Cost: ${plan.get('total_estimated_cost'):,.2f}")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Flights", "Hotels", "Weather", "Attractions"])
    
    with tab1:
        st.subheader("Flight Options")
        if plan.get("flights"):
            for flight in plan.get("flights"):
                with st.expander(f"{flight.get('airline')} - ${flight.get('price')}"):
                    st.write(flight)
        else:
            st.info("No flight details available yet.")
            
    with tab2:
        st.subheader("Accommodation")
        if plan.get("hotels"):
            for hotel in plan.get("hotels"):
                with st.expander(f"{hotel.get('name')} - ${hotel.get('total_price')}"):
                    st.write(hotel)
        else:
            st.info("No hotel details available yet.")
            
    with tab3:
        st.subheader("Weather Forecast")
        weather = plan.get("weather", {})
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Avg High", f"{weather.get('avg_temp_high')}°F")
            st.metric("Condition", weather.get('condition'))
        with col2:
            st.metric("Avg Low", f"{weather.get('avg_temp_low')}°F")
            st.write("Recommendations:", ", ".join(weather.get('recommendations', [])))
            
    with tab4:
        st.subheader("Recommended Activities")
        if plan.get("attractions"):
            for activity in plan.get("attractions"):
                 with st.expander(f"{activity.get('name')} ({activity.get('category')})"):
                    st.write(f"Cost: ${activity.get('cost')}")
                    st.write(activity.get('description'))
        else:
            st.info("No activities generated yet.")
            
    # Reasoning Summary
    st.divider()
    with st.expander("View Agent Reasoning Logic"):
        st.text(plan.get("reasoning_summary"))

else:
    st.info("Enter your trip details and click 'Generate Plan' to get started.")
