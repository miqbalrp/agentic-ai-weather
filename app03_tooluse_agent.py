from agents import Agent, Runner, function_tool
import asyncio
import streamlit as st
from dotenv import load_dotenv
import requests

load_dotenv()

@function_tool
def get_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetches current weather data for a given location using the Open-Meteo API.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.

    Returns:
        dict: A dictionary containing the weather data or an error message if the request fails.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,weathercode,windspeed_10m,winddirection_10m",
            "timezone": "auto"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather data: {e}"}

weather_specialist_agent = Agent(
    name="Weather Specialist Agent",
    # instructions="You provide accurate and concise weather updates based on user queries in plain language.",
    instructions="""
    You are a weather assistant agent.
    Given current weather data (including temperature, humidity, wind speed/direction, precipitation, and weather codes), provide:
    1. A clear and concise explanation of the current weather conditions.
    2. Practical suggestions or precautions for outdoor activities, travel, health, or clothing based on the data.
    3. If any severe weather is detected (e.g., heavy rain, thunderstorms, extreme heat), highlight necessary safety measures.

    Format your response in two sections:
    Weather Summary:
    - Briefly describe the weather in plain language.

    Suggestions:
    - Offer actionable advice relevant to the weather conditions.
    """,
    tools=[get_current_weather],
    tool_use_behavior="run_llm_again" # or "stop_on_first_tool"
)

async def run_agent(user_input: str):
    result = await Runner.run(weather_specialist_agent, user_input)
    return result.final_output

def main():
    st.title("Weather Assistant")
    user_input = st.text_input("Ask about the weather:")
    
    if st.button("Get Weather Update"):
        with st.spinner("Thinking..."):
            if user_input:
                agent_response = asyncio.run(run_agent(user_input))
                st.write(agent_response)
            else:
                st.write("Please enter a question about the weather.")

if __name__ == "__main__":
    main()