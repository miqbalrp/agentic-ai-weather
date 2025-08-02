from agents import Agent, Runner, function_tool, handoff, RunContextWrapper
import asyncio
import streamlit as st
from dotenv import load_dotenv
import requests

load_dotenv()

@function_tool
def get_current_weather(latitude: float, longitude: float) -> dict:
    """Fetch current weather data for the given latitude and longitude."""
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,weathercode,windspeed_10m,winddirection_10m",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

weather_specialist_agent = Agent(
    name="Weather Specialist Agent",
    instructions="""
    You are a weather specialist agent.
    Your task is to analyze current weather data, including temperature, humidity, wind speed and direction, precipitation, and weather codes.

    For each query, provide:
    1. A clear, concise summary of the current weather conditions in plain language.
    2. Practical, actionable suggestions or precautions for outdoor activities, travel, health, or clothing, tailored to the weather data.
    3. If severe weather is detected (e.g., heavy rain, thunderstorms, extreme heat), clearly highlight recommended safety measures.

    Structure your response in two sections:
    Weather Summary:
    - Summarize the weather conditions in simple terms.

    Suggestions:
    - List relevant advice or precautions based on the weather.
    """,
    tools=[get_current_weather],
    tool_use_behavior="run_llm_again"
)

@function_tool
def get_current_air_quality(latitude: float, longitude: float) -> dict:
    """Fetch current air quality data for the given latitude and longitude."""

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "european_aqi,us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

air_quality_specialist_agent = Agent(
    name="Air Quality Specialist Agent",
    instructions="""
    You are an air quality specialist agent.
    Your role is to interpret current air quality data and communicate it clearly to users.

    For each query, provide:
    1. A concise summary of the air quality conditions in plain language, including key pollutants and their levels.
    2. Practical, actionable advice or precautions for outdoor activities, travel, and health, tailored to the air quality data.
    3. If poor or hazardous air quality is detected (e.g., high pollution, allergens), clearly highlight recommended safety measures.

    Structure your response in two sections:
    Air Quality Summary:
    - Summarize the air quality conditions in simple terms.

    Suggestions:
    - List relevant advice or precautions based on the air quality.
    """,
    tools=[get_current_air_quality],
    tool_use_behavior="run_llm_again"
)

from pydantic import BaseModel, Field

class HandoffRequest(BaseModel):
    specialist_agent: str = Field(..., description="Name of the specialist agent to hand off to")
    handoff_reason: str = Field(..., description="Reason for the handoff")
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")

async def on_handoff_callback(ctx: RunContextWrapper, user_input: HandoffRequest):
    st.info(f"""
            Handing off to {user_input.specialist_agent} for further processing...\n
            Handoff reason: {user_input.handoff_reason} \n
            Location : {user_input.latitude}, {user_input.longitude} \n
            """)

weather_handoff = handoff(
    agent=weather_specialist_agent,
    tool_name_override="handoff_to_weather_specialist",
    tool_description_override="Handle queries related to weather conditions",
    on_handoff=on_handoff_callback,
    input_type=HandoffRequest
)

air_quality_handoff = handoff(
    agent=air_quality_specialist_agent,
    tool_name_override="handoff_to_air_quality_specialist",
    tool_description_override="Handle queries related to air quality conditions",
    on_handoff=on_handoff_callback,
    input_type=HandoffRequest
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a triage agent.
    Your task is to determine which specialist agent (Weather Specialist or Air Quality Specialist) is best suited to handle the user's query based on the content of the question.

    For each query, analyze the input and decide:
    - If the query is about weather conditions, route it to the Weather Specialist Agent.
    - If the query is about air quality, route it to the Air Quality Specialist Agent.
    - If the query is ambiguous or does not fit either category, provide a clarification request.
    """,
    handoffs=[weather_handoff, air_quality_handoff]
)

async def run_agent(user_input: str):
    result = await Runner.run(triage_agent, user_input)
    return result.final_output

def main():
    st.title("Weather and Air Quality Assistant")
    user_input = st.text_input("Enter your query about weather or air quality:")

    if st.button("Get Update"):
        with st.spinner("Thinking..."):
            if user_input:
                agent_response = asyncio.run(run_agent(user_input))
                st.write(agent_response)
            else:
                st.write("Please enter a question about the weather or air quality.")

if __name__ == "__main__":
    main()