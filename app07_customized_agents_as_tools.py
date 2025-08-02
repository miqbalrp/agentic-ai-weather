from agents import Agent, Runner, function_tool
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

@function_tool
async def get_weather_update(latitude: float, longitude: float) -> str:
    result = await Runner.run(
        weather_specialist_agent,
        input="Get the current weather condition and suggestion for this location (latitude: {}, longitude: {})".format(latitude, longitude)
        )
    return result.final_output

@function_tool
async def get_air_quality_update(latitude: float, longitude: float) -> str:
    result = await Runner.run(
        air_quality_specialist_agent,
        input="Get the current air quality condition and suggestion for this location (latitude: {}, longitude: {})".format(latitude, longitude)
    )
    return result.final_output

orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions="""
    You are an orchestrator agent with two tools: `get_weather_update` and `get_air_quality_update`.
    Analyze the user's query and invoke:
      - `get_weather_update` for weather-related requests (temperature, humidity, wind, precipitation).
      - `get_air_quality_update` for air quality-related requests (pollutants, AQI).
    If the query requires both, call both tools and merge their outputs.
    Return a single, clear response that addresses the user's question with concise summaries and actionable advice.
    """,
    tools=[get_weather_update, get_air_quality_update],
    tool_use_behavior="run_llm_again"
)

async def run_agent(user_input: str):
    result = await Runner.run(orchestrator_agent, user_input)
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